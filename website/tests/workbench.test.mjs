import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, rename, symlink } from 'node:fs/promises';
import path from 'node:path';
import { writeFixture } from './fixtures.mjs';
import { readCatalog, openProject, validateChangeSet } from '../lib/workbench.mjs';

export const changeFor = opened => ({schemaVersion:1,base:opened.base,projects:[{sourceId:opened.project.id,record:opened.project,story:opened.story}],home:null,services:[],promotions:[]});

test('catalog and project opening fingerprint only project dependencies', async t => {
  const f=await writeFixture(t);
  const catalog=await readCatalog(f.repoRoot);
  assert.deepEqual(catalog.projects.map(p=>p.id),['project-one','project-two']);
  assert.equal(catalog.albumOwners['flickr:111'],'project-one');
  assert.equal(catalog.reviewState,'candidate');
  const opened=await openProject(f.repoRoot,'project-one');
  assert.equal(opened.story,null);
  assert.deepEqual(opened.references.home,f.raw.home);
  assert.deepEqual(opened.references.services,f.raw.services);
  assert.ok(opened.base.some(d=>d.kind==='project'&&d.id==='project-one'));
  assert.ok(!opened.base.some(d=>d.id==='project-two'));
  assert.equal(opened.media.length,3);
  await assert.rejects(openProject(f.repoRoot,'../home'));
  await rename(path.join(f.contentRoot,'projects'),path.join(f.contentRoot,'moved'));
  await symlink(path.join(f.contentRoot,'moved'),path.join(f.contentRoot,'projects'));
  await assert.rejects(openProject(f.repoRoot,'project-one'),/ordinary local/);
});

test('proposal ignores unrelated edits, freezes bytes, and rejects stale or unbased changes',async t=>{
 const f=await writeFixture(t),opened=await openProject(f.repoRoot,'project-one'),change=changeFor(opened);
 await f.saveRecord('projects/project-two.json',{...f.raw.projects[1],summary:'Unrelated edit.'});
 change.projects[0].record={...opened.project,summary:'Edited summary'};
 const p=await validateChangeSet(f.repoRoot,change,[]);
 assert.equal(p.writes.length,1);assert.equal(p.writes[0].path,'website/content/projects/project-one.json');
 assert.match(p.digest,/^[a-f0-9]{64}$/);assert.ok(Object.isFrozen(p));
 assert.equal(p.content.review.state,'candidate');
 assert.equal((await validateChangeSet(f.repoRoot,change,[])).digest,p.digest);
 await assert.rejects(validateChangeSet(f.repoRoot,{...change,base:[]},[]),/base/);
 await f.saveRecord('projects/project-one.json',{...opened.project,summary:'External change'});
 await assert.rejects(validateChangeSet(f.repoRoot,change,[]),/changed|stale/);
});

test('strict change-set validation rejects unknown keys, ownership, IDs, stories, promotion hashes and reviewed snapshots',async t=>{
 const f=await writeFixture(t),opened=await openProject(f.repoRoot,'project-one'),change=changeFor(opened);
 await assert.rejects(validateChangeSet(f.repoRoot,{...change,targetPath:'escape'},[]));
 for(const patch of [{id:'../escape'},{albumKeys:['flickr:333'],sourceRefs:f.raw.projects[1].sourceRefs,gallery:[],searchMediaIds:[]},{storyId:'missing'}])
 await assert.rejects(validateChangeSet(f.repoRoot,{...change,projects:[{...change.projects[0],record:{...opened.project,...patch}}]},[]));
 await assert.rejects(validateChangeSet(f.repoRoot,{...change,promotions:[{itemId:'inbox-one',hash:'bad',record:f.raw.media[0]}]},[]));
 await f.saveRecord('reviews/pilot.json',{...f.raw.review,state:'reviewed'});
 await assert.rejects(validateChangeSet(f.repoRoot,change,[]),/candidate|changed/);
});

test('three-album split produces exactly the approved project identities and retires renamed record and story',async t=>{
 const f=await writeFixture(t);
 await f.saveRecord('site.json',{...f.raw.site,navigation:[{label:'Archive',href:'/tradejournals/'}]});
 await f.saveRecord('projects/project-one.json',{...f.raw.projects[0],storyId:'old-story',albumKeys:['flickr:111','flickr:222'],sourceRefs:[...f.raw.projects[0].sourceRefs,{kind:'inventory',path:'albums.md',anchor:'album-222'}]});
 await f.save('website/content/stories/old-story.md','---\nschemaVersion: 1\nid: old-story\n---\n# Old story\n');
 const one=await openProject(f.repoRoot,'project-one'),two=await openProject(f.repoRoot,'project-two');
 const first={...one.project,id:'living-room-studio-restoration',storyId:'living-room-story',albumKeys:['flickr:111'],sourceRefs:f.raw.projects[0].sourceRefs};
 const second={...two.project,id:'office-restoration'};
 const third={...two.project,id:'studio-office-restoration',storyId:'studio-story',albumKeys:['flickr:222'],sourceRefs:[{kind:'inventory',path:'albums.md',anchor:'album-222'}]};
 const change={schemaVersion:1,base:[...one.base,...two.base.filter(d=>!one.base.some(x=>x.kind===d.kind&&x.id===d.id))],projects:[{sourceId:'project-one',record:first,story:{id:first.storyId,markdown:'# Living room\n'}},{sourceId:'project-two',record:second,story:null},{sourceId:null,record:third,story:{id:third.storyId,markdown:''}}],home:{...f.raw.home,featuredProjectIds:[first.id,second.id,third.id]},services:[{...f.raw.services[0],projectIds:[second.id]}],promotions:[]};
 const p=await validateChangeSet(f.repoRoot,change,[]);
 assert.deepEqual(p.content.projects.map(p=>p.id),['living-room-studio-restoration','office-restoration','studio-office-restoration']);
 assert.equal(Object.hasOwn(p.content.stories,'old-story'),false);
 assert.deepEqual(p.removals.map(r=>r.path),['website/content/projects/project-one.json','website/content/projects/project-two.json','website/content/stories/old-story.md']);
 assert.equal(await readFile(path.join(f.contentRoot,'stories/old-story.md'),'utf8'),'---\nschemaVersion: 1\nid: old-story\n---\n# Old story\n');
 const omitted={...change,home:null};await assert.rejects(validateChangeSet(f.repoRoot,omitted,[]),/reference/);
});

test('stories round-trip editable bodies and derive immutable frontmatter for new stories',async t=>{
 const f=await writeFixture(t),body='# A story\n\nBody text.\n';
 await f.saveRecord('projects/project-one.json',{...f.raw.projects[0],storyId:'project-story'});
 await f.save('website/content/stories/project-story.md',`---\nschemaVersion: 1\nid: project-story\n---\n${body}`);
 const opened=await openProject(f.repoRoot,'project-one');
 assert.deepEqual(opened.story,{id:'project-story',markdown:body});
 const change=changeFor(opened);change.projects[0].story={id:'new-story',markdown:''};change.projects[0].record={...opened.project,storyId:'new-story'};
 const p=await validateChangeSet(f.repoRoot,change,[]);
 assert.equal(Buffer.from(p.writes.find(w=>w.kind==='story').bytes,'base64').toString(),'---\nschemaVersion: 1\nid: new-story\n---\n');
 change.projects[0].story.markdown='---\nid: other\n---\n';
 await assert.rejects(validateChangeSet(f.repoRoot,change,[]),/frontmatter/);
 for(const header of ['---\nschemaVersion: 1\nid: wrong\n---\n','---\nschemaVersion: 1\nid: project-story\nextra: true\n---\n','# Missing metadata\n']) {
  await f.save('website/content/stories/project-story.md',header+body);
  await assert.rejects(openProject(f.repoRoot,'project-one'),/frontmatter/);
 }
});

test('unsafe story Markdown is rejected before proposal or source writes',async t=>{
 const f=await writeFixture(t),opened=await openProject(f.repoRoot,'project-one'),change=changeFor(opened);
 change.projects[0].record={...opened.project,storyId:'new-story'};
 for(const markdown of ['<script>alert(1)</script>','[bad](javascript:alert(1))','![private image](file:///tmp/secret.jpg)']) {
  change.projects[0].story={id:'new-story',markdown};
  await assert.rejects(validateChangeSet(f.repoRoot,change,[]),/Markdown|links/);
 }
});

test('tracked file boundary accepts only declared record kinds',async()=>{
 const { trackedPath }=await import('../lib/workbench-files.mjs');
 for(const kind of ['constructor','toString','unknown'])assert.throws(()=>trackedPath({kind,id:'safe-id'}),/identity/);
});

async function renameChange(f) {
 const opened=await openProject(f.repoRoot,'project-one');
 return {schemaVersion:1,base:opened.base,projects:[{sourceId:'project-one',record:{...opened.project,id:'renamed-project'},story:null}],home:{...f.raw.home,featuredProjectIds:['renamed-project']},services:[{...f.raw.services[0],projectIds:['renamed-project']}],promotions:[]};
}

test('project rename derives exact site navigation links and preserves labels and unrelated links',async t=>{
 const f=await writeFixture(t);
 const navigation=[{label:'Recorded work',href:'/work/project-one/'},{label:'Its journal',href:'/tradejournals/project-one/'},{label:'Other project',href:'/work/project-two/'},{label:'All journals',href:'/tradejournals/'}];
 await f.saveRecord('site.json',{...f.raw.site,navigation});
 const change=await renameChange(f),proposal=await validateChangeSet(f.repoRoot,change,[]);
 assert.ok(change.base.some(item=>item.kind==='site'&&item.id==='site'));
 assert.deepEqual(proposal.content.site.navigation,[{label:'Recorded work',href:'/work/renamed-project/'},{label:'Its journal',href:'/tradejournals/renamed-project/'},...navigation.slice(2)]);
 const write=proposal.writes.find(item=>item.kind==='site');
 assert.equal(write.path,'website/content/site.json');
 assert.deepEqual(JSON.parse(Buffer.from(write.bytes,'base64')),proposal.content.site);
 assert.deepEqual(JSON.parse(await readFile(path.join(f.contentRoot,'site.json'))).navigation,navigation);
 assert.equal((await validateChangeSet(f.repoRoot,change,[])).digest,proposal.digest);
 await assert.rejects(validateChangeSet(f.repoRoot,{...change,site:proposal.content.site},[]));
});

test('derived navigation writes require the site base and reject a stale site',async t=>{
 const f=await writeFixture(t),change=await renameChange(f);
 await assert.rejects(validateChangeSet(f.repoRoot,{...change,base:change.base.filter(item=>item.kind!=='site')},[]),/base/);
 await f.saveRecord('site.json',{...f.raw.site,name:'Changed externally'});
 await assert.rejects(validateChangeSet(f.repoRoot,change,[]),/changed|stale/);
});

test('project rename without matching navigation emits no site write or dependency',async t=>{
 const f=await writeFixture(t);
 await f.saveRecord('site.json',{...f.raw.site,navigation:[{label:'Other project',href:'/work/project-two/'},{label:'Home',href:'/'}]});
 const change=await renameChange(f),proposal=await validateChangeSet(f.repoRoot,change,[]);
 assert.ok(!change.base.some(item=>item.kind==='site'));
 assert.ok(!proposal.writes.some(item=>item.kind==='site'));
 assert.deepEqual(proposal.content.site.navigation,[{label:'Other project',href:'/work/project-two/'},{label:'Home',href:'/'}]);
});
