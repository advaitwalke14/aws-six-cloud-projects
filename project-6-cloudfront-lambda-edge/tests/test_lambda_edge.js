'use strict';
const assert = require('node:assert/strict');
const edge = require('../lambda/index.js');
const {
  hasSuspiciousQuery,
  handleRequest,
  handleOriginResponse
} = edge._test;
let passed = 0;
function test(name, fn) {
  fn();
  console.log(`PASS: ${name}`);
  passed++;
}
function request(uri, querystring = '', accept = '') {
  const headers = {};
  if (accept) {
    headers.accept = [{ key: 'Accept', value: accept }];
  }
  return { uri, querystring, headers };
}
function responseFor(uri) {
  const response = { status: '200', headers: {} };
  return handleOriginResponse(response, { uri });
}
test('clean query is allowed', () => {
  assert.equal(hasSuspiciousQuery('page=2&sort=recent'), false);
});
test('script query is detected', () => {
  assert.equal(
    hasSuspiciousQuery('q=%3Cscript%3Ealert(1)%3C/script%3E'),
    true
  );
});
test('SQL injection pattern is detected', () => {
  assert.equal(hasSuspiciousQuery('q=union%20select%20password'), true);
});
test('malformed query encoding is rejected', () => {
  assert.equal(hasSuspiciousQuery('q=%E0%A4%A'), true);
});
test('suspicious request receives 403 and no-store', () => {
  const result = handleRequest(request('/search', 'q=%3Cscript%3E'));
  assert.equal(result.status, '403');
  assert.equal(result.headers['cache-control'][0].value, 'no-store');
});
test('JPEG path is rewritten when WebP is accepted', () => {
  const result = handleRequest(
    request('/images/cat.jpg', '', 'image/webp,image/*')
  );
  assert.equal(result.uri, '/images/cat.webp');
});
test('image path is not rewritten without WebP support', () => {
  const result = handleRequest(
    request('/images/cat.jpg', '', 'image/jpeg')
  );
  assert.equal(result.uri, '/images/cat.jpg');
});
test('private asset response is not cacheable', () => {
  const result = responseFor('/private/report.pdf');
  assert.equal(
    result.headers['cache-control'][0].value,
    'private, no-store'
  );
});
test('static asset receives shared cache policy', () => {
  const result = responseFor('/images/cat.webp');
  assert.equal(
    result.headers['cache-control'][0].value,
    'public, max-age=3600, s-maxage=86400, stale-while-revalidate=600'
  );
});
test('HTML receives revalidation policy', () => {
  const result = responseFor('/index.html');
  assert.equal(
    result.headers['cache-control'][0].value,
    'public, max-age=0, s-maxage=60, must-revalidate'
  );
});
test('security header is added to origin responses', () => {
  const result = responseFor('/images/cat.webp');
  assert.equal(
    result.headers['x-content-type-options'][0].value,
    'nosniff'
  );
});
test('unknown content uses conservative default cache policy', () => {
  const result = responseFor('/api/status');
  assert.equal(
    result.headers['cache-control'][0].value,
    'public, max-age=300, s-maxage=1800'
  );
});
console.log(`\n${passed}/12 JavaScript handler tests passed.`);
