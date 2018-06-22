var express = require('express');
var proxy = require('http-proxy-middleware');

var app = express();

// static
app.use('/', express.static('dist'));

// api proxy
var apiAddr = 'api_addr_error'
if (typeof(process.env.APIADDR) !== 'undefined' && process.env.APIADDR !== '') {
    apiAddr = process.env.APIADDR
}
var apiProxy = proxy('/api', {target: apiAddr});
app.use('/api', apiProxy)

var adminProxy = proxy('/admin', {target: apiAddr});
app.use('/admin', adminProxy)

var adminStaticProxy = proxy('/static', {target: apiAddr});
app.use('/static', adminStaticProxy)
// start server
var port = 80;
app.listen(port);
console.log('Running on http://localhost:' + port);
