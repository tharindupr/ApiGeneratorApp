var express = require('express');
var router = express.Router();

var entityController = require('../controllers/entity');

router.route('/list')

	.post(function(req, res) {
	entityController.listEntities(req, res)
	});

router.route('/meta')

	.post(function(req, res) {
	entityController.listMeta(req, res)
	});
	



module.exports = router;