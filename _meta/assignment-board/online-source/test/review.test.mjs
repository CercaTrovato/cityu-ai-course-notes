import test from 'node:test';
import assert from 'node:assert/strict';
import {validateSnapshot} from '../server/policy.mjs';

const sample=()=>({schema_version:1,course:'IS6400',assignments:[{course:'IS6400',assignment_type:'group',review:{course:'IS6400',units:[],documents:[]}}],files:[]});
test('review content remains in the authorized course snapshot',()=>{
 const s=sample();validateSnapshot(s,'IS6400');s.assignments[0].review.course='AC6761';assert.throws(()=>validateSnapshot(s,'IS6400'),/复习记录/);
});
test('review cannot publish internal paths or malformed documents',()=>{
 const s=sample();s.assignments[0].review.documents=[{text:'D:/private/work.md'}];assert.throws(()=>validateSnapshot(s,'IS6400'),/本机路径/);
 s.assignments[0].review.documents={};assert.throws(()=>validateSnapshot(s,'IS6400'),/复习记录/);
});
