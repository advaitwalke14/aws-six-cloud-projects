'use strict';

/**
 * Local/reference Lambda@Edge handler.
 * Associate this handler with viewer-request and origin-response events as needed.
 * It does NOT validate CloudFront-native signed URLs; CloudFront's trusted key
 * group should enforce those before private content is served.
 */
const SUSPICIOUS_PATTERNS = [
  /<\s*script/i,
  /<\s*iframe/i,
  /union\s+select/i,
  /javascript\s*:/i,
  /(?:^|[\\/])\.\.(?:[\\/]|$)/i,
  /%0d|%0a/i
];

function hasSuspiciousQuery(queryString) {
  let decoded;
  try {
    decoded = decodeURIComponent(String(queryString || '').replace(/\+/g, ' '));
  } catch (_error) {
    return true;
  }
  return SUSPICIOUS_PATTERNS.some((pattern) => pattern.test(decoded));
}

function getHeader(headers, name) {
  const values = headers && headers[name.toLowerCase()];
  return Array.isArray(values) && values.length ? String(values[0].value || '') : '';
}

function forbiddenResponse() {
  return {
    status: '403',
    statusDescription: 'Forbidden',
    headers: {
      'cache-control': [{ key: 'Cache-Control', value: 'no-store' }],
      'content-type': [{ key: 'Content-Type', value: 'text/plain; charset=utf-8' }],
      'x-content-type-options': [{ key: 'X-Content-Type-Options', value: 'nosniff' }]
    },
    body: 'Forbidden'
  };
}

function handleRequest(request) {
  if (hasSuspiciousQuery(request.querystring)) {
    return forbiddenResponse();
  }

  const accept = getHeader(request.headers, 'accept').toLowerCase();
  if (accept.includes('image/webp')) {
    request.uri = request.uri.replace(/\.(jpe?g|png)$/i, '.webp');
  }

  return request;
}

function handleOriginResponse(response, request) {
  const uri = String((request && request.uri) || '');
  const lowerUri = uri.toLowerCase();
  const privateAsset = lowerUri.startsWith('/private/');

  if (privateAsset) {
    response.headers['cache-control'] = [
      { key: 'Cache-Control', value: 'private, no-store' }
    ];
  } else if (/\.(jpg|jpeg|png|webp|avif|css|js|woff2?)$/i.test(lowerUri)) {
    response.headers['cache-control'] = [
      { key: 'Cache-Control', value: 'public, max-age=3600, s-maxage=86400, stale-while-revalidate=600' }
    ];
  } else if (/\.(html?)$/i.test(lowerUri) || lowerUri === '/') {
    response.headers['cache-control'] = [
      { key: 'Cache-Control', value: 'public, max-age=0, s-maxage=60, must-revalidate' }
    ];
  } else {
    response.headers['cache-control'] = [
      { key: 'Cache-Control', value: 'public, max-age=300, s-maxage=1800' }
    ];
  }

  response.headers['x-content-type-options'] = [
    { key: 'X-Content-Type-Options', value: 'nosniff' }
  ];
  return response;
}

exports.handler = (event, _context, callback) => {
  const cf = event && event.Records && event.Records[0] && event.Records[0].cf;
  if (!cf) {
    return callback(null, forbiddenResponse());
  }

  if (cf.request && cf.response) {
    return callback(null, handleOriginResponse(cf.response, cf.request));
  }
  if (cf.request) {
    return callback(null, handleRequest(cf.request));
  }
  return callback(null, forbiddenResponse());
};

exports._test = { hasSuspiciousQuery, handleRequest, handleOriginResponse };
