import http from 'node:http';
import {readFile, realpath, stat} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
export const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.md':'text/plain; charset=utf-8'};
export function createServer(){return http.createServer(async(req,res)=>{
  try{
    if(!['GET','HEAD'].includes(req.method)){res.writeHead(405);res.end();return;}
    const pathname=decodeURIComponent((req.url||'/').split('?')[0]);
    if(pathname.includes('\0') || pathname.includes('\\') || pathname.split('/').includes('..'))throw Error('Forbidden');
    if(pathname==='/'){res.writeHead(302,{Location:'/v2/demos/'});res.end();return;}
    let target=path.resolve(root,'.'+pathname);
    if(!target.startsWith(root+path.sep))throw Error('Forbidden');
    if((await stat(target)).isDirectory())target=path.join(target,'index.html');
    target=await realpath(target);
    if(!target.startsWith(root+path.sep)||target.includes(path.sep+'node_modules'+path.sep))throw Error('Forbidden');
    res.writeHead(200,{'Content-Type':types[path.extname(target)]||'application/octet-stream','X-Content-Type-Options':'nosniff','Cache-Control':'no-store','Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"});
    res.end(req.method==='HEAD'?undefined:await readFile(target));
  }catch(e){res.writeHead(e.message==='Forbidden'?403:404,{'Content-Type':'text/plain'});res.end('Unavailable');}
});}
if(process.argv[1]===fileURLToPath(import.meta.url))createServer().listen(Number(process.env.PORT||4173),'127.0.0.1',()=>console.log('Awwwards V2: http://127.0.0.1:'+(process.env.PORT||4173)));
