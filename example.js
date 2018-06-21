const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  await page.goto('https://www.twitch.tv/videos/275765066');
  //await page.screenshot({path: 'example.png'});
  await new Promise(resolve => setTimeout(resolve, 5000));
  await browser.close();
})();
