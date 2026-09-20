// Archive-side authoring. Private draft persistence and HTTP belong to the caller.
import path from 'node:path';
import { readFile, realpath, chmod, readdir, lstat, symlink } from 'node:fs/promises';
import { buildWebsite } from '../scripts/build.mjs';
import { z } from 'zod';
import { createSatteriMarkdownProcessor } from '@astrojs/markdown-satteri';
import { assertSafeMarkdownTree } from './markdown-policy.mjs';
import { loadContent, validateContent } from './content.mjs';
import { StableId, schemas } from './schema.mjs';
import { hash, fail, key, readTracked, fingerprintTracked, trackedPath, confined, durableWrite, syncDirectory, writeTemporary, replaceTracked, inspectTracked, removeTracked } from './workbench-files.mjs';
const contentRoot = root => path.join(root,'website/content');
async function load(root) {
  const records=validateContent(await loadContent(contentRoot(root)));
  await Promise.all([{kind:'site',id:'site'},{kind:'home',id:'home'},{kind:'review',id:'pilot'},...records.projects.map(p=>({kind:'project',id:p.id})),...records.services.map(s=>({kind:'service',id:s.id})),...records.media.map(m=>({kind:'media',id:m.id}))].map(d=>readTracked(root,d)));
  return records;
}
export async function readCatalog(root) {
  const content=await load(root);
  return {projects:content.projects,albumOwners:Object.fromEntries(content.projects.flatMap(p=>p.albumKeys.map(a=>[a,p.id]))),reviewState:content.review.state};
}
export async function openProject(root, projectId) {
  StableId.parse(projectId);const content=await load(root),project=content.projects.find(p=>p.id===projectId);
  if(!project)throw fail('Website project not found.');
  const media=content.media.filter(m=>project.albumKeys.includes(m.albumKey));
  const references={home:content.home.featuredProjectIds.includes(projectId)?content.home:null,services:content.services.filter(s=>s.projectIds.includes(projectId))};
  const descriptors=[{kind:'project',id:projectId},{kind:'review',id:'pilot'},...media.map(m=>({kind:'media',id:m.id})),...references.services.map(s=>({kind:'service',id:s.id}))];
  if(references.home)descriptors.push({kind:'home',id:'home'});
  if(content.site.navigation.some(link=>projectRoutes(projectId).includes(link.href)))descriptors.push({kind:'site',id:'site'});
  let story=null;
  if(project.storyId){const bytes=await readTracked(root,{kind:'story',id:project.storyId});if(bytes===null)throw fail('Missing project story.');story={id:project.storyId,markdown:parseStory(project.storyId,bytes.toString('utf8'))};descriptors.push({kind:'story',id:project.storyId});}
  return {project,story,media,references,base:await fingerprintTracked(root,descriptors)};
}
const sha = z.string().regex(/^[a-f0-9]{64}$/);
const descriptor = z.strictObject({kind:z.enum(['project','service','media','story','home','site','review','asset']),id:StableId,sha256:sha.nullable()});
const changeSchema = z.strictObject({
  schemaVersion:z.literal(1),base:z.array(descriptor),
  projects:z.array(z.strictObject({sourceId:StableId.nullable(),record:schemas.project,story:z.strictObject({id:StableId,markdown:z.string()}).nullable()})),
  home:schemas.home.nullable(),services:z.array(schemas.service),
  promotions:z.array(z.strictObject({itemId:StableId,hash:sha,record:schemas.media}))
});
const canonical = value => JSON.stringify(value,(_,v)=>v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.keys(v).sort().map(k=>[k,v[k]])):v);
const jsonBytes = value => Buffer.from(`${JSON.stringify(value,null,2)}\n`);
const projectRoutes = id => [`/work/${id}/`,`/tradejournals/${id}/`];
function remapSiteNavigation(site,renames) {
  const hrefs=new Map([...renames].flatMap(([sourceId,id])=>projectRoutes(sourceId).map((href,index)=>[href,projectRoutes(id)[index]])));
  let changed=false;
  const navigation=site.navigation.map(link=>{
    const href=hrefs.get(link.href);
    if(href===undefined)return link;
    changed=true;
    return {...link,href};
  });
  return changed?{...site,navigation}:site;
}
function freeze(value) {if(value&&typeof value==='object'){Object.values(value).forEach(freeze);Object.freeze(value);}return value;}
async function checkBase(root,base) {
  const actual=await fingerprintTracked(root,base);
  const expected=new Map(base.map(d=>[key(d),d.sha256]));
  if(actual.some(d=>d.sha256!==expected.get(key(d))))throw fail('Website records changed; the draft is stale.');
}
let storyRenderer;
async function verifyContent(root,content,stories,assets=new Set()) {
  validateContent(content);
  for(const project of content.projects){
    if(project.storyId) {
      if(!Object.hasOwn(stories,project.storyId))throw fail('Missing project story.');
      storyRenderer ??= createSatteriMarkdownProcessor({syntaxHighlight:false,mdastPlugins:[{name:'safe-markdown',before:assertSafeMarkdownTree}]});
      await (await storyRenderer).render(parseStory(project.storyId,stories[project.storyId]));
    }
    for(const ref of project.sourceRefs)await readFile(await confined(root,ref.path));
  }
  const selected=new Set(content.projects.flatMap(p=>[...p.gallery.map(g=>g.mediaId),...p.searchMediaIds]));
  if(content.home.heroMediaId)selected.add(content.home.heroMediaId);
  for(const media of content.media.filter(m=>selected.has(m.id)))if(!assets.has(media.id))await readFile(await confined(root,media.assetPath));
  const destinations=new Set(['/', '/tradejournals/', '/search.json',...content.projects.flatMap(p=>[`/work/${p.id}/`,`/tradejournals/${p.id}/`])]);
  for(const link of content.site.navigation)if(!destinations.has(new URL(link.href,'https://website.invalid').pathname))throw fail('Missing navigation reference.');
}
function parseStory(id, markdown) {
  const match=/^---\r?\n([\s\S]*?)\r?\n---\r?\n/.exec(markdown);
  if(!match)throw fail('Missing or malformed story frontmatter.');
  const lines=match[1].split(/\r?\n/);
  if(lines.length!==2||!lines.includes('schemaVersion: 1')||!lines.includes(`id: ${id}`))throw fail('Mismatched or extra story frontmatter.');
  return markdown.slice(match[0].length);
}
function storyBytes(story) {
  if(/^\s*---(?:\r?\n|$)/.test(story.markdown))throw fail('Editable story body must not include frontmatter.');
  const body=story.markdown.replace(/(?:\r?\n)+$/u,'');
  return Buffer.from(`---\nschemaVersion: 1\nid: ${story.id}\n---\n${body}${body?'\n':''}`);
}
async function readStories(root,content) {
  const stories={};
  for(const id of new Set(content.projects.flatMap(p=>p.storyId?[p.storyId]:[]))){const bytes=await readTracked(root,{kind:'story',id});if(bytes===null)throw fail('Missing project story.');parseStory(id,bytes.toString('utf8'));stories[id]=bytes.toString('utf8');}
  return stories;
}
export async function validateChangeSet(root,input,assets=[]) {
  const change=changeSchema.parse(input),content=await load(root);
  if(content.review.state!=='candidate')throw fail('Only candidate content can be edited here.');
  if(new Set(change.base.map(key)).size!==change.base.length)throw fail('Duplicate base descriptor.');
  await checkBase(root,change.base);
  const supplied=new Map(change.base.map(d=>[key(d),d]));
  const requireBase=async d=>{const bytes=await readTracked(root,d);if(bytes!==null&&!supplied.has(key(d)))throw fail(`Missing base fingerprint for ${key(d)}.`);};
  await requireBase({kind:'review',id:'pilot'});
  const stories=await readStories(root,content),mutations=new Map(),retire=new Map();
  const put=(kind,id,bytes)=>{const d={kind,id};if(mutations.has(key(d)))throw fail('Duplicate replacement identity.');mutations.set(key(d),{...d,bytes});};
  const seenSources=new Set();
  const renames=new Map();
  for(const item of change.projects){
    const {sourceId,record,story}=item;
    if(sourceId!==null){
      if(seenSources.has(sourceId))throw fail('Duplicate source project.');seenSources.add(sourceId);
      const old=content.projects.find(p=>p.id===sourceId);if(!old)throw fail('Source project is missing.');
      const opened=await openProject(root,sourceId);for(const d of opened.base)await requireBase(d);
      if(sourceId!==record.id){retire.set(`project:${sourceId}`,{kind:'project',id:sourceId});renames.set(sourceId,record.id);}
      if(old.storyId&&old.storyId!==record.storyId)retire.set(`story:${old.storyId}`,{kind:'story',id:old.storyId});
    }
    if(record.id!==sourceId&&content.projects.some(p=>p.id===record.id))throw fail('Replacement project already exists.');
    if(story?.id!==record.storyId && (story!==null||record.storyId))throw fail('Missing or mismatched project story.');
    if(story){const bytes=storyBytes(story);stories[story.id]=bytes.toString('utf8');put('story',story.id,bytes);}
    put('project',record.id,jsonBytes(record));
    if(renames.has(sourceId))mutations.get(`project:${record.id}`).sourceId=sourceId;
  }
  const site=remapSiteNavigation(content.site,renames);
  if(site!==content.site){await requireBase({kind:'site',id:'site'});content.site=site;put('site','site',jsonBytes(site));}
  content.projects=content.projects.filter(p=>!seenSources.has(p.id)).concat(change.projects.map(p=>p.record)).sort((a,b)=>a.id.localeCompare(b.id));
  if(change.home){content.home=change.home;put('home','home',jsonBytes(change.home));}
  for(const service of change.services){if(!content.services.some(s=>s.id===service.id))throw fail('Service replacement is missing.');content.services=content.services.map(s=>s.id===service.id?service:s);put('service',service.id,jsonBytes(service));}
  const promoted=new Set();
  for(const promotion of change.promotions){
    const {record,itemId}=promotion,asset=assets.find(a=>a.itemId===itemId);
    if(promoted.has(record.id)||!asset||!Buffer.isBuffer(asset.bytes)||asset.bytes.length<1||asset.bytes.length>25*1024*1024||hash(asset.bytes)!==promotion.hash)throw fail('Invalid promotion hash or prepared bytes.');
    if(record.id!==`studio-${promotion.hash}`||record.assetPath!==trackedPath({kind:'asset',id:record.id})||record.kind!=='evidence')throw fail('Invalid promoted media identity.');
    if(!content.projects.some(p=>p.albumKeys.includes(record.albumKey)&&[...p.gallery.map(g=>g.mediaId),...p.searchMediaIds].includes(record.id)))throw fail('Select only promoted project evidence.');
    const existing=content.media.find(m=>m.id===record.id);
    if(existing&&canonical(existing)!==canonical(record))throw fail('Existing media record differs.');
    if(!existing)content.media.push(record);
    put('media',record.id,jsonBytes(record));put('asset',record.id,asset.bytes);promoted.add(record.id);
  }
  for(const [k,d] of retire)if(d.kind==='story') {
    if(content.projects.some(p=>p.storyId===d.id))retire.delete(k);
    else delete stories[d.id];
  }
  await verifyContent(root,content,stories,promoted);
  const writes=[],removals=[];
  for(const entry of mutations.values()){
    await requireBase(entry);const beforeBytes=await readTracked(root,entry),afterBytes=entry.bytes;
    if(beforeBytes!==null&&(beforeBytes.equals(afterBytes)||(entry.kind!=='story'&&entry.kind!=='asset'&&canonical(JSON.parse(beforeBytes))===canonical(JSON.parse(afterBytes)))))continue;
    if(entry.kind==='asset'&&beforeBytes!==null)throw fail('Existing asset differs.');
    writes.push({kind:entry.kind,id:entry.id,...(entry.sourceId?{sourceId:entry.sourceId}:{}),path:trackedPath(entry),before:beforeBytes===null?null:hash(beforeBytes),after:hash(afterBytes),bytes:afterBytes.toString('base64')});
  }
  for(const entry of retire.values()){await requireBase(entry);const bytes=await readTracked(root,entry);if(bytes!==null)removals.push({...entry,path:trackedPath(entry),before:hash(bytes)});}
  writes.sort((a,b)=>a.path.localeCompare(b.path));removals.sort((a,b)=>a.path.localeCompare(b.path));
  const base=await fingerprintTracked(root,[...change.base,...writes,...removals]);
  const payload={base,writes,removals,content:{...content,stories}};
  return freeze({digest:hash(canonical(payload)),...payload});
}

function verifyProposal(proposal) {
  const {digest,...payload}=proposal;
  if(!sha.safeParse(digest).success||hash(canonical(payload))!==digest)throw fail('Proposal digest mismatch.');
  if(Object.keys(payload).sort().join(',')!=='base,content,removals,writes')throw fail('Invalid proposal shape.');
  const base=z.array(descriptor).parse(proposal.base);
  const seen=new Set();
  const renamedSources=new Set();
  for(const entry of [...proposal.writes,...proposal.removals]) {
    if(!['project','service','media','story','home','site','asset'].includes(entry.kind)||entry.path!==trackedPath(entry))throw fail('Invalid proposal target.');
    if(seen.has(key(entry)))throw fail('Duplicate proposal target.');seen.add(key(entry));
    if(!base.some(d=>key(d)===key(entry)&&d.sha256===entry.before))throw fail('Proposal target has no matching base.');
    if(entry.sourceId!==undefined){
      // Recovery may have removed the source already; prove it existed from its saved before-hash.
      if(entry.kind!=='project'||!StableId.safeParse(entry.sourceId).success||entry.sourceId===entry.id||entry.before!==null||entry.bytes===undefined||renamedSources.has(entry.sourceId)||!proposal.removals.some(removal=>removal.kind==='project'&&removal.id===entry.sourceId&&sha.safeParse(removal.before).success))throw fail('Invalid project rename identity.');
      renamedSources.add(entry.sourceId);
    }
    if(entry.bytes!==undefined) {
      const bytes=Buffer.from(entry.bytes,'base64');
      if(hash(bytes)!==entry.after)throw fail('Proposal byte hash mismatch.');
      if(entry.kind==='story') {
        parseStory(entry.id,bytes.toString('utf8'));
        if(proposal.content.stories[entry.id]!==bytes.toString('utf8'))throw fail('Proposal story differs from content.');
      } else if(entry.kind==='asset') {
        if(entry.before!==null||entry.id!==`studio-${entry.after}`)throw fail('Invalid additive asset identity.');
      } else {
        const record=schemas[entry.kind].parse(JSON.parse(bytes));
        if(record.id!==entry.id)throw fail('Proposal record identity mismatch.');
        const group={project:'projects',service:'services',media:'media'}[entry.kind];
        const expected=group?proposal.content[group].find(r=>r.id===entry.id):proposal.content[entry.kind];
        if(canonical(record)!==canonical(expected))throw fail('Proposal bytes differ from proposed content.');
        if(entry.kind==='media'&&entry.before!==null)throw fail('Media promotion must be additive.');
      }
    } else if(!['project','story'].includes(entry.kind))throw fail('Invalid proposal removal.');
  }
  if(proposal.writes.some(entry=>entry.kind==='site')&&!renamedSources.size)throw fail('Site writes require derived project navigation.');
  if(proposal.content.review.state!=='candidate')throw fail('Only candidate content can be edited here.');
  validateContent(proposal.content);
}
async function privateDirectory(root, parent, id) {
  if(typeof parent!=='string'||!path.isAbsolute(parent))throw fail('Private root must be absolute.');
  const repo=await realpath(root),resolved=path.resolve(parent);
  // A caller-owned workspace can be inside the checkout, but never in website or Git inputs.
  for(const protectedRoot of [path.join(repo,'website'),path.join(repo,'.git')]) {
    const relative=path.relative(protectedRoot,resolved);
    if(relative===''||(!relative.startsWith(`..${path.sep}`)&&relative!=='..'&&!path.isAbsolute(relative)))throw fail('Private workspace overlaps canonical website files.');
  }
  const absolute=path.join(resolved,id);
  // Walk from the filesystem root to reject symlink ancestors before mkdir.
  await confined(path.parse(absolute).root,absolute.slice(path.parse(absolute).root.length)+'/marker',true);
  const actual=await realpath(absolute);
  if(actual!==absolute)throw fail('Private workspace must use ordinary local directories.');
  await chmod(absolute,0o700);
  return absolute;
}
async function overlayCurrent(root,proposal) {
  const current=await loadContent(contentRoot(root));
  const renames=new Map(proposal.writes.filter(entry=>entry.kind==='project'&&entry.sourceId!==undefined).map(entry=>[entry.sourceId,entry.id]));
  const derivedSite=remapSiteNavigation(current.site,renames);
  const stories=await readStories(root,{...current,projects:current.projects.filter(p=>![...proposal.removals,...proposal.writes].some(r=>r.kind==='story'&&r.id===p.storyId))});
  const groups={project:'projects',service:'services',media:'media'};
  for(const entry of proposal.writes){
    const bytes=Buffer.from(entry.bytes,'base64');
    if(groups[entry.kind]){const group=groups[entry.kind];current[group]=current[group].filter(r=>r.id!==entry.id).concat(JSON.parse(bytes));}
    if(entry.kind==='home')current.home=JSON.parse(bytes);
    if(entry.kind==='site'){
      if(canonical(JSON.parse(bytes))!==canonical(derivedSite))throw fail('Site write must match derived project navigation.');
      current.site=derivedSite;
    }
    if(entry.kind==='story')stories[entry.id]=bytes.toString('utf8');
  }
  for(const entry of proposal.removals){if(groups[entry.kind])current[groups[entry.kind]]=current[groups[entry.kind]].filter(r=>r.id!==entry.id);if(entry.kind==='story')delete stories[entry.id];}
  if(current.review.state!=='candidate')throw fail('Only candidate content can be edited here.');
  await verifyContent(root,current,stories,new Set(proposal.writes.filter(w=>w.kind==='asset').map(w=>w.id)));
  // Collection order is not content; every record and story must otherwise
  // equal the canonical overlay. A recomputed digest alone proves no origin.
  const normalized=content=>({
    ...content,
    ...Object.fromEntries(['projects','services','media'].map(group=>[
      group,[...content[group]].sort((a,b)=>a.id.localeCompare(b.id))
    ]))
  });
  const reconstructed=normalized({...current,stories});
  if(canonical(reconstructed)!==canonical(normalized(proposal.content)))throw fail('Proposal content differs from the canonical overlay. Revalidate the change set.');
  return reconstructed;
}
export async function stagePublication(root,proposal,{operationRoot,assets=[]}) {
  verifyProposal(proposal);await checkBase(root,proposal.base);await overlayCurrent(root,proposal);
  const directory=await privateDirectory(root,operationRoot,proposal.digest);
  // Reconstruct every expected snapshot while the canonical base still matches.
  // This also repairs incomplete metadata left by an interrupted older writer.
  const writes=[],removals=[];
  for(const [index,entry] of [...proposal.writes,...proposal.removals].entries()) {
    const beforeBytes=await readTracked(root,entry);
    const beforeSnapshot=beforeBytes===null?null:`snapshots/${index}-before`;
    if(beforeBytes!==null)await snapshotWrite(directory,beforeSnapshot,beforeBytes);
    const {bytes,...identity}=entry;
    if(bytes!==undefined){const snapshot=`snapshots/${index}-after`;await snapshotWrite(directory,snapshot,Buffer.from(bytes,'base64'));writes.push({...identity,snapshot,beforeSnapshot});}
    else removals.push({...identity,beforeSnapshot});
  }
  await snapshotWrite(directory,'proposal.json',jsonBytes(proposal));
  const manifest={schemaVersion:1,proposalDigest:proposal.digest,phase:'staged',operationRoot:directory,base:proposal.base,writes,removals};
  await snapshotWrite(directory,'manifest.json',jsonBytes(manifest));
  await syncDirectory(directory);return manifest;
}
async function snapshotWrite(root,relative,bytes) {
  return durableWrite(root,relative,bytes,{repairIncomplete:true});
}
async function readOperation(input) {
  const directory=input?.operationRoot;
  if(typeof directory!=='string'||!path.isAbsolute(directory))throw fail('Invalid operation root.');
  const manifest=JSON.parse(await readFile(await confined(directory,'manifest.json'),'utf8'));
  if(canonical(input)!==canonical(manifest))throw fail('Publication manifest differs from its durable snapshot.');
  const proposal=JSON.parse(await readFile(await confined(directory,'proposal.json'),'utf8'));
  verifyProposal(proposal);
  if(manifest.schemaVersion!==1||manifest.phase!=='staged'||manifest.proposalDigest!==proposal.digest||canonical(manifest.base)!==canonical(proposal.base))throw fail('Invalid publication manifest.');
  if(manifest.writes.length!==proposal.writes.length||manifest.removals.length!==proposal.removals.length)throw fail('Invalid publication targets.');
  for(const [index,entry] of [...manifest.writes,...manifest.removals].entries()) {
    const expected=[...proposal.writes,...proposal.removals][index];
    const {snapshot,beforeSnapshot,...identity}=entry,{bytes,...expectedIdentity}=expected;
    if(canonical(identity)!==canonical(expectedIdentity)||beforeSnapshot!==(entry.before===null?null:`snapshots/${index}-before`)||(bytes!==undefined&&snapshot!==`snapshots/${index}-after`))throw fail('Invalid publication snapshot identity.');
    for(const [relative,digest] of [[beforeSnapshot,entry.before],[snapshot,entry.after]])if(relative&&hash(await readFile(await confined(directory,relative)))!==digest)throw fail('Publication snapshot hash mismatch.');
  }
  return {manifest,proposal};
}
export async function inspectPublication(root,input) {
  const {manifest}=await readOperation(input);
  const files=await Promise.all([...manifest.writes,...manifest.removals.map(r=>({...r,after:null}))].map(entry=>inspectTracked(root,entry)));
  if(files.some(f=>f.state==='conflict'))throw fail('Publication conflict: canonical files changed outside the operation.');
  return {state:files.every(f=>f.state==='after')?'applied':files.every(f=>f.state==='before')?'not-started':'partial',files};
}
export async function applyPublication(root,input,{beforeTargetMutation,afterReplace}={}) {
  const {manifest,proposal}=await readOperation(input),inspection=await inspectPublication(root,manifest);
  const targets=new Map([...manifest.writes,...manifest.removals].map(e=>[key(e),e]));
  // Unchanged dependencies still must match, even when recovering a partial operation.
  await checkBase(root,manifest.base.filter(d=>!targets.has(key(d))));
  if(inspection.state!=='applied') {
    await overlayCurrent(root,proposal);
    const ordered=[...manifest.writes].sort((a,b)=>(a.kind==='asset'?0:1)-(b.kind==='asset'?0:1)||a.path.localeCompare(b.path));
    for(const entry of [...ordered,...manifest.removals.map(r=>({...r,after:null}))]) {
      const state=await inspectTracked(root,entry);
      if(state.state==='after')continue;
      if(state.state!=='before')throw fail('Publication conflict: target changed during apply.');
      if(entry.after===null) {
        await beforeTargetMutation?.({kind:entry.kind,id:entry.id,path:entry.path});
        await removeTracked(root,entry);
      } else {
        const stagedWrite=await writeTemporary(root,manifest.operationRoot,entry);
        await beforeTargetMutation?.({kind:entry.kind,id:entry.id,path:entry.path});
        await replaceTracked(root,stagedWrite);
      }
      await afterReplace?.({kind:entry.kind,id:entry.id,path:entry.path});
    }
  }
  if((await inspectPublication(root,manifest)).state!=='applied')throw fail('Publication verification failed.');
  const receipt={proposalDigest:manifest.proposalDigest,sourceApplied:true};
  await snapshotWrite(manifest.operationRoot,'receipt.json',jsonBytes(receipt));
  return receipt;
}
/** Call only after applyPublication has returned a verified source receipt. */
export async function buildCanonicalPreview(root) {
  try {
    const result=await buildWebsite({mode:'preview',repoRoot:root,websiteRoot:path.join(root,'website')});
    return {sourceApplied:true,candidatePreview:'built',outputRoot:result.outputRoot,report:result.report};
  }catch {
    return {sourceApplied:true,candidatePreview:'failed',message:'Source update is applied. Rebuild the local candidate preview; do not publish the source update again.'};
  }
}

async function copyApplication(source, destination, relative) {
  const info=await lstat(path.join(source,relative));
  if(info.isSymbolicLink())throw fail('Preview application inputs must be ordinary local files.');
  if(info.isDirectory()) {
    for(const name of await readdir(path.join(source,relative)))await copyApplication(source,destination,`${relative}/${name}`);
  } else if(info.isFile())await durableWrite(destination,relative,await readFile(await confined(source,relative)));
  else throw fail('Unsupported preview application input.');
}
/** Snapshot the renderer too: Astro's caches and generated types must remain private. */
export async function buildPrivatePreview(root,proposal,{previewRoot,assets=[]}) {
  verifyProposal(proposal);await checkBase(root,proposal.base);
  // Render only the verified reconstruction, never caller-supplied extra content.
  const content=await overlayCurrent(root,proposal);
  const directory=await privateDirectory(root,previewRoot,proposal.digest);
  try {
    const receipt=JSON.parse(await readFile(await confined(directory,'preview.json'),'utf8'));
    if(receipt.digest!==proposal.digest||receipt.outputRoot!==path.join(directory,'output'))throw fail('Private preview receipt differs.');
    return receipt;
  }catch(error){if(error.code!=='ENOENT')throw error;}
  if((await readdir(directory)).length)throw fail('Private preview is incomplete. Use a fresh caller preview root to retry.');
  for(const kind of ['site','home','review'])await durableWrite(directory,`content/${kind==='review'?'reviews/pilot':kind}.json`,jsonBytes(content[kind]));
  for(const group of ['projects','services','media'])for(const record of content[group])await durableWrite(directory,`content/${group}/${record.id}.json`,jsonBytes(record));
  for(const [id,markdown] of Object.entries(content.stories))await durableWrite(directory,`content/stories/${id}.md`,Buffer.from(markdown));
  // Empty story collections still need a local directory for Astro's loader.
  await confined(directory,'content/stories/marker',true);
  const overrides=new Map();
  for(const entry of proposal.writes.filter(w=>w.kind==='asset'))overrides.set(entry.id,await durableWrite(directory,`assets/${entry.id}.jpg`,Buffer.from(entry.bytes,'base64')));
  const application=await privateDirectory(root,directory,'application'),website=path.join(root,'website');
  for(const relative of ['src','lib','astro.config.mjs','package.json'])await copyApplication(website,application,relative);
  // Link dependencies individually, leaving node_modules/.astro and Vite caches private.
  await confined(application,'node_modules/marker',true);
  for(const name of await readdir(path.join(website,'node_modules'))) {
    if(name.startsWith('.'))continue;
    await symlink(await realpath(path.join(website,'node_modules',name)),path.join(application,'node_modules',name));
  }
  const result=await buildWebsite({mode:'preview',repoRoot:root,websiteRoot:application,contentRoot:path.join(directory,'content'),contentBoundaryRoot:directory,generatedRoot:path.join(directory,'generated'),modelPath:path.join(directory,'site.json'),publicRoot:path.join(directory,'public'),outputRoot:path.join(directory,'output'),assetOverrides:overrides});
  const receipt={digest:proposal.digest,outputRoot:result.outputRoot,report:result.report,urlPath:`/website/previews/${proposal.digest}/`};
  await durableWrite(directory,'preview.json',jsonBytes(receipt));return receipt;
}
