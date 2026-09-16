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

  assert.equal(result.model.projects.length, 1);
  assert.equal(model.projects[0].gallery.length, 10);
  await access(path.join(websiteRoot, ".generated/public/media/flickr-53921322250.jpg"));
  await access(path.join(websiteRoot, ".preview-dist/index.html"));
});
