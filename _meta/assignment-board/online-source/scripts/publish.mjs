import fs from 'node:fs/promises';
import path from 'node:path';
import {buildCourse} from './export.mjs';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {fileURLToPath} from 'node:url';
const args=process.argv.slice(2),get=(flag,fallback)=>args.includes(flag)?args[args.indexOf(flag)+1]:fallback;
const configPath=get('--config',path.resolve('.local/publisher.json'));
async function main(){
 const config=JSON.parse(await fs.readFile(configPath,'utf8')),dry=!args.includes('--publish');
 if(!dry&&!process.env.BOARD_PUBLISH_TOKEN){const script=fileURLToPath(new URL('./windows-secrets.py',import.meta.url));try{const {stdout}=await promisify(execFile)('D:/anaconda3/python.exe',['-X','utf8',script,'read',path.join(path.dirname(configPath),'publish-token.dpapi')],{windowsHide:true});process.env.BOARD_PUBLISH_TOKEN=stdout.trim();}catch{throw Error('尚未完成本机发布凭据配置，或当前 Windows 账号无法解密。');}}
 if(!dry&&(!/^https:\/\//.test(config.origin||'')||!process.env.BOARD_PUBLISH_TOKEN))throw Error('请先完成线上地址和本机发布凭据的一次性配置。');
 const output=path.resolve(config.cache_dir);await fs.mkdir(output,{recursive:true});
 const api=async(route,body)=>{const r=await fetch(config.origin+'/api/'+route,{method:body?'POST':'GET',headers:{'x-board-publish-token':process.env.BOARD_PUBLISH_TOKEN,'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(90000)});const v=await r.json();if(!r.ok)throw Error(v.error||'线上请求失败');return v;};
 const local=await fetch(config.local_api||'http://127.0.0.1:8766/api/assignments',{signal:AbortSignal.timeout(10000)});if(!local.ok)throw Error('无法读取本地看板');const data=await local.json();
 const result={started_at:new Date().toISOString(),mode:dry?'dry-run':'publish',courses:[]};let failed=false;
 for(const policy of config.courses){
  if(get('--course')&&get('--course')!==policy.course)continue;
  try{
   const record=data.assignments.find(r=>r.id===policy.assignment_id);if(!record)throw Error('本地看板中没有该作业');
   const bundle=await buildCourse(record,policy,{cacheDir:output});
   const receipt={course:policy.course,hash:bundle.snapshot.content_hash,files:bundle.assets.length,bytes:bundle.total,warnings:bundle.warnings};
   await fs.writeFile(path.join(output,policy.course+'-preview.json'),JSON.stringify(bundle.snapshot,null,2));
   if(dry){receipt.state='prepared';console.log(policy.course+': 预检通过，'+receipt.files+' 个附件，'+(receipt.bytes/1048576).toFixed(1)+' MiB');}
   else{
    console.log(policy.course+': 正在核对线上版本与共享附件…');
    const prior=await api('publish/status?course='+policy.course);
    if(prior.content_hash===bundle.snapshot.content_hash){receipt.state='unchanged';receipt.release=prior.active_release;console.log(policy.course+': 内容一致，无需上传');}
    else{
     const release=await api('publish/begin',{course_id:policy.course,snapshot:bundle.snapshot,expected_count:bundle.assets.length,expected_release:prior.active_release});let reused=0;
     for(const asset of bundle.assets){const {buffer,...meta}=asset;const ticket=await api('publish/asset',{...meta,release_id:release.id});
      if(ticket.reused){reused++;continue;}
      const upload=await fetch(ticket.signedUrl,{method:'PUT',headers:{'Content-Type':asset.mime,'x-upsert':'false'},body:buffer,signal:AbortSignal.timeout(120000)});
      // A previous interrupted attempt can have uploaded the same content-addressed object.
      if(!upload.ok&&![400,409].includes(upload.status))throw Error('附件上传失败：'+asset.name);
      await api('publish/verify',{release_id:release.id,asset_id:asset.asset_id});
     }
     await api('publish/commit',{release_id:release.id});const now=await api('publish/status?course='+policy.course);if(now.active_release!==release.id)throw Error('线上版本回读不一致');receipt.state='published';receipt.release=release.id;receipt.reused=reused;console.log(policy.course+': 同步成功，复用 '+reused+' 个未变附件');
    }
   }
   result.courses.push(receipt);
  }catch(e){failed=true;console.error(policy.course+': '+e.message);result.courses.push({course:policy.course,state:'failed',error:e.message});}
 }
 result.finished_at=new Date().toISOString();const receipt=JSON.stringify(result,null,2);await fs.mkdir(path.join(output,'receipts'),{recursive:true});await fs.writeFile(path.join(output,'receipts',Date.now()+'.json'),receipt);await fs.writeFile(path.join(output,'latest-receipt.json'),receipt);if(failed)process.exitCode=1;
}
main().catch(e=>{console.error(e.message);process.exitCode=1;});
