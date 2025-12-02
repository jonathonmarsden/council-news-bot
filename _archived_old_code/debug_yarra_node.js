
const https = require('https');

const url = 'https://www.yarracity.vic.gov.au/news';

const options = {
  headers: {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-AU,en;q=0.9',
  }
};

https.get(url, options, (res) => {
  console.log('StatusCode:', res.statusCode);
  console.log('Headers:', res.headers);

  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    console.log('Body length:', data.length);
    if (res.statusCode === 200) {
        console.log('Preview:', data.substring(0, 500));
    } else {
        console.log('Preview:', data.substring(0, 500));
    }
  });

}).on('error', (e) => {
  console.error(e);
});
