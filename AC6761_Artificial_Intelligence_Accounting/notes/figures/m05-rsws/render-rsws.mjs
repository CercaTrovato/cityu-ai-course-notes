// Package-local reproducible copy; layout-only repair AC-M05-V01.
// Usage: node render-rsws.mjs --input model.json --output rsws-full [--overview] [--runtime-dir CACHE]
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {createHash} from 'node:crypto';

// Local Graphviz/WASM rendering only. Source data is never sent to a diagram service.
const args=process.argv.slice(2);
function option(key,fallback){const at=args.indexOf(key);return at<0?fallback:args[at+1];}
const input=option('--input');
const output=option('--output');
const runtime=option('--runtime-dir',process.env.CITYU_DIAGRAM_RUNTIME||'E:/app-data/diagram-tools');
const overview=args.includes('--overview');
if(!input||!output){throw new Error('Usage: node render_concept_graph.mjs --input model.json --output output-prefix [--runtime-dir persistent-cache]');}
const requiredVersion='3.31.0';
const requireRuntime=createRequire(path.join(path.resolve(runtime),'package.json'));
const packageInfo=JSON.parse(await fs.readFile(path.join(path.resolve(runtime),'node_modules','@viz-js','viz','package.json'),'utf8'));
if(packageInfo.version!==requiredVersion)throw new Error(`Expected @viz-js/viz ${requiredVersion}, found ${packageInfo.version}. Use the pinned runtime; do not upgrade silently.`);
const {instance}=requireRuntime('@viz-js/viz');
const raw=await fs.readFile(input,'utf8');
const model=JSON.parse(raw);
if(model.schema!=='cityu-concept-graph-v1')throw new Error('Unsupported graph contract schema');
if(!['uml-rea','uml-class','relational'].includes(model.diagram_type))throw new Error('Use a concept model type; flow and numerical charts have separate routes.');
const states=new Set(['source','reference','assumption']);
const ids=new Set();
for(const node of model.nodes){
  if(!/^\w[\w-]*$/.test(node.id)||ids.has(node.id))throw new Error('Node IDs must be unique ASCII identifiers: '+node.id);
  ids.add(node.id);
  if(!node.label||!node.kind||!node.source||!states.has(node.status))throw new Error('Every node needs label, kind, source and evidence status: '+node.id);
  const fields=new Set();
  for(const field of node.attributes||[]){
    if(!field.id||fields.has(field.id)||!field.name||!field.source||!states.has(field.status))throw new Error('Invalid, duplicate or unsourced attribute: '+node.id);
    fields.add(field.id);
  }
}
const edgeIDs=new Set();
const multiplicity=(value)=>{
  const m=/^(\d+)\.\.(\d+|\*)$/.exec(value);
  return !!m&&(m[2]==='*'||Number(m[2])>=Number(m[1]));
};
for(const edge of model.edges){
  if(!/^\w[\w-]*$/.test(edge.id)||edgeIDs.has(edge.id))throw new Error('Edge IDs must be unique ASCII identifiers');
  edgeIDs.add(edge.id);
  if(!ids.has(edge.a)||!ids.has(edge.b)||edge.a===edge.b)throw new Error('Unknown or self-referential endpoint: '+edge.id);
  if(!multiplicity(edge.a_multiplicity)||!multiplicity(edge.b_multiplicity))throw new Error('Explicit valid multiplicities required at both endpoints: '+edge.id);
  if(!edge.source||!states.has(edge.status)||!edge.label)throw new Error('Every association needs label, source and evidence status: '+edge.id);
  if((edge.direction||'none')!=='none')throw new Error('This renderer preserves undirected associations; do not imply sequence or inheritance with these links.');
  for(const field of edge.attributes||[])if(!field.id||!field.name||!field.source||!states.has(field.status))throw new Error('Unsourced association attribute: '+edge.id);
}
if(!model.scope||!Array.isArray(model.assumptions)||!model.title)throw new Error('Model title, scope and assumptions array (possibly empty) must be explicit');
const columns=model.layout?.columns||[];
const order=new Map();
columns.forEach((list,i)=>list.forEach(id=>{
  if(!ids.has(id)||order.has(id))throw new Error('Layout columns contain unknown or duplicate node');
  order.set(id,i);
}));
if(columns.length&&order.size!==ids.size)throw new Error('If layout columns are specified, include every node exactly once');
const quote=s=>JSON.stringify(String(s));
const escape=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const colors={Resource:'#e9f3fc',EconomicDecrement:'#fff2dc',EconomicIncrement:'#e8f5ed',InternalAgent:'#f3eefb',ExternalAgent:'#f1f3f5'};
const dot=['digraph CityUModel {',
 'graph [rankdir=LR, nodesep=1.1, ranksep=2.0, splines=polyline, pad=0.7, bgcolor="white", outputorder=edgesfirst];',
 'node [shape=plain, fontname="Arial", fontsize=16];',
 'edge [dir=none, fontname="Arial", fontsize=14, labelfontname="Arial", labelfontsize=16, color="#52616b", labeldistance=6.5, labelangle=0, penwidth=1.3];'];
dot.push(`graph [label=${quote(model.title+(overview?' - relationship overview':' - all attributes')+'\n'+(model.figure_caption||model.scope))},labelloc=b,fontname="Arial",fontsize=13];`);
for(const node of model.nodes){
  const header=`<TR><TD BGCOLOR="${colors[node.kind]||'#f1f3f5'}" ALIGN="CENTER"><FONT POINT-SIZE="13">&lt;&lt;${escape(node.kind)}&gt;&gt;</FONT><BR/><B>${escape(node.label)}</B></TD></TR>`;
  const fields=(overview?[]:node.attributes||[]).map(f=>`<TR><TD ALIGN="LEFT" BALIGN="LEFT">${escape(f.name)}</TD></TR>`).join('');
  const table=`<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="9" COLOR="#52616b">${header}${fields}</TABLE>`;
  dot.push(`${quote(node.id)} [id=${quote('node-'+node.id)},label=<${table}>];`);
}
columns.forEach((list,i)=>dot.push(`subgraph column_${i} { rank=same; ${list.map(quote).join('; ')}; }`));
// Layout ordering constraints are invisible and never counted as business edges.
for(const list of columns)for(let i=1;i<list.length;i++)dot.push(`${quote(list[i-1])} -> ${quote(list[i])} [style=invis,weight=100];`);
const endpoint = value => `<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="2" BGCOLOR="white"><TR><TD>${escape(value)}</TD></TR></TABLE>`;
const expected=[];
for(const edge of model.edges){
  const flip=order.has(edge.a)&&order.has(edge.b)&&order.get(edge.a)>order.get(edge.b);
  const tail=flip?edge.b:edge.a,head=flip?edge.a:edge.b;
  const tailMult=flip?edge.b_multiplicity:edge.a_multiplicity;
  const headMult=flip?edge.a_multiplicity:edge.b_multiplicity;
  const labelLines=[edge.label,...(edge.attributes||[]).map(f=>f.name)];
  const labelTable='<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="3" BGCOLOR="white">'+labelLines.map(line=>'<TR><TD>'+escape(line)+'</TD></TR>').join('')+'</TABLE>';
  const horizontal=order.get(tail)!==order.get(head);
  dot.push(`${quote(tail)} -> ${quote(head)} [id=${quote('edge-'+edge.id)},taillabel=<${endpoint(tailMult)}>,headlabel=<${endpoint(headMult)}>,label=<${labelTable}>,labeldistance=${horizontal?6.5:2.8},labelangle=${horizontal?0:35},constraint=${horizontal?'true':'false'},minlen=1];`);
  expected.push({edge_id:edge.id,a:edge.a,a_multiplicity:edge.a_multiplicity,b:edge.b,b_multiplicity:edge.b_multiplicity,draw_tail:tail,draw_tail_multiplicity:tailMult,draw_head:head,draw_head_multiplicity:headMult});
}
dot.push('}');
const dotSource=dot.join('\n')+'\n';
const viz=await instance();
const result=viz.renderFormats(dotSource,['svg','json'],{engine:'dot'});
if(result.status!=='success'||result.errors.some(e=>e.level==='error'))throw new Error(JSON.stringify(result.errors));
const svg=result.output.svg;
if(/<script\b|<foreignObject\b|(?:href|src)=["']https?:/i.test(svg))throw new Error('Unexpected script or remote asset in generated SVG');
const outputPrefix=path.resolve(output);
await fs.mkdir(path.dirname(outputPrefix),{recursive:true});
async function atomicWrite(filename,content){const temp=filename+'.writing-'+process.pid;try{await fs.writeFile(temp,content,'utf8');await fs.rename(temp,filename);}finally{await fs.rm(temp,{force:true});}}
await atomicWrite(outputPrefix+'.dot',dotSource);
await atomicWrite(outputPrefix+'.svg',svg);
await atomicWrite(outputPrefix+'.layout.json',result.output.json);
const report={schema:model.schema,title:model.title,implementation:'@viz-js/viz',implementation_version:packageInfo.version,graphviz_version:viz.graphvizVersion,source_sha256:createHash('sha256').update(raw).digest('hex'),
  nodes:model.nodes.length,associations:model.edges.length,multiplicity_endpoints:2*model.edges.length,node_attributes:model.nodes.reduce((n,c)=>n+(c.attributes?.length||0),0),association_attributes:model.edges.reduce((n,e)=>n+(e.attributes?.length||0),0),
  overview,shown_node_attributes:overview?0:model.nodes.reduce((n,c)=>n+(c.attributes?.length||0),0),
  warnings:result.errors.filter(e=>e.level==='warning'),endpoint_mapping:expected,semantic_review:'required: source contract validation does not verify business facts',visual_review:'required: actual rendered labels and connections must be checked'};
await atomicWrite(outputPrefix+'.render.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({output:outputPrefix,implementation_version:report.implementation_version,graphviz_version:report.graphviz_version,nodes:report.nodes,associations:report.associations,warnings:report.warnings}));
