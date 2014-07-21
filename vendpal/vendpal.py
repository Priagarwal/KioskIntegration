import tempfile

import cv2
from flask import Flask, jsonify, request
import numpy as np
from sqlalchemy.orm.exc import NoResultFound

from models import User, Device, db
import faceutil

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['DATA_DIR'] = 'data'
app.config['TRAIN_DIR'] = 'images'
app.config['TRAIN_SIZE'] = (160, 160)
app.config['TRAIN_SIZE_MIN'] = (64, 64)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/vendpal.db'
app.config.from_envvar('VENDPAL_SETTINGS', silent=True)

db.init_app(app)

recognizer = None
def clear_recognizer():
    global recognizer
    recognizer = cv2.createLBPHFaceRecognizer()
clear_recognizer()

@app.route('/clear', methods=['GET'])
def clear_state():
    clear_recognizer()
    for user in User.query.all():
        user.is_checked_in = False
    Device.query.delete()
    db.session.commit()
    return jsonify(error=None), 200

@app.route('/login', methods=['POST'])
def login():
    identifier = request.form['device']
    user_email = request.form['email']
    if not Device.query.filter_by(identifier=identifier).count():
        device = Device(identifier)
        try:
            device.user = User.query.filter_by(email=user_email).one()
        except NoResultFound:
            return jsonify(error="No user found with email {}".format(user_email)), 400
        db.session.add(device)
        db.session.commit()
        return jsonify(error=None), 200
    else:
        return jsonify(error="A user is already logged in on device {}".format(identifier)), 400

@app.route('/checkin', methods=['POST'])
def checkin():
    identifier = request.form['device']
    try:
        device = Device.query.filter_by(identifier=identifier).one()
    except NoResultFound:
        return jsonify(error="No user logged in on device {}".format(identifier)), 400
    user = User.query.get(device.user_id)
    if not user.is_checked_in:
        user_images = user.images()
        recognizer.update(np.asarray(user_images), np.asarray(len(user_images) * [user.id]))
        user.is_checked_in = True
        db.session.commit()
    return jsonify(error=None,email=user.email), 200

@app.route('/recognize', methods=['POST'])
def recognize():
    temp = tempfile.NamedTemporaryFile(suffix='.jpg')
    request.files['capture.jpg'].save(temp)
    temp.flush()
    image = cv2.imread(temp.name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    face = faceutil.largest_face(image)[0]
    if face.size:
        prediction = recognizer.predict(cv2.resize(face, app.config['TRAIN_SIZE']))
        return jsonify(email=User.query.get(prediction[0]).email, confidence=prediction[1], error=None), 200
    else:
        return jsonify(email=None, confidence=None, error="No face detected in image"), 400

if __name__ == '__main__':
    import os
    if not os.path.exists(app.config['DATA_DIR']):
        from models import init_db
        with app.app_context():
            init_db(traindir=app.config['TRAIN_DIR'])

    app.run(host='0.0.0.0')
