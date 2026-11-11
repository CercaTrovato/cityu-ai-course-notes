import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {promisify} from 'node:util';
import {execFile} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {validateSnapshot} from '../server/policy.mjs';
const exec=promisify(execFile),sha=b=>createHash('sha256').update(b).digest('hex');
const mime={'.md':'text/markdown','.txt':'text/plain','.py':'text/plain','.js':'text/plain','.mjs':'text/plain','.sql':'text/plain','.json':'application/json','.csv':'text/csv','.pdf':'application/pdf','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.docx':'application/octet-stream','.pptx':'application/octet-stream','.xlsx':'application/octet-stream','.zip':'application/octet-stream'};
const privateKeys=new Set(['root','metadata_path','thread_id','root_thread_id','report_path','answer_source','review_note','model','age_minutes']);
const uuid=/\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/gi;
export function sharedText(s){return s.replace(/(?:codex|plugin|file):\/\/[^\s)\]<>"']+/gi,'[本地入口]').replace(/\b[A-Z]:[\\/][^\r\n)\]<>"'，；]+/gi,'[本地资料]').replace(uuid,'[内部记录]').replaceAll('你的','总监督的').replaceAll('你 ·','总监督 ·').replaceAll('你参与','总监督参与').replaceAll('本人','总监督');}
function clean(v){if(typeof v==='string')return sharedText(v).replaceAll('你','总监督');if(Array.isArray(v))return v.map(clean);if(v&&typeof v==='object')return Object.fromEntries(Object.entries(v).filter(([k])=>!privateKeys.has(k)).map(([k,x])=>[k,clean(x)]));return v;}
function scan(bytes,label){const t=bytes.toString('utf8');if(/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:ghp_|github_pat_|sb_secret_|sk-)[A-Za-z0-9_-]{16,}|Bearer\s+[A-Za-z0-9._-]{20,}/i.test(t))throw Error('发现疑似凭据，停止导出：'+label);}
function within(file,root){const p=path.relative(root,file);return p===''||(!p.startsWith('..'+path.sep)&&p!=='..'&&!path.isAbsolute(p));}
export async function buildCourse(record,policy,{cacheDir}){
 if(record.course!==policy.course||record.id!==policy.assignment_id||record.assignment_type!=='group')throw Error('课程与发布清单不匹配');
 const root=await fs.realpath(policy.root),allowedRoots=await Promise.all([policy.root,...(policy.allowed_roots||[])].map(r=>fs.realpath(r))),assets=new Map(),entries=new Map(),filesByPath=new Map(),warnings=[];
 let thinkingRaw=null,thinkingBytes=null,thinkingPath=null;
 if(policy.thinking_file){thinkingPath=await fs.realpath(policy.thinking_file);if(!within(thinkingPath,root))throw Error('思路元数据不属于本课程');thinkingBytes=await fs.readFile(thinkingPath);thinkingRaw=JSON.parse(thinkingBytes);if(thinkingRaw.assignment_id!==record.id)throw Error('思路元数据与课程不一致');}
 let timelineBytes=null;
 if(policy.timeline_file){timelineBytes=await fs.readFile(policy.timeline_file);if(!record.timeline||record.timeline.error||sha(timelineBytes)!==record.timeline.revision)throw Error('时间线在读取后已变化或无效，请重新导出');}
 const descriptors=[];
 for(const item of policy.files){
  const original=path.resolve(root,item.path),real=await fs.realpath(original);
  if(!allowedRoots.some(r=>within(real,r)))throw Error('共享文件超出获准课程目录：'+item.path);
  if(!mime[path.extname(real).toLowerCase()])throw Error('不支持的共享文件类型：'+item.path);
  const bytes=await fs.readFile(real);if(bytes.length>50*1024*1024)throw Error('单文件超过 50 MiB：'+item.path);
  descriptors.push({item,real,bytes,sourceHash:sha(bytes),alias:'shared-file-'+sha(real.toLowerCase()).slice(0,20),references:{}});
 }
 async function register(name,bytes,type){scan(bytes,name);const id=sha(bytes);assets.set(id,{asset_id:id,sha256:id,bytes:bytes.length,name,mime:type,buffer:bytes});if(!entries.has(id))entries.set(id,{id,name,bytes:bytes.length,mime:type});return id;}
 for(const d of descriptors){
  const ext=path.extname(d.real).toLowerCase(),type=mime[ext];
  let bytes=d.bytes,name=d.item.name||path.basename(d.real);
  if(d.item.shared_copy){if(!type.startsWith('text/')&&type!=='application/json')throw Error('共享副本仅适用于文字文件');let content=bytes.toString('utf8');if(type==='text/markdown')content=content.replace(/(!?\[[^\]]*\]\()([^\s)]+)([^)]*\))/g,(all,begin,href,end)=>{if(/^https?:\/\//i.test(href)||href.startsWith('#'))return all;let target;try{target=path.resolve(path.dirname(d.real),decodeURIComponent(href.split('#')[0]));}catch{return all;}const linked=descriptors.find(x=>x.real.toLowerCase()===target.toLowerCase());if(!linked)return all;d.references[linked.alias]=linked;return begin+linked.alias+end;});bytes=Buffer.from(sharedText(content));name=path.basename(name,ext)+'-shared'+ext;}
  d.id=await register(name,bytes,type);filesByPath.set(d.real.toLowerCase(),d.id);
  const entry=entries.get(d.id);entry.source_sha256=d.sourceHash;entry.shared_copy=!!d.item.shared_copy;
  entry.title=sharedText(d.item.label||(type==='text/markdown'?bytes.toString('utf8').match(/^#\s+(.+)$/m)?.[1]:'')||name).slice(0,140);
  if(ext==='.docx'||ext==='.pptx'){
   let pdf;
   if(d.item.preview){const real=await fs.realpath(path.resolve(root,d.item.preview));if(!allowedRoots.some(r=>within(real,r)))throw Error('预览超出课程范围');pdf=await fs.readFile(real);}
   else{
    const dest=path.join(cacheDir,'previews',d.sourceHash+'.pdf');await fs.mkdir(path.dirname(dest),{recursive:true});
    try{pdf=await fs.readFile(dest);}catch(e){if(e.code!=='ENOENT')throw e;const script=fileURLToPath(new URL('./office-preview.ps1',import.meta.url));await exec('powershell.exe',['-NoProfile','-File',script,'-Source',d.real,'-Destination',dest],{timeout:90000,windowsHide:true,maxBuffer:100000});pdf=await fs.readFile(dest);}
   }
   if(!pdf.subarray(0,5).equals(Buffer.from('%PDF-')))throw Error('Office 预览没有生成有效 PDF');
   entry.preview_id=await register(path.basename(name,ext)+'-preview.pdf',pdf,'application/pdf');
  }
 }
 // Only references to explicitly listed files become links. Never follow links recursively.
 for(const d of descriptors){if(path.extname(d.real).toLowerCase()!=='.md')continue;const links=Object.fromEntries(Object.entries(d.references).map(([alias,target])=>[alias,target.id]));for(const match of d.bytes.toString('utf8').matchAll(/!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)/g)){const href=match[1];if(/^[a-z]+:/i.test(href)||href.startsWith('#'))continue;let target;try{target=path.resolve(path.dirname(d.real),decodeURIComponent(href.split('#')[0]));}catch{continue;}const id=filesByPath.get(target.toLowerCase());if(id)links[href]=id;else warnings.push('未共享引用：'+path.basename(d.real)+' → '+href);}entries.get(d.id).links=links;}
 const recordCopy=clean(record);recordCopy.sources=(record.sources||[]).map(s=>{
  const out={id:s.id,label:sharedText(s.label),observed_at:s.observed_at,sha256:s.sha256,assignment_id:record.id};
  const descriptor=descriptors.find(d=>d.item.source_ids?.includes(s.id));
  if(descriptor)return {...out,kind:'shared',asset_id:descriptor.id};
  if(s.kind==='web'&&/^https:\/\//.test(s.locator))return {...out,kind:'web',locator:s.locator};
  return {...out,kind:'record',label:out.label+'（依据记录，未共享原件）'};
 });
 if(recordCopy.coordination){recordCopy.coordination.report_exists=false;recordCopy.coordination.title='课程监督记录';}
 const snapshot={schema_version:1,course:record.course,assignments:[recordCopy],files:[...entries.values()]};
 if(thinkingRaw){
  const thinking=clean(thinkingRaw);thinking.publication='published_snapshot';thinking.revision=sha(thinkingBytes);thinking.warnings=[];
  thinking.latest_progress=record.revision!==thinking.assignment_revision?recordCopy.summary:'';
  if(thinking.latest_progress)thinking.warnings.push('课程进度台账已有新版本；思路解析保留已核内容，新进展在下方单独列出。');
  thinking.sources=thinkingRaw.sources.map(s=>{const descriptor=descriptors.find(d=>d.real.toLowerCase()===path.resolve(s.path).toLowerCase());if(!descriptor)throw Error('思路引用尚未加入共享白名单：'+s.title);const changed=s.sha256!==descriptor.sourceHash;if(changed)thinking.warnings.push(sharedText(s.title)+' 已更新，节点解释需复核。');return {id:s.id,title:sharedText(s.title),sha256:s.sha256,current_sha256:descriptor.sourceHash,changed,available:true,asset_id:descriptor.id};});
  snapshot.thinking=thinking;
 }
 snapshot.content_hash=sha(JSON.stringify(snapshot));validateSnapshot(snapshot,record.course);
 const total=[...assets.values()].reduce((n,a)=>n+a.bytes,0);if(total>(policy.max_total_bytes||150*1024*1024))throw Error('本课程共享资料超过容量预算');
 // Re-read source hashes after conversion: a concurrent edit aborts the course export.
 for(const d of descriptors)if(sha(await fs.readFile(d.real))!==d.sourceHash)throw Error('导出期间文件发生变化，请重新同步：'+d.item.path);
 if(thinkingPath&&sha(await fs.readFile(thinkingPath))!==sha(thinkingBytes))throw Error('导出期间思路元数据发生变化，请重新同步');
 if(policy.timeline_file&&sha(await fs.readFile(policy.timeline_file))!==sha(timelineBytes))throw Error('导出期间时间线发生变化');
 return {snapshot,assets:[...assets.values()],warnings:[...new Set(warnings)],total};
}
