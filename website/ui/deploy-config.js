var secrets = require('./secrets.js');

var s3Credential = {
  accessKeyId:     secrets.s3.accessKeyId,
  secretAccessKey: secrets.s3.secretAccessKey,
  params: {
    Bucket:        'concorde-assets'
  }
};

var config = {
  s3: {
    // Let's stick with single S3 bucket for now
    development: {
      credentials: s3Credential,
      dirname: '/development/assets',
      assetsPath: 'dist/assets/*',
    },
    staging: {
      credentials: s3Credential,
      dirname: '/development/assets',
      assetsPath: 'dist/assets/*',
    },
    me: {
      credentials: s3Credential,
      dirname: '/development/assets',
      assetsPath: 'dist/assets/*',
    },
    production: {
      credentials: s3Credential,
      dirname: '/development/assets',
      assetsPath: 'dist/assets/*',
    }
  }
};

module.exports = config;

