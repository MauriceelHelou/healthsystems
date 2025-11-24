import { test } from '@playwright/test'

test('Debug H1 presence', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  
  // Wait for header and main
  await page.waitForSelector('header', { state: 'visible', timeout: 10000 });
  await page.waitForSelector('main', { state: 'visible', timeout: 10000 });
  
  // Get all HTML content
  const html = await page.content();
  console.log('=== Page HTML ===');
  console.log(html);
  
  // Check for H1 elements
  const h1s = await page.locator('h1').all();
  console.log('=== H1 count:', h1s.length);
  
  for (const h1 of h1s) {
    const text = await h1.textContent();
    const classes = await h1.getAttribute('class');
    console.log('H1:', { text, classes });
  }
});
