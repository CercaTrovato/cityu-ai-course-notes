import {createHash,timingSafeEqual} from 'node:crypto';
export const COURSES=['AC6761','IS6400','IS5113','IS5542','EF5560'];
export class HttpError extends Error{constructor(status,message){super(message);this.status=status;}}
export function githubIdentity(user){
 const ids=(user?.identities||[]).filter(i=>i.provider==='github').map(i=>String(i.identity_data?.provider_id??i.identity_data?.sub??'')).filter(x=>/^\d+$/.test(x));
 if(ids.length!==1)throw new HttpError(403,'请使用 GitHub 账号登录。');return ids[0];
}
export function githubUsername(user,id){
 const profile=(user?.identities||[]).find(i=>i.provider==='github')?.identity_data||{};
 const name=profile.user_name||profile.preferred_username||profile.login;
 return typeof name==='string'&&/^[A-Za-z0-9-]{1,39}$/.test(name)?name:'GitHub-'+id;
}
export function canRead(identity,course){return Boolean(identity.owner||identity.membership&&!identity.membership.disabled&&identity.membership.course_id===course);}
export function requireCourse(identity,course){if(!COURSES.includes(course)||!canRead(identity,course))throw new HttpError(403,'你没有这个课程的访问权限。');}
export function requireOwner(identity){if(!identity.owner)throw new HttpError(403,'此操作仅限总监督。');}
export function checkPublishToken(token,hash){if(!token||!hash||!/^[a-f0-9]{64}$/.test(hash))return false;const got=createHash('sha256').update(token).digest();return timingSafeEqual(got,Buffer.from(hash,'hex'));}
export function validateAsset(a){
 if(!a||!/^[a-f0-9]{64}$/.test(a.asset_id)||a.asset_id!==a.sha256||!Number.isSafeInteger(a.bytes)||a.bytes<0||a.bytes>50*1024*1024)throw new HttpError(400,'附件清单无效。');
 if(typeof a.name!=='string'||a.name.length>220||/[\x00-\x1f\/\\]/.test(a.name))throw new HttpError(400,'附件名称无效。');
 const allowed=['text/markdown','text/plain','text/csv','application/json','application/pdf','image/png','image/jpeg','image/webp','application/octet-stream'];
 if(!allowed.includes(a.mime))throw new HttpError(400,'不支持的附件类型。');
}
export function validateSnapshot(snapshot,course){
 if(!snapshot||snapshot.schema_version!==1||snapshot.course!==course||!Array.isArray(snapshot.assignments)||snapshot.assignments.length!==1)throw new HttpError(400,'课程发布包结构无效。');
 if(snapshot.assignments.some(r=>r.course!==course||r.assignment_type!=='group'))throw new HttpError(400,'发布包包含跨课程或个人作业。');
 for(const r of snapshot.assignments){const t=r.timeline;if(t&&(t.error||t.schema_version!==1||t.course!==course||t.assignment_id!==r.id||!Array.isArray(t.items)))throw new HttpError(400,'时间线归属或结构无效。');}
 if(!Array.isArray(snapshot.files)||snapshot.files.length>250)throw new HttpError(400,'附件索引无效。');
 const ids=new Set(snapshot.files.map(f=>f.id));
 for(const f of snapshot.files){validateAsset({asset_id:f.id,sha256:f.id,bytes:f.bytes,name:f.name,mime:f.mime});if((f.preview_id&&!ids.has(f.preview_id))||Object.values(f.links||{}).some(id=>!ids.has(id)))throw new HttpError(400,'附件预览或引用不完整。');}
 for(const s of snapshot.assignments[0].sources||[]){if(s.asset_id&&!ids.has(s.asset_id))throw new HttpError(400,'来源附件未登记。');}
 if(snapshot.thinking){
  const t=snapshot.thinking;
  if(t.schema_version!==1||t.assignment_id!==snapshot.assignments[0].id||t.publication!=='published_snapshot'||!Array.isArray(t.sources)||!Array.isArray(t.nodes)||!Array.isArray(t.edges))throw new HttpError(400,'思路解析归属或结构无效。');
  const sources=new Set(t.sources.map(s=>s.id)),nodes=new Set(t.nodes.map(n=>n.id));
  if(sources.size!==t.sources.length||nodes.size!==t.nodes.length||!sources.has(t.primary_source)||!nodes.size)throw new HttpError(400,'思路节点或来源编号无效。');
  if(t.sources.some(s=>!ids.has(s.asset_id))||t.nodes.some(n=>!Array.isArray(n.evidence)||n.evidence.some(id=>!sources.has(id)))||t.edges.some(e=>!nodes.has(e.from)||!nodes.has(e.to)))throw new HttpError(400,'思路引用未纳入本课程共享版本。');
 }
 const text=JSON.stringify(snapshot);if(text.length>1500000)throw new HttpError(413,'快照过大。');
 if(/\b[A-Z]:[\\/]/i.test(text)||/codex:\/\/|plugin:\/\/|file:\/\/|bearer\s+[a-z0-9._-]{12,}|(?:sk-|ghp_)[a-z0-9_-]{16,}/i.test(text))throw new HttpError(400,'发布包含本机路径、内部入口或疑似凭据。');
 const walk=v=>{if(Array.isArray(v))v.forEach(walk);else if(v&&typeof v==='object'){for(const [k,x]of Object.entries(v)){if(['root','metadata_path','thread_id','root_thread_id','answer_source','review_note','path','report_path'].includes(k))throw new HttpError(400,'发布包含内部字段。');walk(x);}}};walk(snapshot);
}
