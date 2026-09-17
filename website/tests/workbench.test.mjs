import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, symlink, mkdir, rename } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';
import { writeFixture } from './fixtures.mjs';
import { openCandidate, saveCandidate } from '../lib/workbench.mjs';

test('candidate editing preserves copy, order, overrides and review state; stale saves fail', async t => {
  const f = await writeFixture(t);
  const before = await openCandidate(f.repoRoot, 'project-one');
  const gallery = [{ mediaId:'photo-two', caption:'Second surface first', alt:'Two boards', role:'context' }, ...before.project.gallery];
  await saveCandidate(f.repoRoot, { projectId:'project-one', revision:before.revision, gallery });
  const after = await openCandidate(f.repoRoot, 'project-one');
  assert.deepEqual(after.project.gallery, gallery);
  assert.equal(after.project.summary, before.project.summary);
  assert.deepEqual(after.project.searchMediaIds, ['photo-two', 'photo-one']);
  assert.equal(JSON.parse(await readFile(path.join(f.contentRoot,'reviews/pilot.json'))).state, 'candidate');
  await assert.rejects(saveCandidate(f.repoRoot, {projectId:'project-one',revision:before.revision,gallery:[]}), /changed/);
});

test('invalid selection and reviewed snapshots cannot be overwritten', async t => {
  const f=await writeFixture(t), before=await openCandidate(f.repoRoot,'project-one');
  await assert.rejects(saveCandidate(f.repoRoot,{projectId:'project-one',revision:before.revision,gallery:[{mediaId:'missing',caption:'Image',role:'detail'}]}));
  await f.saveRecord('reviews/pilot.json',{...f.raw.review,state:'reviewed'});
  await assert.rejects(saveCandidate(f.repoRoot,{projectId:'project-one',revision:before.revision,gallery:[]}), /candidate|changed/);
  assert.deepEqual((await openCandidate(f.repoRoot,'project-one')).project.gallery,before.project.gallery);
});

test('unsafe IDs and symlinked content directories are refused', async t => {
  const f=await writeFixture(t);
  await assert.rejects(openCandidate(f.repoRoot,'../home'));
  const before=await openCandidate(f.repoRoot,'project-one');
  await assert.rejects(saveCandidate(f.repoRoot,{projectId:'project-one',revision:before.revision,gallery:[],promotions:[{id:'../../escape'}]}));
  const other=path.join(f.repoRoot,'other'); await mkdir(other);
  await rename(path.join(f.contentRoot,'projects'),path.join(other,'projects'));
  await symlink(path.join(other,'projects'),path.join(f.contentRoot,'projects'));
  await assert.rejects(openCandidate(f.repoRoot,'project-one'), /ordinary local/);
});

test('promotion adds only selected bytes and keeps the other project untouched', async t => {
  const f=await writeFixture(t),before=await openCandidate(f.repoRoot,'project-one');
  const untouched=await readFile(path.join(f.contentRoot,'projects/project-two.json'));
  const bytes=Buffer.from('synthetic prepared image'),id='studio-'+createHash('sha256').update(bytes).digest('hex');
  const record={...f.raw.media[0],id,assetPath:`website/assets/workbench/${id}.jpg`};
  const gallery=[{mediaId:id,caption:'Selected evidence',alt:'Synthetic image',role:'detail'}];
  const saved=await saveCandidate(f.repoRoot,{projectId:'project-one',revision:before.revision,gallery,promotions:[{record,bytes}]});
  assert.deepEqual(saved.project.gallery,gallery);
  assert.deepEqual(await readFile(path.join(f.repoRoot,record.assetPath)),bytes);
  assert.deepEqual(await readFile(path.join(f.contentRoot,'projects/project-two.json')),untouched);
  assert.equal(saved.state,'candidate');
  await assert.rejects(saveCandidate(f.repoRoot,{projectId:'project-one',revision:saved.revision,gallery:[],promotions:[{record,bytes}]}),/Select only/);
});
