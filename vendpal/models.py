import os

import cv2
import numpy as np

from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(64), unique=True)
    fb_id = db.Column(db.Integer, default=0)
    devices = db.relationship('Device', backref='user')
    is_checked_in = db.Column(db.Boolean, default=False)

    def __init__(self, email):
        self.email = email

    def images(self):
        datadir = current_app.config['DATA_DIR']
        images = []
        for i in os.walk(os.path.join(datadir, self.email)).next()[2]:
            images.append(np.load(os.path.join(datadir, self.email, i)))
        if self.fb_id and os.path.exists(os.path.join(datadir, 'fb', str(self.fb_id))):
            for i in os.walk(os.path.join(datadir, 'fb', str(self.fb_id))).next()[2]:
                images.append(np.load(os.path.join(datadir, 'fb', str(self.fb_id), i)))
        return images


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    identifier = db.Column(db.String(64), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, identifier):
        self.identifier = identifier


import json

import faceutil

def init_db(traindir):
    datadir = current_app.config['DATA_DIR']
    os.makedirs(datadir)
    db.create_all()
    with open(os.path.join(traindir, 'facebook_mapping')) as facebook_mapping_file:
        facebook_mapping = json.load(facebook_mapping_file)
    # create users
    for email in os.walk(traindir).next()[1]:
        user = User(email)
        try:
            user.fb_id = facebook_mapping[user.email]
        except KeyError:
            print('No facebook mapping for {}'.format(user.email))
        db.session.add(user)
        db.session.commit()
    # # load all default images
    for user in User.query.all():
        faces = []
        for image in os.walk(os.path.join(traindir, user.email)).next()[2]:
            face, x,y,w,h = faceutil.largest_face(cv2.imread(os.path.join(traindir, user.email, image), cv2.CV_LOAD_IMAGE_GRAYSCALE))
            if current_app.config['TRAIN_SIZE_MIN'] < (w, h):
                faces.append(cv2.resize(face, current_app.config['TRAIN_SIZE']))
        os.makedirs(os.path.join(datadir, user.email))
        for i, face in enumerate(faces):
            np.save(os.path.join(datadir, user.email, str(i)), face)
        os.makedirs(os.path.join(datadir, 'png', user.email))
        for i, face in enumerate(faces):
            cv2.imwrite(os.path.join(datadir, 'png', user.email, '{}.png'.format(i)), face)
    # load images from facebook
    os.makedirs(os.path.join(datadir, 'fb'))
    os.makedirs(os.path.join(datadir, 'png', 'fb'))
    for file_ in os.listdir(traindir):
        if file_.endswith(".json"):
            with open(os.path.join(traindir, file_)) as fbimgjson_file:
                fbimgjson = json.load(fbimgjson_file)
                fbimg = cv2.imread(os.path.join(traindir, fbimgjson["filename"]), cv2.CV_LOAD_IMAGE_GRAYSCALE)
                faces = faceutil.faces(fbimg)
                for tag in fbimgjson['tags']:
                    if 'x' in tag and 'y' in tag:
                        tag['x'] = tag['x']*fbimg.shape[1]/100
                        tag['y'] = tag['y']*fbimg.shape[0]/100
                for face, x,y,w,h in faces:
                    if current_app.config['TRAIN_SIZE_MIN'] < (w, h):
                        face = cv2.resize(face, current_app.config['TRAIN_SIZE'])
                        tags = filter(lambda tag: 'x' in tag and 'y' in tag and tag['x'] > x and tag['x'] < x+w and tag['y'] > y and tag['y'] < y+h, fbimgjson['tags'])
                        if len(tags) == 1 and 'id' in tags[0]:
                            if not os.path.exists(os.path.join(datadir, 'fb', tags[0]['id'])):
                                os.makedirs(os.path.join(datadir, 'fb', tags[0]['id']))
                            np.save(os.path.join(datadir, 'fb', tags[0]['id'], fbimgjson['id']), face)
                            if not os.path.exists(os.path.join(datadir, 'png', 'fb', tags[0]['id'])):
                                os.makedirs(os.path.join(datadir, 'png', 'fb', tags[0]['id']))
                            cv2.imwrite(os.path.join(datadir, 'png', 'fb', tags[0]['id'], '{}.png'.format(fbimgjson['id'])), face)
