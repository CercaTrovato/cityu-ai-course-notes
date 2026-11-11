export function createCourseSelection(courses,onSelect){
 const form=document.createElement('form');form.className='course-selection';
 const label=document.createElement('label');label.htmlFor='first-course';label.textContent='选择你所属的课程';
 const select=document.createElement('select');select.id='first-course';select.required=true;
 const empty=document.createElement('option');empty.value='';empty.textContent='请选择课程';empty.disabled=true;empty.selected=true;select.append(empty);
 for(const course of courses){const option=document.createElement('option');option.value=course.id;option.textContent=course.id+' · '+course.title;select.append(option);}
 const note=document.createElement('p');note.className='micro';note.textContent='每个 GitHub 账号只可绑定一门课程。确认后即可查看本课资料；选错时由总监督协助改绑。';
 const submit=document.createElement('button');submit.type='submit';submit.className='primary';submit.textContent='确认并进入课程';submit.disabled=true;
 const error=document.createElement('p');error.setAttribute('role','alert');error.className='course-selection-error';
 select.onchange=()=>{submit.disabled=!select.value;error.textContent='';};
 form.onsubmit=async event=>{event.preventDefault();if(!select.value||submit.disabled)return;submit.disabled=true;select.disabled=true;error.textContent='';try{await onSelect(select.value);}catch(e){error.textContent=e.message||'暂时无法完成选课，请重试。';select.disabled=false;submit.disabled=false;}};
 form.append(label,select,note,submit,error);return form;
}
