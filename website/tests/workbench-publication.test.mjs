import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, stat, writeFile, symlink, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { writeFixture } from './fixtures.mjs';
import { readCatalog, openProject, validateChangeSet, stagePublication, applyPublication, inspectPublication, buildCanonicalPreview } from '../lib/workbench.mjs';
import { hash, durableWrite } from '../lib/workbench-files.mjs';

function redigest(proposal) {
 const {digest,...payload}=proposal;
 proposal.digest=hash(JSON.stringify(payload,(_,value)=>value&&typeof value==='object'&&!Array.isArray(value)?Object.fromEntries(Object.keys(value).sort().map(key=>[key,value[key]])):value));
 return proposal;
}

async function proposed(f, {markdown='# New story\n'}={}) {
 const opened=await openProject(f.repoRoot,'project-one');
 const bytes=Buffer.from('prepared JPEG fixture bytes'),digest=hash(bytes),id=`studio-${digest}`;
 const record={...f.raw.media[0],id,assetPath:`website/assets/workbench/${id}.jpg`};
 const project={...opened.project,summary:'New summary',storyId:'new-story',gallery:[{mediaId:id,caption:'New image',role:'detail'}],searchMediaIds:[id]};
 const change={schemaVersion:1,base:opened.base,projects:[{sourceId:project.id,record:project,story:{id:'new-story',markdown}}],home:{...f.raw.home,intro:'New home copy'},services:[{...f.raw.services[0],description:'New service copy'}],promotions:[{itemId:'inbox-one',hash:digest,record}]};
 const assets=[{itemId:'inbox-one',hash:digest,bytes}];
 return {proposal:await validateChangeSet(f.repoRoot,change,assets),assets};
}

test('staging is private, durable, exact and rejects tampering before canonical mutation',async t=>{
 const f=await writeFixture(t),{proposal,assets}=await proposed(f);
 const before=await readFile(path.join(f.contentRoot,'projects/project-one.json'));
 const manifest=await stagePublication(f.repoRoot,proposal,{operationRoot:path.join(f.repoRoot,'private-operations'),assets});
 assert.equal(manifest.phase,'staged');assert.equal(manifest.proposalDigest,proposal.digest);
 assert.equal((await stat(manifest.operationRoot)).mode&0o777,0o700);
 assert.equal((await stat(path.join(manifest.operationRoot,'manifest.json'))).mode&0o777,0o600);
 assert.deepEqual(await readFile(path.join(f.contentRoot,'projects/project-one.json')),before);
 assert.equal((await inspectPublication(f.repoRoot,manifest)).state,'not-started');
 assert.deepEqual(await stagePublication(f.repoRoot,proposal,{operationRoot:path.join(f.repoRoot,'private-operations'),assets}),manifest);
 await writeFile(path.join(manifest.operationRoot,manifest.writes[0].snapshot),'tampered');
 await assert.rejects(applyPublication(f.repoRoot,manifest),/snapshot|hash/);
 assert.deepEqual(await readFile(path.join(f.contentRoot,'projects/project-one.json')),before);
});

test('every replacement interruption recovers exact after-state and retry performs no writes',async t=>{
 const baseline=await writeFixture(t),sample=await proposed(baseline);
 for(let stop=1;stop<=sample.proposal.writes.length;stop++) {
  const f=await writeFixture(t),{proposal,assets}=await proposed(f);
  const review=await readFile(path.join(f.contentRoot,'reviews/pilot.json'));
  const manifest=await stagePublication(f.repoRoot,proposal,{operationRoot:path.join(f.repoRoot,'operations'),assets});
  let count=0;
  await assert.rejects(applyPublication(f.repoRoot,manifest,{afterReplace:()=>{if(++count===stop)throw Error('interrupted');}}),/interrupted/);
  const reopened=JSON.parse(await readFile(path.join(manifest.operationRoot,'manifest.json'),'utf8'));
  assert.equal((await inspectPublication(f.repoRoot,reopened)).state,stop===proposal.writes.length?'applied':'partial');
  const first=await applyPublication(f.repoRoot,reopened);
  const retry=await applyPublication(f.repoRoot,reopened,{afterReplace:()=>{throw Error('replayed');}});
  assert.deepEqual(retry,first);assert.equal(first.sourceApplied,true);
  for(const write of proposal.writes)assert.equal(hash(await readFile(path.join(f.repoRoot,write.path))),write.after);
  assert.deepEqual(await readFile(path.join(f.contentRoot,'reviews/pilot.json')),review);
  assert.equal((await readCatalog(f.repoRoot)).reviewState,'candidate');
 }
});

test('external conflicts and changed review block publication before the first write',async t=>{
 const f=await writeFixture(t),{proposal,assets}=await proposed(f);
 const manifest=await stagePublication(f.repoRoot,proposal,{operationRoot:path.join(f.repoRoot,'operations'),assets});
 await f.saveRecord('reviews/pilot.json',{...f.raw.review,state:'reviewed'});
 await assert.rejects(applyPublication(f.repoRoot,manifest),/changed|candidate|stale/);
 assert.equal((await inspectPublication(f.repoRoot,manifest)).state,'not-started');
 await f.saveRecord('reviews/pilot.json',f.raw.review);
 await f.saveRecord('projects/project-one.json',{...f.raw.projects[0],summary:'Outside edit'});
 await assert.rejects(applyPublication(f.repoRoot,manifest),/conflict|changed/);
});

test('replacement rechecks the expected before digest immediately before install',async t=>{
 const f=await writeFixture(t),{proposal,assets}=await proposed(f);
 const manifest=await stagePublication(f.repoRoot,proposal,{operationRoot:path.join(f.repoRoot,'operations'),assets});
 const outside={...f.raw.projects[0],summary:'Concurrent structured edit'};
 await assert.rejects(applyPublication(f.repoRoot,manifest,{beforeTargetMutation:async entry=>{
  if(entry.kind==='project'&&entry.id==='project-one')await f.saveRecord('projects/project-one.json',outside);
 }}),/conflict|changed/);
 assert.deepEqual(JSON.parse(await readFile(path.join(f.contentRoot,'projects/project-one.json'))),outside);
});

test('removal rechecks the expected before digest immediately before unlink',async t=>{
 const f=await writeFixture(t);
 await f.saveRecord('site.json',{...f.raw.site,navigation:[{label:'Home',href:'/'}]});
 const opened=await openProject(f.repoRoot,'project-one');
 const change={schemaVersion:1,base:opened.base,projects:[{sourceId:'project-one',record:{...opened.project,id:'renamed-project'},story:null}],home:{...f.raw.home,featuredProjectIds:['renamed-project']},services:[{...f.raw.services[0],projectIds:['renamed-project']}],promotions:[]};
 const proposal=await validateChangeSet(f.repoRoot,change,[]);
 const manifest=await stagePublication(f.repoRoot,proposal,{operationRoot:path.join(f.repoRoot,'operations')});
 const outside={...f.raw.projects[0],summary:'Concurrent structured edit'};
 await assert.rejects(applyPublication(f.repoRoot,manifest,{beforeTargetMutation:async entry=>{
  if(entry.kind==='project'&&entry.id==='project-one')await f.saveRecord('projects/project-one.json',outside);
 }}),/conflict|changed/);
 assert.deepEqual(JSON.parse(await readFile(path.join(f.contentRoot,'projects/project-one.json'))),outside);
});

test('verified apply followed by candidate build failure preserves applied source and permits a no-write retry',async t=>{
 const f=await writeFixture(t),{proposal,assets}=await proposed(f);
 const manifest=await stagePublication(f.repoRoot,proposal,{operationRoot:path.join(f.repoRoot,'operations'),assets});
 await applyPublication(f.repoRoot,manifest);
 const result=await buildCanonicalPreview(f.repoRoot);
 assert.equal(result.sourceApplied,true);assert.equal(result.candidatePreview,'failed');assert.match(result.message,/rebuild/i);
 assert.equal((await inspectPublication(f.repoRoot,manifest)).state,'applied');
 await applyPublication(f.repoRoot,manifest,{afterReplace:()=>{throw Error('replayed');}});
});

test('private preview builds promoted bytes and blank stories entirely under its caller root',async t=>{
 const { cp, readdir }=await import('node:fs/promises');
 const { fileURLToPath }=await import('node:url');
 const { buildPrivatePreview }=await import('../lib/workbench.mjs');
 const f=await writeFixture(t),source=path.resolve(fileURLToPath(new URL('..',import.meta.url)));
 for(const name of ['src','lib','astro.config.mjs','package.json'])await cp(path.join(source,name),path.join(f.repoRoot,'website',name),{recursive:true});
 await symlink(path.join(source,'node_modules'),path.join(f.repoRoot,'website/node_modules'));
 await f.save('site_example/journal-search.js',await readFile(path.join(source,'../site_example/journal-search.js')));
 const {proposal,assets}=await proposed(f,{markdown:''}),protectedFiles=['website/content/projects/project-one.json','website/content/reviews/pilot.json','website/src/generated/site.json'];
 const before=await Promise.all(protectedFiles.map(p=>readFile(path.join(f.repoRoot,p))));
 const result=await buildPrivatePreview(f.repoRoot,proposal,{previewRoot:path.join(f.repoRoot,'private-previews'),assets});
 assert.equal(result.digest,proposal.digest);assert.ok(result.outputRoot.startsWith(path.join(f.repoRoot,'private-previews')+path.sep));
 assert.match(await readFile(path.join(result.outputRoot,'work/project-one/index.html'),'utf8'),/New summary/);
 const asset=proposal.writes.find(w=>w.kind==='asset');
 assert.equal(hash(await readFile(path.join(result.outputRoot,'media',`${asset.id}.jpg`))),asset.after);
 assert.deepEqual(await Promise.all(protectedFiles.map(p=>readFile(path.join(f.repoRoot,p)))),before);
 assert.ok(!(await readdir(path.join(f.repoRoot,'website'))).includes('.preview-dist'));
 assert.deepEqual(await buildPrivatePreview(f.repoRoot,proposal,{previewRoot:path.join(f.repoRoot,'private-previews'),assets}),result);
 await assert.rejects(buildPrivatePreview(f.repoRoot,proposal,{previewRoot:path.join(f.repoRoot,'website','private'),assets}),/overlap/);
 await mkdir(path.join(f.repoRoot,'outside'));
 await symlink(path.join(f.repoRoot,'outside'),path.join(f.repoRoot,'linked-preview'));
 await assert.rejects(buildPrivatePreview(f.repoRoot,proposal,{previewRoot:path.join(f.repoRoot,'linked-preview'),assets}),/ordinary local/);
});

test('renames recover after every replacement and removal, retaining exact before snapshots',async t=>{
 for(let stop=1;stop<=6;stop++) {
  const f=await writeFixture(t);
  await f.saveRecord('site.json',{...f.raw.site,navigation:[{label:'Home',href:'/'}]});
  await f.saveRecord('projects/project-one.json',{...f.raw.projects[0],storyId:'old-story'});
  const oldStory='---\nschemaVersion: 1\nid: old-story\n---\n# Exact old story\n';
  await f.save('website/content/stories/old-story.md',oldStory);
  const opened=await openProject(f.repoRoot,'project-one');
  const change={schemaVersion:1,base:opened.base,projects:[{sourceId:'project-one',record:{...opened.project,id:'renamed-project',storyId:'renamed-story'},story:{id:'renamed-story',markdown:''}}],home:{...f.raw.home,featuredProjectIds:['renamed-project']},services:[{...f.raw.services[0],projectIds:['renamed-project']}],promotions:[]};
  const proposal=await validateChangeSet(f.repoRoot,change,[]);
  assert.equal(proposal.writes.length+proposal.removals.length,6);
  const manifest=await stagePublication(f.repoRoot,proposal,{operationRoot:path.join(f.repoRoot,'operations')});
  let count=0;const landed=[];
  await assert.rejects(applyPublication(f.repoRoot,manifest,{afterReplace:entry=>{landed.push(entry.path);if(++count===stop)throw Error('stop');}}),/stop/);
  assert.deepEqual(landed.slice(0,Math.min(4,stop)),proposal.writes.slice(0,Math.min(4,stop)).map(w=>w.path));
  const reopened=JSON.parse(await readFile(path.join(manifest.operationRoot,'manifest.json'),'utf8'));
  const before=manifest.removals.find(r=>r.kind==='story');
  assert.equal(await readFile(path.join(manifest.operationRoot,before.beforeSnapshot),'utf8'),oldStory);
  await applyPublication(f.repoRoot,reopened);
  assert.equal((await inspectPublication(f.repoRoot,reopened)).state,'applied');
  assert.deepEqual((await readCatalog(f.repoRoot)).projects.map(p=>p.id),['project-two','renamed-project']);
  for(const removal of proposal.removals)await assert.rejects(readFile(path.join(f.repoRoot,removal.path)),{code:'ENOENT'});
 }
});

test('staging rejects a newly conflicting untouched album owner and caller target tampering',async t=>{
 const f=await writeFixture(t),{proposal}=await proposed(f);
 const tampered=structuredClone(proposal);tampered.writes[0].path='journals/project-one.md';
 await assert.rejects(stagePublication(f.repoRoot,tampered,{operationRoot:path.join(f.repoRoot,'operations')}),/digest|target/);
 const manifest=await stagePublication(f.repoRoot,proposal,{operationRoot:path.join(f.repoRoot,'operations')});
 const changed=structuredClone(manifest);changed.writes[0].path='journals/project-one.md';
 await assert.rejects(applyPublication(f.repoRoot,changed),/manifest/);
 await f.saveRecord('projects/project-two.json',{...f.raw.projects[1],albumKeys:['flickr:111'],sourceRefs:f.raw.projects[0].sourceRefs});
 await assert.rejects(applyPublication(f.repoRoot,manifest),/already owned/);
 assert.equal((await inspectPublication(f.repoRoot,manifest)).state,'not-started');
});

test('even a recomputed proposal digest cannot substitute a different record identity',async t=>{
 const f=await writeFixture(t);
 await f.saveRecord('site.json',{...f.raw.site,navigation:[{label:'Home',href:'/'}]});
 const {proposal}=await proposed(f),forged=structuredClone(proposal);
 const entry=forged.writes.find(w=>w.kind==='project');
 const record=JSON.parse(Buffer.from(entry.bytes,'base64'));record.id='different-id';
 const bytes=Buffer.from(JSON.stringify(record));entry.bytes=bytes.toString('base64');entry.after=hash(bytes);
 for(const w of forged.writes.filter(w=>['home','service'].includes(w.kind))) {
  const value=JSON.parse(Buffer.from(w.bytes,'base64'));
  if(w.kind==='home')value.featuredProjectIds=['different-id'];else value.projectIds=['different-id'];
  const replacement=Buffer.from(JSON.stringify(value));w.bytes=replacement.toString('base64');w.after=hash(replacement);
 }
 const {digest,...payload}=forged;
 forged.digest=hash(JSON.stringify(payload,(_,v)=>v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.keys(v).sort().map(k=>[k,v[k]])):v));
 await assert.rejects(stagePublication(f.repoRoot,forged,{operationRoot:path.join(f.repoRoot,'operations')}),/identity|proposal/i);
});

test('recomputed proposal digests cannot change untouched content outside the canonical overlay',async t=>{
 const {buildPrivatePreview}=await import('../lib/workbench.mjs');
 const f=await writeFixture(t),{proposal}=await proposed(f);
 const forged=structuredClone(proposal);
 forged.content.projects.find(project=>project.id==='project-two').summary='Forged preview-only summary';
 redigest(forged);
 await assert.rejects(stagePublication(f.repoRoot,forged,{operationRoot:path.join(f.repoRoot,'operations')}),/overlay/);
 await assert.rejects(buildPrivatePreview(f.repoRoot,forged,{previewRoot:path.join(f.repoRoot,'previews')}),/overlay/);
});

test('forged removals cannot leave the removed project in proposal content',async t=>{
 const {buildPrivatePreview}=await import('../lib/workbench.mjs');
 const f=await writeFixture(t),{proposal}=await proposed(f),forged=structuredClone(proposal);
 const target='website/content/projects/project-two.json',before=hash(await readFile(path.join(f.repoRoot,target)));
 forged.base.push({kind:'project',id:'project-two',sha256:before});
 forged.removals.push({kind:'project',id:'project-two',path:target,before});
 redigest(forged);
 await assert.rejects(stagePublication(f.repoRoot,forged,{operationRoot:path.join(f.repoRoot,'operations')}),/overlay/);
 await assert.rejects(buildPrivatePreview(f.repoRoot,forged,{previewRoot:path.join(f.repoRoot,'previews')}),/overlay/);
 assert.equal(hash(await readFile(path.join(f.repoRoot,target))),before);
});

test('operation staging repairs truncated snapshots, proposal, and manifest on retry',async t=>{
 for(const kind of ['before','after','proposal','manifest']) {
  const f=await writeFixture(t),{proposal}=await proposed(f),operationRoot=path.join(f.repoRoot,'operations');
  const manifest=await stagePublication(f.repoRoot,proposal,{operationRoot});
  const relative=kind==='before'?manifest.writes.find(write=>write.beforeSnapshot).beforeSnapshot:
   kind==='after'?manifest.writes[0].snapshot:`${kind}.json`;
  const target=path.join(manifest.operationRoot,relative),complete=await readFile(target);
  await writeFile(target,complete.subarray(0,Math.floor(complete.length/2)));
  assert.deepEqual(await stagePublication(f.repoRoot,proposal,{operationRoot}),manifest);
  assert.deepEqual(await readFile(target),complete);
  assert.equal((await stat(target)).mode&0o777,0o600);
  assert.equal((await inspectPublication(f.repoRoot,manifest)).state,'not-started');
 }
});

test('applied source plus a truncated receipt retries to the same receipt without source writes',async t=>{
 const f=await writeFixture(t),{proposal}=await proposed(f);
 const manifest=await stagePublication(f.repoRoot,proposal,{operationRoot:path.join(f.repoRoot,'operations')});
 const first=await applyPublication(f.repoRoot,manifest),receiptPath=path.join(manifest.operationRoot,'receipt.json');
 const complete=await readFile(receiptPath);
 for(const length of [0,Math.floor(complete.length/2)]) {
  await writeFile(receiptPath,complete.subarray(0,length));
  const reopened=JSON.parse(await readFile(path.join(manifest.operationRoot,'manifest.json'),'utf8'));
  assert.deepEqual(await applyPublication(f.repoRoot,reopened,{afterReplace:()=>{throw Error('replayed');}}),first);
  assert.deepEqual(await readFile(receiptPath),complete);
  assert.equal((await inspectPublication(f.repoRoot,reopened)).state,'applied');
 }
 const different=Buffer.from(JSON.stringify({...first,proposalDigest:'f'.repeat(64)}));
 await writeFile(receiptPath,different);
 await assert.rejects(applyPublication(f.repoRoot,manifest),/snapshot differs/);
 assert.deepEqual(await readFile(receiptPath),different);
});

test('durable metadata replacement exposes only complete files across interruptions',async t=>{
 const f=await writeFixture(t),bytes=Buffer.from('{"receipt":"complete"}\n'),relative='operation/receipt.json';
 const options={repairIncomplete:true,afterSync:async({target,temporary})=>{
  assert.deepEqual(await readFile(temporary),bytes);
  await assert.rejects(readFile(target),{code:'ENOENT'});
  throw Error('metadata interruption');
 }};
 await assert.rejects(durableWrite(f.repoRoot,relative,bytes,options),/metadata interruption/);
 await assert.rejects(readFile(path.join(f.repoRoot,relative)),{code:'ENOENT'});
 await durableWrite(f.repoRoot,relative,bytes,{repairIncomplete:true});
 assert.deepEqual(await readFile(path.join(f.repoRoot,relative)),bytes);
 const partial=bytes.subarray(0,8);
 await writeFile(path.join(f.repoRoot,relative),partial);
 await assert.rejects(durableWrite(f.repoRoot,relative,bytes,{repairIncomplete:true,afterSync:async({target})=>{
  assert.deepEqual(await readFile(target),partial);
  throw Error('metadata interruption');
 }}),/metadata interruption/);
 assert.deepEqual(await readFile(path.join(f.repoRoot,relative)),partial);
 await durableWrite(f.repoRoot,relative,bytes,{repairIncomplete:true});
 assert.deepEqual(await readFile(path.join(f.repoRoot,relative)),bytes);
 assert.equal((await stat(path.join(f.repoRoot,relative))).mode&0o777,0o600);
 const different=Buffer.from('{"receipt":"other"}\n');
 await writeFile(path.join(f.repoRoot,relative),different);
 await assert.rejects(durableWrite(f.repoRoot,relative,bytes,{repairIncomplete:true}),/snapshot differs/);
 assert.deepEqual(await readFile(path.join(f.repoRoot,relative)),different);
});

test('derived site navigation writes survive every rename interruption and reject arbitrary site edits',async t=>{
 for(let stop=1;stop<=5;stop++) {
  const f=await writeFixture(t),opened=await openProject(f.repoRoot,'project-one');
  const change={schemaVersion:1,base:opened.base,projects:[{sourceId:'project-one',record:{...opened.project,id:'renamed-project'},story:null}],home:{...f.raw.home,featuredProjectIds:['renamed-project']},services:[{...f.raw.services[0],projectIds:['renamed-project']}],promotions:[]};
  const proposal=await validateChangeSet(f.repoRoot,change,[]);
  assert.equal(proposal.writes.length+proposal.removals.length,5);
  const forged=structuredClone(proposal),siteWrite=forged.writes.find(write=>write.kind==='site');
  forged.content.site.name='Arbitrary site edit';
  const bytes=Buffer.from(JSON.stringify(forged.content.site));siteWrite.bytes=bytes.toString('base64');siteWrite.after=hash(bytes);
  redigest(forged);
  await assert.rejects(stagePublication(f.repoRoot,forged,{operationRoot:path.join(f.repoRoot,'forged')}),/derived.*navigation/);
  const manifest=await stagePublication(f.repoRoot,proposal,{operationRoot:path.join(f.repoRoot,'operations')});
  let count=0;
  await assert.rejects(applyPublication(f.repoRoot,manifest,{afterReplace:()=>{if(++count===stop)throw Error('stop');}}),/stop/);
  const reopened=JSON.parse(await readFile(path.join(manifest.operationRoot,'manifest.json'),'utf8'));
  const first=await applyPublication(f.repoRoot,reopened);
  assert.deepEqual(await applyPublication(f.repoRoot,reopened,{afterReplace:()=>{throw Error('replayed');}}),first);
  assert.deepEqual(JSON.parse(await readFile(path.join(f.contentRoot,'site.json'))),proposal.content.site);
  assert.equal((await inspectPublication(f.repoRoot,reopened)).state,'applied');
 }
});

test('persisted rename metadata rejects a ghost source with no prior project hash',async t=>{
 const f=await writeFixture(t);
 await f.saveRecord('site.json',{...f.raw.site,navigation:[{label:'Home',href:'/'}]});
 const opened=await openProject(f.repoRoot,'project-one');
 const change={schemaVersion:1,base:opened.base,projects:[{sourceId:'project-one',record:{...opened.project,id:'renamed-project'},story:null}],home:{...f.raw.home,featuredProjectIds:['renamed-project']},services:[{...f.raw.services[0],projectIds:['renamed-project']}],promotions:[]};
 const forged=structuredClone(await validateChangeSet(f.repoRoot,change,[]));
 forged.writes.find(write=>write.kind==='project').sourceId='ghost-project';
 forged.base.push({kind:'project',id:'ghost-project',sha256:null});
 forged.removals.push({kind:'project',id:'ghost-project',path:'website/content/projects/ghost-project.json',before:null});
 redigest(forged);
 await assert.rejects(stagePublication(f.repoRoot,forged,{operationRoot:path.join(f.repoRoot,'operations')}),/rename identity/);
 assert.equal(JSON.parse(await readFile(path.join(f.contentRoot,'projects/project-one.json'))).id,'project-one');
});
