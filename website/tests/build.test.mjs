import assert from "node:assert/strict";
import { access, mkdir, readFile, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { setTimeout as delay } from "node:timers/promises";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { buildWebsite } from "../scripts/build.mjs";

const websiteRoot = fileURLToPath(new URL("..", import.meta.url));
const repoRoot = fileURLToPath(new URL("../..", import.meta.url));
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

test("candidate preview stages selected assets and writes the public model", async t => {
  await acquireBuildLock(t);
  const result = await buildWebsite({ mode: "preview", repoRoot, websiteRoot });
  const model = JSON.parse(await readFile(path.join(websiteRoot, "src/generated/site.json"), "utf8"));

  assert.equal(result.outputRoot, path.join(websiteRoot, ".preview-dist"));
  assert.deepEqual(result.model.projects.map(project => project.id).sort(), [
    "living-room-studio-restoration", "office-restoration", "studio-office-restoration"
  ]);
  assert.equal(model.projects.find(project => project.id === "office-restoration").gallery.length, 5);
  assert.equal(model.projects.find(project => project.id === "studio-office-restoration").gallery.length, 5);
  assert.equal(model.projects.find(project => project.id === "living-room-studio-restoration").gallery.length, 3);
  await access(path.join(websiteRoot, ".generated/public/media/flickr-53921322250.jpg"));
  await access(path.join(websiteRoot, ".preview-dist/index.html"));
  await access(path.join(websiteRoot, ".preview-dist/work/studio-office-restoration/index.html"));
  await access(path.join(websiteRoot, ".preview-dist/work/living-room-studio-restoration/index.html"));
  await access(path.join(websiteRoot, ".preview-dist/tradejournals/studio-office-restoration/index.html"));
  await access(path.join(websiteRoot, ".preview-dist/tradejournals/living-room-studio-restoration/index.html"));
});
