const fs = require('fs');
const path = require('path');

// Create dist directory
const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

// Copy views directory
const viewsDir = path.join(__dirname, 'views');
const viewsDist = path.join(distDir, 'views');
if (fs.existsSync(viewsDir)) {
  if (!fs.existsSync(viewsDist)) {
    fs.mkdirSync(viewsDist, { recursive: true });
  }
  fs.readdirSync(viewsDir).forEach(file => {
    const src = path.join(viewsDir, file);
    const dest = path.join(viewsDist, file);
    fs.copyFileSync(src, dest);
  });
}

// Copy app.js
const appSrc = path.join(__dirname, 'app.js');
const appDest = path.join(distDir, 'app.js');
if (fs.existsSync(appSrc)) {
  fs.copyFileSync(appSrc, appDest);
}

// Copy package.json
const pkgSrc = path.join(__dirname, 'package.json');
const pkgDest = path.join(distDir, 'package.json');
if (fs.existsSync(pkgSrc)) {
  fs.copyFileSync(pkgSrc, pkgDest);
}

console.log('Build complete: files copied to dist/');
