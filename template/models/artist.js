var mongoose     = require('mongoose');
var Schema= mongoose.Schema;
var ArtistSchema   = new Schema({
name:String,style:String,location:String
});
module.exports = mongoose.model('Artist', ArtistSchema);