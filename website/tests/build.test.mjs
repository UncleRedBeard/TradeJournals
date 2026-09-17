import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { buildWebsite } from "../scripts/build.mjs";

const websiteRoot = fileURLToPath(new URL("..", import.meta.url));
const repoRoot = fileURLToPath(new URL("../..", import.meta.url));

test("candidate preview stages selected assets and writes the public model", async () => {
  const result = await buildWebsite({ mode: "preview", repoRoot, websiteRoot });
  const model = JSON.parse(await readFile(path.join(websiteRoot, "src/generated/site.json"), "utf8"));

  assert.deepEqual(result.model.projects.map(project => project.id).sort(), ["office-restoration", "studio-restoration"]);
  assert.equal(model.projects.find(project => project.id === "office-restoration").gallery.length, 10);
  assert.equal(model.projects.find(project => project.id === "studio-restoration").gallery.length, 3);
  await access(path.join(websiteRoot, ".generated/public/media/flickr-53921322250.jpg"));
  await access(path.join(websiteRoot, ".preview-dist/index.html"));
  await access(path.join(websiteRoot, ".preview-dist/work/studio-restoration/index.html"));
  await access(path.join(websiteRoot, ".preview-dist/tradejournals/studio-restoration/index.html"));
});
