var restify = require('restify');
var MongoClient = require('mongodb').MongoClient;
var mongodb = null;
var ip_addr = '127.0.0.1';
var port    =  '8080';
var users = null;
var checkedInUsers = null;
var server = restify.createServer({
   name : "myapp"
});

server.use(restify.queryParser());
server.use(restify.bodyParser());
server.use(restify.CORS());

MongoClient.connect('mongodb://127.0.0.1:27017/kiosk', function(err, db) {
	if(err) throw err;
	console.log('connected');
	mongodb = db;
	users = mongodb.collection("users");
	checkedInUsers = mongodb.collection("checkedInUsers");
	server.listen(port, function() {
		console.log('%s listening at %s', server.name, server.url);
	});
});


var PATH1 = '/users';
server.get({path : PATH1 , version : '0.0.1'} , findAllUsers);
server.get({path : PATH1 +'/:userId' , version : '0.0.1'} , findUser);
server.post({path : PATH1 , version: '0.0.1'} ,createNewUser);
server.del({path : PATH1 +'/:userId' , version: '0.0.1'} ,deleteUser);

var PATH2 = '/checkedInUsers';
server.get({path : PATH2 , version : '0.0.1'} , findAllCheckedInUsers);
server.get({path : PATH2 +'/:checkInId' , version : '0.0.1'} , findACheckedInUser);
server.post({path : PATH2 , version: '0.0.1'} ,checkInUser);
server.del({path : PATH2 +'/:checkInId' , version: '0.0.1'} ,checkOutUser);

function findAllCheckedInUsers(req, res , next){
    res.setHeader('Access-Control-Allow-Origin','*');
    checkedInUsers.find().limit(20).sort({postedOn : -1} , function(err , success){
        console.log('Response success '+success);
        console.log('Response error '+err);
        if(success){
            res.send(200 , success);
            return next();
        }else{
            return next(err);
        }
 
    });
 
}

function findACheckedInUser(req, res , next){
    res.setHeader('Access-Control-Allow-Origin','*');
    checkedInUsers.findOne({_id:mongojs.ObjectId(req.params.checkInId)} , function(err , success){
        console.log('Response success '+success);
        console.log('Response error '+err);
        if(success){
            res.send(200 , success);
            return next();
        }
        return next(err);
    })
}
 
function checkInUser(req , res , next){
    var buyer = {};
    buyer.name = req.params.name;
    buyer.email = req.params.email;
    buyer.password = req.params.password;
    buyer.checkedOn = new Date();
 
    res.setHeader('Access-Control-Allow-Origin','*');
 
    checkedInUsers.save(buyer , function(err , success){
        console.log('Response success '+success);
        console.log('Response error '+err);
        if(success){
            res.send(201 , buyer);
            return next();
        }else{
            return next(err);
        }
    });
}
 
function checkOutUser(req , res , next){
    res.setHeader('Access-Control-Allow-Origin','*');
    checkedInUsers.remove({_id:mongojs.ObjectId(req.params.buyerId)} , function(err , success){
        console.log('Response success '+success);
        console.log('Response error '+err);
        if(success){
            res.send(204);
            return next();      
        } else{
            return next(err);
        }
    })
 
}

function findAllUsers(req, res , next){
    res.setHeader('Access-Control-Allow-Origin','*');
    users.find().limit(20).toArray(function(err , success){
        console.log('Response success '+ success);
        console.log('Response error '+err);
        if(success){
            res.send(200 , success);
            //return next();
        }else{
            return next(err);
        }
 
    });
 
}


function findUser(req, res , next){
    res.setHeader('Access-Control-Allow-Origin','*');
    users.findOne({_id:mongojs.ObjectId(req.params.userId)} , function(err , success){
        console.log('Response success '+success);
        console.log('Response error '+err);
        if(success){
            res.send(200 , success);
            return next();
        }
        return next(err);
    })
}
 
function createNewUser(req , res , next){
	var user = {};
    user.name = req.params.name;
    user.email = req.params.email;
    user.password = req.params.password;
    user.createdOn = new Date();
    res.setHeader('Access-Control-Allow-Origin','*');
 
    users.save(user , function(err , success){
        console.log('Response success '+success);
        console.log('Response error '+err);
        if(success){
            res.send(201 , user);
            return next();
        }else{
            return next(err);
        }
    });
	return '{"text": "Sample Text"}';
}
 
function deleteUser(req , res , next){
    res.setHeader('Access-Control-Allow-Origin','*');
    users.remove({_id:mongojs.ObjectId(req.params.userId)} , function(err , success){
        console.log('Response success '+success);
        console.log('Response error '+err);
        if(success){
            res.send(204);
            return next();      
        } else{
            return next(err);
        }
    })
 
}


