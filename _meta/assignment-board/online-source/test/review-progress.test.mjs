import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source=fs.readFileSync(new URL('../src/review.mjs',import.meta.url),'utf8').replace(/^import .*;\r?\n/gm,'');
const sandbox={window:{}};
vm.runInNewContext(source,sandbox);
const learned=sandbox.window.ReviewBoard.learned;
test('IS5113 evidence-backed independent_correct is counted',()=>{
 assert.equal(learned({status:'in_progress',mastery_status:'independent_correct',evidence:[{session_id:'s1'}]}),true);
 assert.equal(learned({status:'in_progress',mastery_status:'independent_correct',evidence:[]}),false);
});
test('other courses retain evidence and retest semantics',()=>{
 assert.equal(learned({status:'completed',mastery_level:'solved_independently',learning_evidence:['s1']}),true);
 assert.equal(learned({status:'in_progress',mastery:'solved_with_hint',evidence:['s2']}),false);
 assert.equal(learned({status:'retest_passed',evidence:['s3']}),true);
});
