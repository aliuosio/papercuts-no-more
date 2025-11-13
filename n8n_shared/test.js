const http = require('http');

const options = {
  hostname: 'webserver',
  port: 8000,
  path: '/api/',
  method: 'GET',
  auth: 'admin:admin123'
};

const req = http.request(options, (res) => {
  console.log(`STATUS: ${res.statusCode}`);
  res.on('data', (chunk) => {
    console.log(`BODY: ${chunk}`);
  });
});

req.on('error', (e) => {
  console.error(`problem with request: ${e.message}`);
});

req.end();
