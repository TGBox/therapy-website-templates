const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
    let reqUrl = req.url.split('?')[0];
    if (reqUrl === '/') reqUrl = '/index.html';
    
    // Normalize path to prevent directory traversal
    const safePath = path.normalize(decodeURIComponent(reqUrl)).replace(/^(\.\.[\/\\])+/, '');
    const filePath = path.join(__dirname, safePath);

    fs.stat(filePath, (err, stats) => {
        if (err || !stats.isFile()) {
            res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(`<h1>404 Not Found</h1><p>Datei nicht gefunden: ${safePath}</p><p><a href="/">Zurück zur Startseite</a></p>`);
            return;
        }

        const ext = path.extname(filePath).toLowerCase();
        const contentType = MIME_TYPES[ext] || 'application/octet-stream';

        res.writeHead(200, {
            'Content-Type': contentType,
            'Cache-Control': 'no-cache'
        });

        const stream = fs.createReadStream(filePath);
        stream.pipe(res);
    });
});

server.listen(PORT, () => {
    console.log(`Demo-Server läuft auf http://localhost:${PORT}`);
    console.log(`Übersicht: http://localhost:${PORT}/index.html`);
    console.log(`Design 1 (UNVERKRAMPFT): http://localhost:${PORT}/design-1-unverkrampft/index.html`);
    console.log(`Design 2 (KINETIQ): http://localhost:${PORT}/design-2-kinetiq/index.html`);
    console.log(`Design 3 (SANA VITA): http://localhost:${PORT}/design-3-sanavita/index.html`);
    console.log(`Design 4 (AURORA MED): http://localhost:${PORT}/design-4-auroramed/index.html`);
    console.log(`Design 5 (VITALWERK): http://localhost:${PORT}/design-5-vitalwerk/index.html`);
});
