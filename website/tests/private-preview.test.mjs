import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { cp, lstat, mkdir, mkdtemp, readdir, readFile, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { setTimeout as delay } from "node:timers/promises";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { buildWebsite } from "../scripts/build.mjs";

const websiteRoot = fileURLToPath(new URL("..", import.meta.url));
const repoRoot = fileURLToPath(new URL("../..", import.meta.url));
const protectedPaths = [
  path.join(websiteRoot, "src/generated/site.json"),
  path.join(websiteRoot, ".generated"),
  path.join(websiteRoot, ".preview-dist")
];
const buildLock = path.join(os.tmpdir(), `wk-website-build-${process.ppid}.lock`);

async function acquireBuildLock(t) {
  const deadline = Date.now() + 30000;
  while (true) {
    try {
      await mkdir(buildLock);
      t.after(() => rm(buildLock, { recursive: true, force: true }));
      return;
    } catch (error) {
      if (error.code !== "EEXIST" || Date.now() >= deadline) throw error;
      await delay(25);
    }
  }
}

async function snapshot(target) {
  try {
    const info = await lstat(target);
    if (info.isDirectory()) {
      const entries = await readdir(target);
      return {
        type: "directory",
        entries: await Promise.all(entries.sort().map(async name => [name, await snapshot(path.join(target, name))]))
      };
    }
    const digest = createHash("sha256").update(await readFile(target)).digest("hex");
    return { type: "file", digest };
  } catch (error) {
    if (error.code === "ENOENT") return { type: "missing" };
    throw error;
  }
}

async function snapshots(targets) {
  return Promise.all(targets.map(snapshot));
}

async function privateFixture(t) {
  const privateRoot = await mkdtemp(path.join(os.tmpdir(), "wk-private-preview-"));
  t.after(() => rm(privateRoot, { recursive: true, force: true }));
  const privateContent = path.join(privateRoot, "content");
  await cp(path.join(websiteRoot, "content"), privateContent, { recursive: true });
  return { privateRoot, privateContent };
}

test("private preview isolates all generated inputs and outputs", async t => {
  await acquireBuildLock(t);
  const { privateRoot, privateContent } = await privateFixture(t);
  const before = await snapshots(protectedPaths);

  const result = await buildWebsite({
    mode: "preview",
    repoRoot,
    websiteRoot,
    contentRoot: privateContent,
    contentBoundaryRoot: privateRoot,
    generatedRoot: path.join(privateRoot, "generated"),
    modelPath: path.join(privateRoot, "site.json"),
    publicRoot: path.join(privateRoot, "public"),
    outputRoot: path.join(privateRoot, "output"),
    assetOverrides: new Map()
  });

  assert.equal(result.outputRoot, path.join(privateRoot, "output"));
  assert.deepEqual(await snapshots(protectedPaths), before);
});

test("private preview rejects asset overrides outside its content boundary before Astro starts", async t => {
  const { privateRoot, privateContent } = await privateFixture(t);
  const outputRoot = path.join(privateRoot, "output");

  await assert.rejects(buildWebsite({
    mode: "preview",
    repoRoot,
    websiteRoot,
    contentRoot: privateContent,
    contentBoundaryRoot: privateRoot,
    generatedRoot: path.join(privateRoot, "generated"),
    modelPath: path.join(privateRoot, "site.json"),
    publicRoot: path.join(privateRoot, "public"),
    outputRoot,
    assetOverrides: new Map([["flickr-53921322250", path.join(repoRoot, "site_example/assets/flickr/office/01.jpg")]])
  }), { code: "INVALID_PATH" });

  assert.deepEqual(await snapshot(outputRoot), { type: "missing" });
});

test('private new-media override fingerprints staged bytes without requiring a future canonical asset', async t => {
  const { writeFixture } = await import('./fixtures.mjs');
  const { prepareSite } = await import('../lib/prepare.mjs');
  const f=await writeFixture(t),bytes=Buffer.from('new prepared image');
  const sha256=createHash('sha256').update(bytes).digest('hex');
  const id=`studio-${sha256}`;
  await f.saveRecord(`media/${id}.json`,{...f.raw.media[0],id,assetPath:`website/assets/workbench/${id}.jpg`});
  await f.saveRecord('projects/project-one.json',{...f.raw.projects[0],gallery:[{mediaId:id,caption:'New image',role:'detail'}],searchMediaIds:[id]});
  await f.save('private/new.jpg',bytes);
  const result=await prepareSite({repoRoot:f.repoRoot,contentRoot:f.contentRoot,contentBoundaryRoot:f.repoRoot,mode:'preview',assetOverrides:new Map([[id,path.join(f.repoRoot,'private/new.jpg')]])});
  assert.equal(result.report.snapshot.sources.find(s=>s.key===`media:${id}`).sha256,sha256);
  assert.equal(result.assetCopies[0].sourceAbsolute,path.join(f.repoRoot,'private/new.jpg'));
  assert.ok(result.report.snapshot.sources.some(s=>s.key==='journal:journals/project-one.md'));
  assert.deepEqual(await snapshot(path.join(f.repoRoot,`website/assets/workbench/${id}.jpg`)),{type:'missing'});
});
