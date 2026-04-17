import puppeteer from 'puppeteer';
import { writeFile, mkdir } from 'fs/promises';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { existsSync } from 'fs';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const outDir = join(__dirname, 'temporary screenshots');

const url = process.argv[2] || 'http://localhost:3000';
const label = process.argv[3] ? `-${process.argv[3]}` : '';

await mkdir(outDir, { recursive: true });

// Auto-increment screenshot number
let n = 1;
while (existsSync(join(outDir, `screenshot-${n}${label}.png`))) n++;
const outPath = join(outDir, `screenshot-${n}${label}.png`);

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1.5 });
await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
await new Promise(r => setTimeout(r, 1200));

await page.screenshot({ path: outPath, fullPage: true });
await browser.close();

console.log(`Screenshot saved: ${outPath}`);
