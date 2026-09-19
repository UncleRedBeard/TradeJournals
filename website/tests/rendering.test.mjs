import assert from "node:assert/strict";
import { cp, readFile, symlink } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { buildWebsite } from "../scripts/build.mjs";
import { writeFixture } from "./fixtures.mjs";

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

test("candidate preview renders explicit occupancy", async t => {
  const fixture = await writeFixture(t);
  const fixtureWebsiteRoot = path.join(fixture.repoRoot, "website");
  fixture.raw.projects[0].occupancy = { state: "current", label: "Current barre studio" };
  await fixture.saveRecord("projects/project-one.json", fixture.raw.projects[0]);
  await cp(path.join(websiteRoot, "astro.config.mjs"), path.join(fixtureWebsiteRoot, "astro.config.mjs"));
  await cp(path.join(websiteRoot, "lib"), path.join(fixtureWebsiteRoot, "lib"), { recursive: true });
  await cp(path.join(websiteRoot, "src"), path.join(fixtureWebsiteRoot, "src"), { recursive: true });
  await symlink(path.join(websiteRoot, "node_modules"), path.join(fixtureWebsiteRoot, "node_modules"));
  await cp(path.join(repoRoot, "site_example"), path.join(fixture.repoRoot, "site_example"), { recursive: true });

  await buildWebsite({ mode: "preview", repoRoot: fixture.repoRoot, websiteRoot: fixtureWebsiteRoot });
  const page = await readFile(path.join(fixtureWebsiteRoot, ".preview-dist/work/project-one/index.html"), "utf8");

  assert.match(page, /<strong[^>]*>Stage:<\/strong> Recorded work/);
  assert.match(page, /<strong[^>]*>Recorded:<\/strong> 2026/);
  assert.equal([...page.matchAll(/Current barre studio/g)].length, 1);
});
