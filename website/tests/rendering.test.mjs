import assert from "node:assert/strict";
import { cp, readFile, symlink } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { buildWebsite } from "../scripts/build.mjs";
import { writeFixture } from "./fixtures.mjs";

const websiteRoot = fileURLToPath(new URL("..", import.meta.url));
const repoRoot = fileURLToPath(new URL("../..", import.meta.url));

test("preview renders the Office record and review notice without a contact form", async () => {
  const result = await buildWebsite({ mode: "preview", repoRoot, websiteRoot });
  const page = await readFile(path.join(websiteRoot, ".preview-dist/work/office-restoration/index.html"), "utf8");

  assert.match(page, /Toil &amp; Timber Restoration/);
  assert.match(page, /Historic floors, interior woodwork, and architectural restoration\./);
  assert.ok(result.model.reviewNotice);
  assert.ok(page.includes(result.model.reviewNotice));
  assert.match(page, /https:\/\/www\.flickr\.com\/photos\/boocher\/53921322250\/in\/set-72177720316928566\//);
  assert.match(page, /\/media\/flickr-53921322250\.jpg/);
  assert.doesNotMatch(page, /<form[^>]*action=/);
  assert.doesNotMatch(page, /01_the_residence_1894/);
});

test("homepage links every selected project in folio order and keeps inquiries disabled", async () => {
  await buildWebsite({ mode: "preview", repoRoot, websiteRoot });
  const page = await readFile(path.join(websiteRoot, ".preview-dist/index.html"), "utf8");

  assert.match(page, /href="#documented-projects"/);
  assert.match(page, /id="documented-projects"/);
  assert.match(page, /href="#practice"/);
  assert.match(page, /id="practice"/);
  assert.match(page, /href="#workshop-studies"/);
  assert.match(page, /id="workshop-studies"/);
  const cards = [...page.matchAll(/<article\b[^>]*>.*?<\/article>/gs)].map(match => match[0]);
  const projectIds = ["living-room-studio-restoration", "entry-restoration", "guest-bath-dresser-vanity", "master-bedroom-restoration", "returning-to-clay", "agfa-isolette"];
  assert.equal(cards.length, projectIds.length);
  for (const [index, id] of projectIds.entries()) {
    assert.ok(cards[index].includes(`href="/work/${id}/"`), `${id} has a working story link in the selected order`);
    assert.match(cards[index], /<img[^>]+alt="[^"]+"/);
  }
  const contactButtons = [...page.matchAll(/<button\b[^>]*>Email us — coming soon<\/button>/g)];
  assert.ok(contactButtons.length > 0);
  for (const [button] of contactButtons) assert.match(button, /\bdisabled\b/);
  assert.doesNotMatch(page, /mailto:/);
  assert.doesNotMatch(page, /<form\b/);
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
