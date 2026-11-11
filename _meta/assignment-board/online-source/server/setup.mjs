// Local-only setup assistant. This module is never mounted by api/index.js.
import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import {randomBytes,createHash} from 'node:crypto';
import {spawn} from 'node:child_process';
const nonce=process.env.BOARD_SETUP_NONCE||randomBytes(24).toString('hex'),port=8771,origin=`http://127.0.0.1:${port}`;
await fs.mkdir('.local',{recursive:true});
const seal=value=>new Promise((resolve,reject)=>{const p=spawn('D:/anaconda3/python.exe',['-X','utf8','scripts/windows-secrets.py','seal'],{windowsHide:true});let out='';p.stdout.on('data',b=>out+=b);p.on('error',()=>reject(Error('无法启动本机加密程序')));p.on('close',c=>c?reject(Error('本机加密失败')):resolve(out.trim()));p.stdin.end(value);});
const server=http.createServer(async(req,res)=>{
 res.setHeader('Cache-Control','no-store');res.setHeader('X-Frame-Options','DENY');
 try{
  const u=new URL(req.url,origin);if(u.pathname!==`/${nonce}`){res.writeHead(404);return res.end();}
  if(req.method==='POST'){
   if(req.headers.origin!==origin||!req.headers['content-type']?.startsWith('application/json')){res.writeHead(403);return res.end();}
   let raw='';for await(const b of req){raw+=b;if(raw.length>20000)throw Error('请求过大');}
   const data=JSON.parse(raw);if(!data.service||!data.anon)throw Error('请填入本项目的两项 API key');
   const url='https://fryjlczmxyjqdphkizzo.supabase.co';
   const check=await fetch(url+'/rest/v1/rpc/board_call',{method:'POST',headers:{apikey:data.service,Authorization:'Bearer '+data.service,'Content-Type':'application/json'},body:JSON.stringify({op:'identity',payload:{github_id:'130777537'}})});
   if(!check.ok)throw Error('密钥验证失败或数据库结构尚未初始化；请核对项目与密钥。');
   const token=randomBytes(32).toString('hex'),config={SUPABASE_URL:url,SUPABASE_ANON_KEY:data.anon,SUPABASE_SERVICE_ROLE_KEY:data.service,APP_ORIGIN:data.origin,PUBLISH_TOKEN_SHA256:createHash('sha256').update(token).digest('hex')};
   await fs.writeFile('.local/cloud.dpapi',await seal(JSON.stringify(config)));await fs.writeFile('.local/publish-token.dpapi',await seal(token));
   res.setHeader('Content-Type','application/json');return res.end(JSON.stringify({ok:true,message:'已验证并加密保存在本机。可以关闭这个页面。'}));
  }
  const sql=await fs.readFile('supabase/migrations/001_board.sql','utf8');
  res.setHeader('Content-Type','text/html;charset=utf-8');
  res.end(`<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>CityU 线上看板 · 本机配置</title><style>body{font:16px system-ui;max-width:900px;margin:40px auto;padding:20px;background:#f5f7f6;color:#233d32}input,textarea,button{font:inherit;box-sizing:border-box;width:100%;padding:12px;margin:8px 0}textarea{height:240px}button{cursor:pointer;background:#14543e;color:white;border:0;border-radius:6px}label{display:block;margin-top:22px}small{line-height:1.8}#result{white-space:pre-wrap}</style><h1>线上看板的一次性配置</h1><p>此页面仅运行在本机。课程资料还没有上传。</p><details><summary>数据库初始化 SQL</summary><textarea id="sql" readonly>${sql.replaceAll('&','&amp;').replaceAll('<','&lt;')}</textarea><button id="copy">复制 SQL</button></details><h2>连接已创建的 Supabase 项目</h2><p>项目：<b>cityu-board-online</b> · fryjlczmxyjqdphkizzo</p><p>下面两项从 Supabase 项目 API Keys 页面复制。服务端密钥将以 Windows DPAPI 加密保存在本机，并仅配置到 Vercel 后端；不会进入网页源码或 Git。</p><form><label>线上看板地址<input id="origin" value="https://cityu-board-online-cercatrovato-5991s-projects.vercel.app" required></label><label>anon / publishable key<input id="anon" type="password" required autocomplete="off"></label><label>service_role / secret key<input id="service" type="password" required autocomplete="off"></label><button>验证并加密保存</button></form><p id="result"></p><script>document.getElementById('copy').onclick=()=>navigator.clipboard.writeText(document.getElementById('sql').value);document.querySelector('form').onsubmit=async e=>{e.preventDefault();const b=e.target.querySelector('button');b.disabled=true;const r=await fetch(location.href,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({origin:document.getElementById('origin').value,anon:document.getElementById('anon').value,service:document.getElementById('service').value})});const d=await r.json();document.getElementById('result').textContent=d.message||d.error;if(d.ok){document.getElementById('anon').value='';document.getElementById('service').value='';}b.disabled=false;}</script></html>`);
 }catch(e){res.statusCode=400;res.setHeader('Content-Type','application/json');res.end(JSON.stringify({error:e.message}));}
});
server.listen(port,'127.0.0.1',()=>console.log(origin+'/'+nonce));
