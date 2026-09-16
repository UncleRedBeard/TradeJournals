import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { buildWebsite } from "../scripts/build.mjs";

const websiteRoot = fileURLToPath(new URL("..", import.meta.url));
const repoRoot = fileURLToPath(new URL("../..", import.meta.url));

test("candidate preview renders the Office record without a contact form", async () => {
  await buildWebsite({ mode: "preview", repoRoot, websiteRoot });
  const page = await readFile(path.join(websiteRoot, ".preview-dist/work/office-restoration/index.html"), "utf8");

  assert.match(page, /Toil &amp; Timber Restoration/);
  assert.match(page, /Historic floors, interior woodwork, and architectural restoration\./);
  assert.match(page, /Local review preview — content and photo selections await review\./);
  assert.match(page, /https:\/\/www\.flickr\.com\/photos\/boocher\/53921322250\/in\/set-72177720316928566\//);
  assert.match(page, /\/media\/flickr-53921322250\.jpg/);
  assert.doesNotMatch(page, /<form[^>]*action=/);
  assert.doesNotMatch(page, /01_the_residence_1894/);
});
