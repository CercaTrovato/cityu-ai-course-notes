import {createClient} from '@supabase/supabase-js';
import {marked} from 'marked';
import DOMPurify from 'dompurify';
import Papa from 'papaparse';
import {createThinkingBridge} from './thinking-bridge.mjs';
import {createCourseSelection} from './course-selection.mjs';
import {getDocument,GlobalWorkerOptions} from 'pdfjs-dist';
GlobalWorkerOptions.workerSrc='/assets/pdf.worker.min.mjs';
DOMPurify.addHook('afterSanitizeAttributes',node=>{if(node.tagName==='IMG'){const src=node.getAttribute('src');if(src)node.setAttribute('data-shared-src',src);node.removeAttribute('src');node.removeAttribute('srcset');}});
let auth,session,me,config,release=null,cached=null,cachedAt=0,ownerCourse=null,objectUrls=[];
const thinkingVersions=new Map();
const $=id=>document.getElementById(id);
const text=(tag,content)=>{const el=document.createElement(tag);el.textContent=content;return el;};
function screen(message){thinkingVersions.clear();$('workspace').hidden=true;$('auth-screen').hidden=false;$('auth-message').textContent=message;$('file-panel').hidden=true;clearViewer();$('detail').close();$('detail-content').replaceChildren();$('admin').close();$('admin-content').replaceChildren();}
async function api(path,body){const {data}=await auth.auth.getSession();session=data.session;if(!session){cached=null;release=null;me=null;window.resetBoard?.();screen('登录已失效，请重新登录。');$('login').hidden=false;throw Object.assign(Error('请重新登录'),{status:401});}const r=await fetch('/api/'+path,{method:body?'POST':'GET',headers:{Authorization:'Bearer '+session.access_token,...(body?{'Content-Type':'application/json'}:{})},body:body?JSON.stringify(body):undefined,cache:'no-store'});const result=await r.json();if(!r.ok){if(r.status===401||r.status===403){cached=null;release=null;window.resetBoard?.();screen(result.error);if(r.status===401){me=null;$('login').hidden=false;}$('auth-options').replaceChildren();if(r.status===403)$('auth-options').append(text('p','刷新页面可读取当前课程；改绑或恢复访问请联系总监督。'));}throw Object.assign(Error(result.error||'请求失败'),{status:r.status});}return result;}
function clearViewer(){for(const u of objectUrls)URL.revokeObjectURL(u);objectUrls=[];$('file-body').replaceChildren();}
async function download(id,version=release){const a=await api('asset?release='+version.id+'&asset='+id);const {data}=await auth.auth.getSession();const r=await fetch(a.authenticatedUrl,{headers:{Authorization:'Bearer '+data.session.access_token,apikey:config.anonKey},cache:'no-store'});if(!r.ok)throw Error('文件权限已变更或文件不可用。');return {a,blob:await r.blob()};}
async function preview(id){
 clearViewer();$('file-panel').hidden=false;$('file-download').hidden=false;$('file-title').textContent='读取资料…';$('file-note').textContent='';
 try{
  const entry=release.snapshot.files.find(f=>f.id===id);if(!entry)throw Error('此版本没有登记该文件。');
  $('file-title').textContent=entry.title||entry.name;$('file-download').textContent=entry.shared_copy?'下载共享副本':'下载原件';$('file-note').textContent=entry.name+' · '+new Date(release.published_at).toLocaleString('zh-CN',{timeZone:'Asia/Shanghai'})+(entry.shared_copy?' · 隐去本机入口的共享副本':'');
  $('file-download').onclick=async()=>{try{const {blob}=await download(entry.id);const u=URL.createObjectURL(blob);objectUrls.push(u);const a=document.createElement('a');a.href=u;a.download=entry.name;a.click();}catch(e){$('file-body').prepend(text('p',e.message));}};
  const display=entry.preview_id||entry.id;const result=await download(display);const mime=result.a.mime;
  if(mime==='application/pdf'){
   const doc=await getDocument({data:new Uint8Array(await result.blob.arrayBuffer()),isEvalSupported:false}).promise;let page=1,scale=1;
   const controls=document.createElement('div');controls.className='reader-controls';const prev=text('button','上一页'),next=text('button','下一页'),count=text('span',''),zoom=document.createElement('select'),search=document.createElement('input'),find=text('button','查找');
   for(const val of [.75,1,1.25,1.5]){const op=text('option',Math.round(val*100)+'%');op.value=val;op.selected=val===1;zoom.append(op);}search.placeholder='在 PDF 中查找';search.setAttribute('aria-label','在PDF中查找');
   controls.append(prev,count,next,zoom,search,find);const canvas=document.createElement('canvas');$('file-body').append(controls,canvas);
   let rendering=false;async function draw(){if(rendering)return;rendering=true;try{const p=await doc.getPage(page),v=p.getViewport({scale});canvas.width=v.width;canvas.height=v.height;await p.render({canvasContext:canvas.getContext('2d'),viewport:v}).promise;count.textContent=`${page} / ${doc.numPages}`;prev.disabled=page===1;next.disabled=page===doc.numPages;}finally{rendering=false;}}
   prev.onclick=()=>{if(!rendering&&page>1){page--;draw();}};next.onclick=()=>{if(!rendering&&page<doc.numPages){page++;draw();}};zoom.onchange=()=>{scale=Number(zoom.value);draw();};find.onclick=async()=>{const q=search.value.trim().toLowerCase();if(!q)return;find.disabled=true;try{for(let offset=1;offset<=doc.numPages;offset++){const i=(page+offset-1)%doc.numPages+1;const p=await doc.getPage(i);const t=await p.getTextContent();if(t.items.map(x=>x.str).join(' ').toLowerCase().includes(q)){page=i;await draw();return;}}count.textContent='没有找到该文字';}finally{find.disabled=false;}};await draw();
  }else if(mime.startsWith('image/')){const u=URL.createObjectURL(result.blob);objectUrls.push(u);const img=document.createElement('img');img.src=u;img.alt=entry.name;img.className='file-image';img.onclick=()=>img.classList.toggle('actual-size');$('file-body').append(img);}
  else if(mime==='text/markdown'){
   const html=DOMPurify.sanitize(marked.parse(await result.blob.text()),{FORBID_TAGS:['style','iframe','form','video','audio','source','svg','math','object','embed','link','base','meta'],FORBID_ATTR:['style','srcset'],SANITIZE_NAMED_PROPS:true});const section=document.createElement('article');section.className='markdown';section.innerHTML=html;
   section.querySelectorAll('a').forEach(a=>{const href=a.getAttribute('href');const target=entry.links?.[href];if(target){a.href='#';a.onclick=e=>{e.preventDefault();preview(target);};}else if(/^https:\/\//.test(href||'')){a.target='_blank';a.rel='noopener noreferrer';}else if(!(href||'').startsWith('#')){a.removeAttribute('href');a.title='该引用未纳入本次共享';}});
   for(const img of section.querySelectorAll('img')){const source=entry.links?.[img.getAttribute('data-shared-src')];if(!source){img.replaceWith(text('span','[图片未纳入本次共享]'));continue;}const {blob}=await download(source);const u=URL.createObjectURL(blob);objectUrls.push(u);img.src=u;}
   $('file-body').append(section);
  }else if(mime==='text/csv'){
   const parsed=Papa.parse(await result.blob.text(),{header:true,preview:500,skipEmptyLines:true});$('file-body').append(text('p','预览最多 500 行；下载可取得完整原件。'));
   const filter=document.createElement('input');filter.placeholder='筛选预览行';filter.setAttribute('aria-label','筛选表格');const table=document.createElement('table'),wrap=document.createElement('div');wrap.className='csv-scroll';wrap.append(table);$('file-body').append(filter,wrap);
   function draw(){table.replaceChildren();const tr=document.createElement('tr');for(const c of parsed.meta.fields||[])tr.append(text('th',c));table.append(tr);for(const row of parsed.data.filter(r=>JSON.stringify(r).toLowerCase().includes(filter.value.toLowerCase()))){const line=document.createElement('tr');for(const c of parsed.meta.fields||[])line.append(text('td',String(row[c]??'')));table.append(line);}}filter.oninput=draw;draw();
  }else if(mime.startsWith('text/')||mime==='application/json'){$('file-body').append(text('pre',await result.blob.text()));}
  else {$('file-body').append(text('p','该文件保留原件供下载，本版本未提供浏览器预览。'));}
 }catch(e){$('file-body').replaceChildren(text('p',e.message));}
}
async function initialize(){
 const response=await fetch('/api/config');config=await response.json();
 if(!config.configured){screen('线上服务正在配置。当前没有向访客公开任何课程资料。');$('login').disabled=true;return;}
 auth=createClient(config.supabaseUrl,config.anonKey,{auth:{flowType:'pkce',persistSession:true,autoRefreshToken:true,detectSessionInUrl:false}});
 const code=new URL(location.href).searchParams.get('code');if(code){const {error}=await auth.auth.exchangeCodeForSession(code);history.replaceState({},'',location.pathname);if(error){screen('登录回调已失效，请重试。');}}
 $('login').onclick=()=>auth.auth.signInWithOAuth({provider:'github',options:{redirectTo:location.origin,scopes:'read:user user:email'}});
 $('logout').onclick=async()=>{await auth.auth.signOut();cached=null;release=null;me=null;window.resetBoard?.();clearViewer();screen('已退出登录。');$('account').replaceChildren();$('auth-options').replaceChildren();$('login').hidden=false;};
 const {data}=await auth.auth.getSession();if(!data.session){screen('使用 GitHub 登录，首次选择一门课程后即可进入。选定后课程固定，后续改绑由总监督处理。');return;}
 try{
  me=await api('me');$('account').textContent=me.owner?'总监督':(me.githubLogin||'GitHub 账号已登录');$('logout').hidden=false;$('login').hidden=true;
  if(!me.owner&&!me.membership){
   screen('登录成功。选择你所属的一门课程，确认后立即进入，无需等待邀请或审批。');
   $('auth-options').replaceChildren(createCourseSelection(me.courses,async course_id=>{try{await api('bind',{course_id});location.reload();}catch(error){if([403,409].includes(error.status)){const current=await api('me');if(current.membership){location.reload();return;}}throw error;}}));return;
  }
  if(me.membership?.disabled){screen('本账号的课程访问已停用，请联系总监督。');return;}
  $('auth-screen').hidden=true;$('workspace').hidden=false;
  const library=text('button','课程资料库');library.className='quiet-button';library.onclick=showLibrary;$('account-actions').prepend(library);
  if(me.owner){const button=text('button','成员与版本管理');button.className='quiet-button';button.onclick=admin;$('account-actions').prepend(button);}
  window.boardRefresh?.();
 }catch(e){screen(e.message);}
}
async function snapshots(){
 if(!auth||!me||$('workspace').hidden)return null;
 if(cached&&Date.now()-cachedAt<25000)return cached;
 const ids=me.courses.map(c=>c.id),records=[];let latest=null;
 for(const id of ids){const r=await api('snapshot?course='+encodeURIComponent(id));thinkingVersions.set(id,{value:r,at:Date.now()});if(r){records.push(...r.snapshot.assignments.map(a=>({...a,_onlineRelease:r.id,_onlinePublishedAt:r.published_at})));if(!latest||r.published_at>latest)latest=r.published_at;}}
 cached={assignments:records,errors:[],missing:[],generated_at:new Date().toISOString()};cachedAt=Date.now();
 $('sync-status').textContent=latest?'线上资料发布于 '+new Date(latest).toLocaleString('zh-CN',{timeZone:'Asia/Shanghai'}):'尚未发布课程资料';
 return cached;
}
async function previewSource(id,assignmentId){$('detail').close();const course=assignmentId.split('-')[0];release=await api('snapshot?course='+course);await preview(id);}
async function showLibrary(){
 clearViewer();$('file-panel').hidden=false;$('file-title').textContent='课程资料库';$('file-note').textContent='仅显示最近成功同步的共享资料';$('file-download').hidden=true;
 for(const c of me.courses){const r=await api('snapshot?course='+c.id);$('file-body').append(text('h3',c.id+' · '+c.title));if(!r){$('file-body').append(text('p','该课程尚未同步资料。'));continue;}const previews=new Set(r.snapshot.files.map(f=>f.preview_id).filter(Boolean));for(const f of r.snapshot.files.filter(f=>!previews.has(f.id))){const b=text('button',f.title||f.name);b.append(text('small',f.name+(f.shared_copy?' · 共享副本':'')));b.className='library-file';b.onclick=()=>{release=r;$('file-download').hidden=false;preview(f.id);};$('file-body').append(b);}}
}
async function admin(){
 $('admin').showModal();$('admin-content').replaceChildren(text('h2','成员与课程绑定'));
 const list=await api('admin/members'),course=document.createElement('select');
 for(const c of me.courses){const o=text('option',c.id+' · '+c.title);o.value=c.id;course.append(o);}$('admin-content').append(text('p','组员首次登录后自行选择一门课，无需邀请。你在这里处理改绑或停用；其他人不能自行更改所属课程。'));if(!list.members.length)$('admin-content').append(text('p','还没有成员完成选课。把看板链接发给组员即可，绑定后会出现在这里。'));
 for(const member of list.members){const line=document.createElement('div');line.className='member-row';const name=list.invites.find(x=>x.github_id===member.github_id)?.github_login||member.github_id;line.append(text('b',name+' · '+member.course_id+(member.disabled?'（已停用）':'')));const select=course.cloneNode(true);select.value=member.course_id;const reason=document.createElement('input');reason.placeholder='改绑原因';const rebind=text('button','由我批准改绑'),revoke=text('button','停用访问');rebind.onclick=async()=>{try{await api('admin/rebind',{github_id:member.github_id,course_id:select.value,reason:reason.value});await admin();}catch(e){alert(e.message);}};revoke.onclick=async()=>{if(confirm('停止该成员访问课程？')){await api('admin/revoke',{github_id:member.github_id});await admin();}};line.append(select,reason,rebind,revoke);$('admin-content').append(line);}
 $('admin-content').append(text('h3','版本回退'));
 const pick=course.cloneNode(true),versions=document.createElement('select'),load=text('button','读取版本'),rollback=text('button','切换到所选版本');load.onclick=async()=>{versions.replaceChildren();for(const r of await api('admin/releases?course='+pick.value)){const o=text('option',r.published_at+' · '+r.id.slice(0,8));o.value=r.id;versions.append(o);}};rollback.onclick=async()=>{if(versions.value&&confirm('把此课程切换到选定的历史版本？')){await api('admin/rollback',{course_id:pick.value,release_id:versions.value});cached=null;window.boardRefresh?.();}};$('admin-content').append(pick,load,versions,rollback);
}
const thinking=createThinkingBridge({
 async getSnapshot(course){
  if(!me?.courses.some(c=>c.id===course)||$('workspace').hidden)throw Error('请登录并确认课程权限。');
  const saved=thinkingVersions.get(course);if(saved&&Date.now()-saved.at<25000)return saved.value;
  const value=await api('snapshot?course='+course);thinkingVersions.set(course,{value,at:Date.now()});return value;
 },
 async readSource({release:version,source,entry,thinking:story,assignmentId}){
  const {a,blob}=await download(entry.id,version),content=await blob.text();let rows=null,html='',kind='.'+entry.name.split('.').pop().toLowerCase();
  const section=document.createElement('article');
  if(a.mime==='text/markdown'){
   section.innerHTML=DOMPurify.sanitize(marked.parse(content),{ALLOW_DATA_ATTR:false,FORBID_TAGS:['style','iframe','form','video','audio','source','svg','math','object','embed','link','base','meta'],FORBID_ATTR:['style','srcset'],SANITIZE_NAMED_PROPS:true});
   for(const link of section.querySelectorAll('a')){const href=link.getAttribute('href'),asset=entry.links?.[href];if(asset){const target=story.sources.find(s=>s.asset_id===asset);link.href='#';if(target)link.dataset.thinkingSource=target.id;else{link.dataset.asset=asset;link.dataset.assignment=assignmentId;}}else if(/^https:\/\//.test(href||'')){link.target='_blank';link.rel='noopener noreferrer';}else if(!(href||'').startsWith('#')){link.removeAttribute('href');link.title='此引用未纳入本课程共享资料';}}
   for(const img of section.querySelectorAll('img'))img.replaceWith(text('span','[原文图片请在课程资料库中查看]'));
   html=section.innerHTML;
  }else if(a.mime==='text/csv'){
   const data=Papa.parse(content,{header:true,preview:500,skipEmptyLines:true});rows=data.data;const table=document.createElement('table'),head=document.createElement('thead'),tr=document.createElement('tr'),body=document.createElement('tbody');
   for(const key of data.meta.fields||[])tr.append(text('th',key));head.append(tr);table.append(head,body);for(const row of rows){const tr=document.createElement('tr');for(const key of data.meta.fields||[])tr.append(text('td',String(row[key]??'')));body.append(tr);}html=table.outerHTML;
  }else html=text('pre',content).outerHTML;
  return {title:source.title,html,rows,kind,sha256:a.sha256,changed:source.changed,path:'本课程共享资料 · '+entry.name};
 }
});
window.onlineBridge={snapshots,previewSource,thinking,invalidate:()=>{cached=null;thinkingVersions.clear();}};
document.addEventListener('click',e=>{const b=e.target.closest('[data-asset]');if(b){e.preventDefault();previewSource(b.dataset.asset,b.dataset.assignment);}});
$('file-close').onclick=()=>{$('file-panel').hidden=true;clearViewer();};$('file-expand').onclick=()=>$('file-panel').classList.toggle('fullscreen');$('admin-close').onclick=()=>$('admin').close();
initialize().catch(e=>screen(e.message));
