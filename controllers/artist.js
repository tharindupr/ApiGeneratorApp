var Artist = require('../models/artist');

exports.save = function (req, res) {
var artist= new Artist();
artist.name=req.body.name;
artist.style=req.body.style;
artist.location=req.body.location;
artist.save(function(err) {
if (err) res.send(err);
res.json({ message: 'created!' });
});
};

exports.see = function(req, res) {
Artist.find(function(err, val) {
if (err)
	res.send(err);
		res.json(val);
}); 
};

exports.updatename = function (req, res) {
	Artist.update({ 'name':  req.params.name}, req.body , {} , function (err, count) {
		if (err) console.log(err);
		res.send({ 'updated': count });
	});
};

exports.getname = function(req, res) {
	Artist.find({ 'name':  req.params.name }, function (err, rcd) {
		if (err) console.log(err);
		res.json(rcd);
	});
};

exports.deletename = function (req, res) {
	var query =Artist.remove({ 'name':  req.params.name});
	if(query.exec()) res.json("'status':'1'");
	else res.json("'status':'0'"); 
};

