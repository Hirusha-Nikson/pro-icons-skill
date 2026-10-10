import fs from 'node:fs';
import path from 'node:path';
import * as si from 'simple-icons';
import sharp from 'sharp';

const SKILL = path.resolve('skills/dev-icons');
const list = JSON.parse(fs.readFileSync('source/icons.json', 'utf8'));

// Simple Icons exports objects like siReact → index them by slug
const bySlug = {};
for (const icon of Object.values(si)) if (icon && icon.slug) bySlug[icon.slug] = icon;

const DARK_BG = '#242938';
const LIGHT_BG = '#F4F2ED';
const PNG_SIZES = [128, 512];          // 128 for docs, 512 for slides/video

// relative brightness of a hex colour (0 = black, 1 = white)
function luminance(hex) {
  const [r, g, b] = [0, 2, 4].map(i => {
    const c = parseInt(hex.slice(i, i + 2), 16) / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');

function tileSvg(icon, theme) {
  const brand = '#' + icon.hex;
  const L = luminance(icon.hex);
  let bg, fg;
  if (theme === 'dark')  { bg = DARK_BG;  fg = L < 0.12 ? '#FFFFFF' : brand; }
  if (theme === 'light') { bg = LIGHT_BG; fg = L > 0.70 ? DARK_BG  : brand; }
  if (theme === 'brand') { bg = brand;    fg = L > 0.50 ? '#000000' : '#FFFFFF'; }
  // icon paths are 24×24 → scale ×6 = 144px, centred in a 256px tile
  return `<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" role="img" aria-label="${esc(icon.title)}"><title>${esc(icon.title)}</title><rect width="256" height="256" rx="60" fill="${bg}"/><g transform="translate(56 56) scale(6)"><path d="${icon.path}" fill="${fg}"/></g></svg>`;
}

const manifest = [];
const missing = [];

for (const theme of ['dark', 'light', 'brand']) {
  fs.mkdirSync(path.join(SKILL, 'icons', theme), { recursive: true });
  for (const size of PNG_SIZES) fs.mkdirSync(path.join(SKILL, 'png', theme, String(size)), { recursive: true });
}

for (const item of list) {
  const icon = bySlug[item.slug];
  if (!icon) { missing.push(`${item.id} (slug "${item.slug}")`); continue; }

  for (const theme of ['dark', 'light', 'brand']) {
    const svg = tileSvg(icon, theme);
    fs.writeFileSync(path.join(SKILL, 'icons', theme, `${item.id}.svg`), svg);
    for (const size of PNG_SIZES) {
      await sharp(Buffer.from(svg)).resize(size, size).png()
        .toFile(path.join(SKILL, 'png', theme, String(size), `${item.id}.png`));
    }
  }
  manifest.push({
    id: item.id, name: item.name, category: item.category,
    aliases: item.aliases, hex: '#' + icon.hex, source: 'simple-icons'
  });
}

fs.writeFileSync(path.join(SKILL, 'manifest.json'), JSON.stringify(manifest, null, 2));
console.log(`✔ Built ${manifest.length} icons × 3 themes`);
if (missing.length) console.log(`✘ Not found in Simple Icons:\n  - ${missing.join('\n  - ')}`);
