// Local authoring adapter. Astro never imports this module or private media.
import { createHash, randomUUID } from 'node:crypto';
import { lstat, mkdir, open, readFile, realpath, rename } from 'node:fs/promises';
import path from 'node:path';
import { loadContent, validateContent } from './content.mjs';
import { StableId, parseRecord } from './schema.mjs';

const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const json = value => `${JSON.stringify(value,null,2)}\n`;
const fail = message => Object.assign(new Error(message), {safe:true,status:409,code:'website-candidate'});

async function confined(root, relative, create = false) {
  let target = await realpath(root);
  for (const [i,part] of relative.split('/').entries()) {
    if (!part || ['.','..'].includes(part)) throw fail('Invalid website path.');
    target=path.join(target,part);
    let info=await lstat(target).catch(error=>{if(error.code!=='ENOENT')throw error;return null;});
    if (!info && create && i < relative.split('/').length-1) {await mkdir(target);info=await lstat(target);}
    if (info?.isSymbolicLink() || (info && i<relative.split('/').length-1 && !info.isDirectory()) || (info?.isFile() && info.nlink!==1)) throw fail('Website paths must be ordinary local files and directories.');
    if (!info && !create) throw fail('Required website files are unavailable.');
  }
  return target;
}

export async function openCandidate(root, projectId) {
  StableId.parse(projectId);
  await confined(root,`website/content/projects/${projectId}.json`);
  const records=validateContent(await loadContent(path.join(root,'website/content')));
  const project=records.projects.find(item=>item.id===projectId);
  if (!project) throw fail('Website project not found.');
  return {project,media:records.media.filter(item=>project.albumKeys.includes(item.albumKey)),revision:hash(JSON.stringify(records)),state:records.review.state};
}

async function addFile(root, relative, bytes) {
  const target=await confined(root,relative,true);
  let handle;
  try {handle=await open(target,'wx',0o644);await handle.writeFile(bytes);await handle.sync();}
  catch(error) {if(error.code!=='EEXIST')throw error;if(!(await readFile(target)).equals(Buffer.from(bytes)))throw fail('An existing website asset differs. Nothing was replaced.');}
  finally {await handle?.close();}
}

/** Additive media is installed first; one atomic project replacement selects it.
 * Interrupted saves can leave unselected assets, never a half-written project.
 * Caller serializes mutations. External editors are detected by revision checks.
 */
export async function saveCandidate(root, {projectId,revision,gallery,promotions=[]}) {
  const before=await openCandidate(root,projectId);
  if (before.state!=='candidate') throw fail('Only candidate content can be edited here.');
  if (revision!==before.revision) throw fail('Website records changed. Reopen the project before saving.');
  if (!Array.isArray(gallery)||gallery.length>50||!Array.isArray(promotions)||promotions.length>50) throw fail('Select at most 50 photos.');
  const records=validateContent(await loadContent(path.join(root,'website/content')));
  const project=parseRecord('project',{...before.project,gallery,searchMediaIds:gallery.map(item=>item.mediaId)},projectId);
  const additions=[];
  for(const promotion of promotions) {
    const {record,bytes}=promotion??{};
    if (!Buffer.isBuffer(bytes)||bytes.length<1||bytes.length>25*1024*1024) throw fail('A prepared JPEG is required.');
    const media=parseRecord('media',record,'promotion');
    if (media.id!==`studio-${hash(bytes)}`||media.assetPath!==`website/assets/workbench/${media.id}.jpg`||!project.albumKeys.includes(media.albumKey)||!gallery.some(item=>item.mediaId===media.id)) throw fail('Select only prepared photos for this project.');
    const existing=records.media.find(item=>item.id===media.id);
    if(existing&&JSON.stringify(existing)!==JSON.stringify(media))throw fail('This photo already has a different public record. Reopen the saved candidate.');
    if(!existing){records.media.push(media);additions.push({record:media,bytes});}
  }
  records.projects=records.projects.map(item=>item.id===projectId?project:item);
  validateContent(records);
  for(const item of additions){
    await addFile(root,item.record.assetPath,item.bytes);
    await addFile(root,`website/content/media/${item.record.id}.json`,json(item.record));
  }
  // Ignore our own additive records while detecting edits to preexisting records.
  const current=await loadContent(path.join(root,'website/content'));
  current.media=current.media.filter(item=>!additions.some(added=>added.record.id===item.id));
  if(hash(JSON.stringify(validateContent(current)))!==before.revision)throw fail('Website records changed during save. Reopen the project.');
  const target=await confined(root,`website/content/projects/${projectId}.json`);
  const temporary=await confined(root,`website/content/projects/.${projectId}-${randomUUID()}.tmp`,true);
  const handle=await open(temporary,'wx',0o644);
  try{await handle.writeFile(json(project));await handle.sync();}finally{await handle.close();}
  await rename(temporary,target);
  return openCandidate(root,projectId);
}
