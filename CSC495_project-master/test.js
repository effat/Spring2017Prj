//Sample API usage
var guardian = require('guardian-js');
let api = new guardian('8d020f80-9140-41b0-a45f-9c7ceb9e5ddf', false);

api.content.search('cookie privacy data')
    .then(function(response) {
               console.log(response.body);
     });
