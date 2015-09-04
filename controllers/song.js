var Song = require('../models/song');

exports.save = function (req, res) {
var song= new Song();
song.songId=req.body.songId;
song.name=req.body.name;
song.artist=req.body.artist;
song.save(function(err) {
if (err) res.send(err);
res.json({ message: 'created!' });
});
};

exports.see = function(req, res) {
Song.find(function(err, val) {
if (err)
	res.send(err);
		res.json(val);
}); 
};

exports.updatesongId = function (req, res) {
	Song.update({ 'songId':  req.params.songId}, req.body , {} , function (err, count) {
		if (err) console.log(err);
		res.send({ 'updated': count });
	});
};

exports.getsongId = function(req, res) {
	Song.find({ 'songId':  req.params.songId }, function (err, rcd) {
		if (err) console.log(err);
		res.json(rcd);
	});
};

exports.deletesongId = function (req, res) {
	var query =Song.remove({ 'songId':  req.params.songId});
	if(query.exec()) res.json("'status':'1'");
	else res.json("'status':'0'"); 
};

exports.getname = function(req, res) {
	Song.find({ 'name':  req.params.name }, function (err, rcd) {
		if (err) console.log(err);
		res.json(rcd);
	});
};

