// File identities are derived here; callers never choose canonical target paths.
import { createHash, randomUUID } from 'node:crypto';
import { lstat, mkdir, open, readFile, realpath, rename, unlink } from 'node:fs/promises';
import path from 'node:path';
import { StableId } from './schema.mjs';

export const hash = bytes => createHash('sha256').update(bytes).digest('hex');
export const fail = message => Object.assign(new Error(message), {
  safe: true, status: 409, code: 'website-candidate'
});
export const key = descriptor => `${descriptor.kind}:${descriptor.id}`;

export function trackedPath({ kind, id }) {
  StableId.parse(id);
  const groups = { project: 'projects', service: 'services', media: 'media', story: 'stories' };
  if (Object.hasOwn(groups, kind)) return `website/content/${groups[kind]}/${id}.${kind === 'story' ? 'md' : 'json'}`;
  if (kind === 'home' && id === 'home') return 'website/content/home.json';
  if (kind === 'site' && id === 'site') return 'website/content/site.json';
  if (kind === 'review' && id === 'pilot') return 'website/content/reviews/pilot.json';
  if (kind === 'asset' && /^studio-[a-f0-9]{64}$/.test(id)) return `website/assets/workbench/${id}.jpg`;
  throw fail('Invalid tracked record identity.');
}

export async function confined(root, relative, create = false) {
  if (typeof relative !== 'string' || relative.split('/').some(part => !part || part === '.' || part === '..') || /[\\\u0000]/.test(relative)) {
    throw fail('Invalid website path.');
  }
  let target = await realpath(root);
  const parts = relative.split('/');
  for (const [index, part] of parts.entries()) {
    target = path.join(target, part);
    let info = await lstat(target).catch(error => {
      if (error.code !== 'ENOENT') throw error;
      return null;
    });
    if (!info && create && index < parts.length - 1) {
      await mkdir(target, { mode: 0o700 });
      await syncDirectory(path.dirname(target));
      info = await lstat(target);
    }
    if (info && (info.isSymbolicLink() ||
      (index < parts.length - 1 && !info.isDirectory()) ||
      (index === parts.length - 1 && (!info.isFile() || info.nlink !== 1)))) {
      throw fail('Website paths must be ordinary local files and directories.');
    }
  }
  return target;
}

export async function readTracked(root, descriptor) {
  const file = await confined(root, trackedPath(descriptor));
  return readFile(file).catch(error => {
    if (error.code !== 'ENOENT') throw error;
    return null;
  });
}

export async function fingerprintTracked(root, descriptors) {
  const unique = [...new Map(descriptors.map(descriptor => [key(descriptor), descriptor])).values()];
  unique.sort((a, b) => key(a).localeCompare(key(b)));
  return Promise.all(unique.map(async ({ kind, id }) => {
    const bytes = await readTracked(root, { kind, id });
    return { kind, id, sha256: bytes === null ? null : hash(bytes) };
  }));
}

export async function syncDirectory(directory) {
  const handle = await open(directory, 'r');
  try { await handle.sync(); } finally { await handle.close(); }
}

export async function durableWrite(root, relative, bytes, { repairIncomplete = false, afterSync } = {}) {
  const target = await confined(root, relative, true);
  const readExisting = async () => readFile(await confined(root, relative)).catch(error => {
    if (error.code !== 'ENOENT') throw error;
    return null;
  });
  const before = await readExisting();
  if (before !== null) {
    if (!repairIncomplete) throw Object.assign(new Error('File already exists.'), { code: 'EEXIST' });
    if (before.equals(bytes)) {
      await syncDirectory(path.dirname(target));
      return target;
    }
    // Recover only an exact truncated prefix of the independently known bytes.
    // A different complete snapshot or non-prefix corruption is a conflict.
    if (before.length >= bytes.length || !bytes.subarray(0, before.length).equals(before)) {
      throw fail('Publication snapshot differs.');
    }
  }
  const temporary = await confined(root, `${relative}.${randomUUID()}.tmp`);
  const handle = await open(temporary, 'wx', 0o600);
  try {
    await handle.writeFile(bytes);
    await handle.sync();
  } finally {
    await handle.close();
  }
  await afterSync?.({ target, temporary });
  // Callers serialize operations; still fail if the observed final changed
  // while the temporary was prepared. Incomplete temporaries are never read.
  const current = await readExisting();
  if ((before === null) !== (current === null) || (before !== null && !before.equals(current))) {
    throw fail('Publication snapshot changed during replacement.');
  }
  await rename(temporary, target);
  await syncDirectory(path.dirname(target));
  return target;
}

export async function writeTemporary(root, operationRoot, write) {
  // Operation snapshot contains exact bytes; install temp is on the target filesystem.
  const bytes = await readFile(await confined(operationRoot, write.snapshot));
  if (hash(bytes) !== write.after) throw fail('Publication snapshot hash mismatch.');
  const relative = trackedPath(write);
  const target = await confined(root, relative, true);
  const temporary = await durableWrite(root, `${relative}.${randomUUID()}.tmp`, bytes);
  return { ...write, target, temporary };
}

export async function replaceTracked(root, stagedWrite) {
  const target = await confined(root, trackedPath(stagedWrite), true);
  if (target !== stagedWrite.target) throw fail('Publication target changed.');
  const before = await readTracked(root, stagedWrite);
  if ((before === null ? null : hash(before)) !== stagedWrite.before) {
    throw fail('Publication conflict: target changed during apply.');
  }
  await rename(stagedWrite.temporary, target);
  await syncDirectory(path.dirname(target));
}

export async function removeTracked(root, descriptor) {
  const target = await confined(root, trackedPath(descriptor));
  const before = await readTracked(root, descriptor);
  if ((before === null ? null : hash(before)) !== descriptor.before) {
    throw fail('Publication conflict: target changed during apply.');
  }
  await unlink(target);
  await syncDirectory(path.dirname(target));
}

export async function inspectTracked(root, expected) {
  const bytes = await readTracked(root, expected);
  const actual = bytes === null ? null : hash(bytes);
  return {
    kind: expected.kind, id: expected.id, actual,
    state: actual === expected.after ? 'after' : actual === expected.before ? 'before' : 'conflict'
  };
}
