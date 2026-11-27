import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source=fs.readFileSync(new URL('../src/review.mjs',import.meta.url),'utf8').replace(/^import .*;\r?\n/gm,'');
const context=vm.createContext({window:{},document:{getElementById:()=>null}});vm.runInContext(source,context);
test('knowledge route exposes its existing map without replacing unit evidence',()=>{
 context.fixture={documents:[{id:'learning-map.md'}],next:'已有学习停点',units:[]};
 assert.match(vm.runInContext('route(fixture)',context),/打开本课学习地图/);
 assert.match(vm.runInContext('route(fixture)',context),/已有学习停点/);
});
test('opening the map clears an old search and selects the map document',()=>{
 vm.runInContext("filter='old term';openMap()",context);
 assert.equal(vm.runInContext('mode',context),'reader');
 assert.equal(vm.runInContext('docId',context),'learning-map.md');
 assert.equal(vm.runInContext('filter',context),'');
});
