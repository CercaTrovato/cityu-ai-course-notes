// Route thinking reads through the same authenticated course snapshot and asset APIs.
export function createThinkingBridge({getSnapshot,readSource}){
 return async function thinking(url){
  const match=/^\/api\/thinking\/([A-Z]{2}\d{4}-A\d{2})(?:\/source\/([a-z0-9-]+))?$/.exec(url);
  if(!match)throw Error('思路资料入口无效。');
  const [,assignmentId,sourceId]=match,course=assignmentId.split('-')[0];
  const release=await getSnapshot(course),data=release?.snapshot?.thinking;
  if(!data)return null;
  if(data.assignment_id!==assignmentId||release.course_id!==course)throw Error('思路解析与获准课程不一致。');
  if(!sourceId)return data;
  const source=data.sources.find(s=>s.id===sourceId),entry=release.snapshot.files.find(f=>f.id===source?.asset_id);
  if(!source||!entry)throw Error('此资料未纳入本课程共享版本。');
  return readSource({release,source,entry,thinking:data,assignmentId});
 };
}
