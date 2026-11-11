import http from 'node:http';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
import {createHandler} from './app.mjs';
const handler=createHandler();const root=path.resolve('dist');const port=Number(process.env.PORT||8770);
http.createServer(async(req,res)=>{
 if(req.url.startsWith('/api/'))return handler(req,res);
 const pathname=new URL(req.url,'http://localhost').pathname;let file=path.resolve(root,'.'+pathname);
 if(!file.startsWith(root+path.sep)&&file!==root){res.writeHead(403);return res.end();}
 if(pathname==='/'||!path.extname(pathname))file=path.join(root,'index.html');
 try{const bytes=await readFile(file);res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.js':'application/javascript','.mjs':'application/javascript','.css':'text/css','.wasm':'application/wasm'})[path.extname(file)]||'application/octet-stream');res.setHeader('Cache-Control','no-store');res.end(bytes);}catch{res.writeHead(404);res.end('Not found');}
}).listen(port,'127.0.0.1',()=>console.log(`Preview: http://127.0.0.1:${port}`));
