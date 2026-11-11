import {createClient} from '@supabase/supabase-js';
import {createHash} from 'node:crypto';
import {HttpError,githubIdentity,githubUsername,requireCourse,requireOwner,checkPublishToken,validateAsset,validateSnapshot,COURSES} from './policy.mjs';

export function configuration(){return {url:process.env.SUPABASE_URL,key:process.env.SUPABASE_ANON_KEY,service:process.env.SUPABASE_SERVICE_ROLE_KEY,origin:process.env.APP_ORIGIN,publishHash:process.env.PUBLISH_TOKEN_SHA256};}
export function storeFor(config){
 const db=createClient(config.url,config.service,{auth:{persistSession:false,autoRefreshToken:false}});
 return {async call(op,payload){const {data,error}=await db.rpc('board_call',{op,payload});if(error){const message=String(error.message);if(/COURSE_LOCKED/.test(message))throw new HttpError(403,'课程已固定绑定或访问已停用；改绑请联系总监督。');if(/NOT_INVITED/.test(message))throw new HttpError(409,'选课状态刚发生变化，请刷新查看已绑定课程或重新选择。');if(/VERSION_CONFLICT|FILES_INCOMPLETE|IMMUTABLE_RELEASE/.test(message))throw new HttpError(409,'版本冲突或附件尚未全部验证，线上旧版本不变。');throw new HttpError(500,'云端数据操作失败，请查看管理员诊断。');}return data;},
 async user(jwt){const {data,error}=await db.auth.getUser(jwt);if(error||!data.user)throw new HttpError(401,'登录已失效，请重新登录。');return data.user;},
 async uploadUrl(path){const {data,error}=await db.storage.from('board-files').createSignedUploadUrl(path,{upsert:false});if(error)throw new HttpError(500,'无法创建附件上传通道。');return data;},
 async bytes(path){const {data,error}=await db.storage.from('board-files').download(path);if(error)throw new HttpError(409,'附件尚未上传。');return Buffer.from(await data.arrayBuffer());}};
}

export function createHandler(config=configuration(),providedStore){
 let cachedStore=providedStore;
 return async function handler(req,res){
  res.setHeader('Cache-Control','private, no-store');res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Referrer-Policy','no-referrer');
  const send=(status,body)=>{res.statusCode=status;res.setHeader('Content-Type','application/json; charset=utf-8');res.end(JSON.stringify(body));};
  try{
   const url=new URL(req.url,'http://local'),path=url.searchParams.get('route')||url.pathname.replace(/^\/api\/?/,'');
   if(path==='config'&&req.method==='GET')return send(200,{configured:!!(config.url&&config.key&&config.service&&config.origin),enrollmentMode:'self_service_once',supabaseUrl:config.url||null,anonKey:config.key||null});
   if(!config.url||!config.key||!config.service||!config.origin)throw new HttpError(503,'站点尚未完成云端配置；没有发布任何课程资料。');
   const origin=req.headers.origin;if(origin&&origin!==config.origin)throw new HttpError(403,'来源站点未获授权。');
   const store=cachedStore||(cachedStore=storeFor(config));
   let body={};if(req.method!=='GET'){
    if(req.body&&typeof req.body==='object'&&!Buffer.isBuffer(req.body)){if(Buffer.byteLength(JSON.stringify(req.body))>2000000)throw new HttpError(413,'请求过大。');body=req.body;}
    else {let raw=req.body?Buffer.from(req.body):Buffer.alloc(0);if(!req.body)for await(const chunk of req){raw=Buffer.concat([raw,chunk]);if(raw.length>2000000)throw new HttpError(413,'请求过大。');}try{body=raw.length?JSON.parse(raw):{};}catch{throw new HttpError(400,'请求不是有效 JSON。');}}
   }
   if(!body||typeof body!=='object'||Array.isArray(body))throw new HttpError(400,'请求必须是 JSON 对象。');
   let identity,gid,login,publisher=false;
   if(path.startsWith('publish/')&&checkPublishToken(req.headers['x-board-publish-token'],config.publishHash)){publisher=true;gid='local-publisher';}
   else{const token=(req.headers.authorization||'').replace(/^Bearer /,'');if(!token)throw new HttpError(401,'请先使用 GitHub 登录。');const user=await store.user(token);gid=githubIdentity(user);login=githubUsername(user,gid);identity=await store.call('identity',{github_id:gid});}
   if(path==='me'&&req.method==='GET'){
    const visible=identity.owner||!identity.membership?identity.courses:!identity.membership.disabled?identity.courses.filter(c=>c.id===identity.membership.course_id):[];
    return send(200,{githubId:gid,githubLogin:login,owner:identity.owner,membership:identity.membership,canSelectCourse:!identity.owner&&!identity.membership,courses:visible.filter(c=>COURSES.includes(c.id)).map(c=>({id:c.id,title:c.title}))});
   }
   if(path==='bind'&&req.method==='POST'){
    if(identity.owner)throw new HttpError(400,'总监督不需要绑定单门课程。');
    if(!COURSES.includes(body.course_id))throw new HttpError(400,'请选择有效课程。');
    if(identity.membership&&(identity.membership.disabled||identity.membership.course_id!==body.course_id))throw new HttpError(403,'课程已固定绑定或访问已停用；改绑请联系总监督。');
    // Self-enroll only the verified caller. The existing DB bind transaction still
    // serializes concurrent requests and can never overwrite an existing membership.
    // The legacy eligibility row also retains the verified GitHub login for admin display.
    if(!identity.membership)await store.call('invite',{github_id:gid,github_login:login,course_id:body.course_id,actor:gid});
    return send(200,await store.call('bind',{github_id:gid,course_id:body.course_id}));
   }
   if(path==='snapshot'&&req.method==='GET'){
    const cid=url.searchParams.get('course');requireCourse(identity,cid);
    return send(200,await store.call('snapshot',{course_id:cid}));
   }
   if(path==='asset'&&req.method==='GET'){
    const release=url.searchParams.get('release'),asset=url.searchParams.get('asset');
    if(!/^[a-f0-9-]{36}$/.test(release||'')||!/^[a-f0-9]{64}$/.test(asset||''))throw new HttpError(400,'附件编号无效。');
    const file=await store.call('get_asset',{release_id:release,asset_id:asset});
    if(!file||file.state!=='published'||!file.verified)throw new HttpError(404,'附件不可用。');
    requireCourse(identity,file.course_id);
    return send(200,{...file,authenticatedUrl:`${config.url}/storage/v1/object/authenticated/board-files/${file.course_id}/objects/${asset}`});
   }
   if(path.startsWith('admin/')){
    requireOwner(identity);
    if(path==='admin/members'&&req.method==='GET')return send(200,await store.call('admin_members',{}));
    if(path==='admin/invite'&&req.method==='POST'){
     if(!/^[A-Za-z0-9-]{1,39}$/.test(body.login||'')||!COURSES.includes(body.course_id))throw new HttpError(400,'GitHub 用户名或课程无效。');
     const response=await fetch(`https://api.github.com/users/${encodeURIComponent(body.login)}`,{headers:{Accept:'application/vnd.github+json','User-Agent':'CityU-Board'}});
     if(!response.ok)throw new HttpError(400,'无法核实此 GitHub 账号。');const user=await response.json();
     return send(200,await store.call('invite',{github_id:String(user.id),github_login:user.login,course_id:body.course_id,actor:gid}));
    }
    if(['admin/rebind','admin/revoke'].includes(path)&&req.method==='POST'){
     if(!/^\d+$/.test(body.github_id||''))throw new HttpError(400,'账号编号无效。');
     if(path==='admin/rebind'&&(!COURSES.includes(body.course_id)||typeof body.reason!=='string'||!body.reason.trim()))throw new HttpError(400,'改绑需要指定课程并填写原因。');
     return send(200,await store.call(path.split('/')[1],{...body,actor:gid}));
    }
    if(path==='admin/releases'&&req.method==='GET')return send(200,await store.call('releases',{course_id:url.searchParams.get('course')}));
    if(path==='admin/rollback'&&req.method==='POST')return send(200,await store.call('rollback',{...body,actor:gid}));
   }
   if(path.startsWith('publish/')){
    if(!publisher)requireOwner(identity);
    if(path==='publish/status'&&req.method==='GET'){const cid=url.searchParams.get('course');if(!COURSES.includes(cid))throw new HttpError(400,'课程无效。');const snapshot=await store.call('snapshot',{course_id:cid});return send(200,{active_release:snapshot?.id||null,published_at:snapshot?.published_at||null,content_hash:snapshot?.snapshot?.content_hash||null});}
    if(path==='publish/begin'&&req.method==='POST'){
     if(!COURSES.includes(body.course_id))throw new HttpError(400,'课程无效。');validateSnapshot(body.snapshot,body.course_id);
     if(!Number.isInteger(body.expected_count)||body.expected_count<0||body.expected_count>250)throw new HttpError(400,'附件数量无效。');
     if(body.expected_count!==new Set(body.snapshot.files.map(f=>f.id)).size)throw new HttpError(400,'附件数量与共享清单不一致。');
     return send(200,await store.call('begin_release',body));
    }
    if(path==='publish/asset'&&req.method==='POST'){
     validateAsset(body);if(!/^[a-f0-9-]{36}$/.test(body.release_id||''))throw new HttpError(400,'版本编号无效。');
     const {course_id,reused}=await store.call('add_asset',body);const target=`${course_id}/objects/${body.asset_id}`;
     return send(200,reused?{target,reused:true}:{target,reused:false,...await store.uploadUrl(target)});
    }
    if(path==='publish/verify'&&req.method==='POST'){
     const a=await store.call('get_asset',body);if(!a||a.state!=='draft')throw new HttpError(409,'附件不是待发布版本。');
     const bytes=await store.bytes(`${a.course_id}/objects/${body.asset_id}`);
     if(bytes.length!==Number(a.bytes)||createHash('sha256').update(bytes).digest('hex')!==a.sha256)throw new HttpError(409,'附件字节或哈希与清单不符。');
     return send(200,await store.call('verified_asset',body));
    }
    if(path==='publish/commit'&&req.method==='POST')return send(200,await store.call('publish',{...body,actor:gid}));
   }
   throw new HttpError(404,'接口不存在。');
  }catch(error){return send(error.status||500,{error:error.status?error.message:'服务暂不可用，请稍后重试。'});}
 };
}
