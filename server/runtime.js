const http = require("http");
const fs = require("fs");
const path = require("path");

const server = http.createServer((req, res) => {
    if (req.url === "/") {
        const filePath = path.join(__dirname, "templates", "index.html");
        const readStream = fs.createReadStream(filePath);
        readStream.pipe(res);
    } else {
        res.writeHead(404);
        res.end();
    }
});

server.listen(3006, () => {
    console.log("Server running on http://localhost:3006");
});
