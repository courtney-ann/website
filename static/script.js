var MongoClient = require('mongodb').MongoClient;
var url = "MONGO_CONNECTION_STRING";

MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  var dbo = db.db("drivers");
  dbo.collection("driverList").find({}).toArray(function(err, result) {
    if (err) throw err;
    console.log(result);
    db.close();
  });
});