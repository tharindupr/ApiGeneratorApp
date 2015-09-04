var mongoose     = require('mongoose');
var Schema= mongoose.Schema;
var SongSchema   = new Schema({
songId:String,name:String,artist:String
});
module.exports = mongoose.model('Song', SongSchema);