import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source=fs.readFileSync(new URL('../src/review.mjs',import.meta.url),'utf8').replace(/^import .*;\r?\n/gm,'');
const context=vm.createContext({window:{}});vm.runInContext(source,context);
const sample={course:'IS5113',exam:'12/10 18:30–20:30',title:'AI伦理',scope:'当前范围',progress_updated_at:'2026-11-27',issues:[],documents:[{id:'framework.md',text:'# 全课框架',url:'https://example.org/framework.md'},{id:'exam-guide.md',text:'# 考试依据',url:'https://example.org/exam-guide.md'}]};
test('course landing opens the dedicated exam guide by default',()=>{
 context.fixture=sample;
 assert.equal(vm.runInContext('mode',context),'exam');
 const html=vm.runInContext('course(fixture)',context);
 assert.match(html,/data-rv-mode="exam" class="selected">考试范围与要求/);
 assert.match(html,/id="rv-document"/);
 assert.equal(vm.runInContext('docId',context),'exam-guide.md');
});
test('a missing exam guide shows an explicit gap, not the full course as confirmed scope',()=>{
 context.fixture={...sample,documents:[sample.documents[0]]};
 const html=vm.runInContext('exam(fixture)',context);
 assert.match(html,/详细考试依据待同步/);
 assert.doesNotMatch(html,/id="rv-document"/);
});
