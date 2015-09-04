var Bear = require('../models/bear');


exports.save = function (req, res) {
  var bear = new Bear();      // create a new instance of the Bear model
  console.log(req.body);
  bear.name = req.body.name;
  bear.save(function(err) {
   if (err) res.send(err);
   res.json({ message: 'Bear created!' });
  });
};


exports.see = function(req, res) {

    Bear.find(function(err, bears) {
     
           if (err)
                res.send(err);

            res.json(bears);
        }); 

 };


 exports.get = function (req, res) {
       Bear.find({ "_id":  req.params.id }, function (err, rcd) {
            if (err) console.log(err);
            res.json(rcd);
       });
};


exports.delete = function (req, res) {

    var query = Bear.remove({ "_id":  req.params.id});
    if(query.exec())
         res.json("'status':'1'"); 
    else 
       res.json("'status':'0'"); 
};


