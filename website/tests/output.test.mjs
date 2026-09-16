import assert from "node:assert/strict";
import { mkdir, mkdtemp, rm, symlink, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { checkOutput } from "../scripts/check-output.mjs";

async function fixture(t) {
  const outputRoot = await mkdtemp(path.join(os.tmpdir(), "tj-output-"));
  t.after(() => rm(outputRoot, { recursive: true, force: true }));
  const image = { src: "/media/photo.jpg", sourceUrl: "https://example.org/photo/" };
  const model = {
    home: {}, reviewNotice: "Local review preview", searchEntries: [],
    projects: [{ href: "/work/office/", archiveHref: "/tradejournals/office/",
      gallery: [image], searchImages: [image], albums: [] }]
  };
  const save = async (file, value) => {
    await mkdir(path.dirname(path.join(outputRoot, file)), { recursive: true });
    await writeFile(path.join(outputRoot, file), value);
  };
  const page = '<meta name="robots" content="noindex"><p>Local review preview</p><main id="main"><a href="#main">Skip</a><img src="/media/photo.jpg"><a href="https://example.org/photo/">Source</a></main>';
  for (const file of ["index.html", "tradejournals/index.html", "work/office/index.html", "tradejournals/office/index.html"]) await save(file, page);
  await save("search.json", "[]");
  await save("media/photo.jpg", "synthetic selected image");
  for (const file of ["journal-search.js", "archive-search.js"]) await save(`scripts/${file}`, "// fixture");
  return { outputRoot, model, save, page };
}

test("valid static output checks real destinations, fragments, images and preview metadata", async t => {
  const f = await fixture(t);
  await f.save("index.html", f.page + '<a href="/work/office/?view=all#main">Work</a><img srcset="/media/photo.jpg 1x, /media/photo.jpg 2x">');
  assert.equal((await checkOutput(f)).pages, 4);
});

for (const [name, mutate, code] of [
  ["missing page", f => rm(path.join(f.outputRoot, "work/office/index.html")), "MISSING_OUTPUT"],
  ["missing image", f => rm(path.join(f.outputRoot, "media/photo.jpg")), "MISSING_OUTPUT"],
  ["broken local destination", f => f.save("index.html", f.page + '<a href="/missing/">Missing</a>'), "BROKEN_REFERENCE"],
  ["same-page fragment", f => f.save("index.html", f.page + '<a href="#absent">Missing</a>'), "BROKEN_FRAGMENT"],
  ["duplicate fragment target", f => f.save("index.html", f.page + '<p id="main">Duplicate</p>'), "BROKEN_FRAGMENT"],
  ["private script path", f => f.save("scripts/archive-search.js", 'const path = "/Users/example/private.md";'), "PRIVATE_OUTPUT"],
  ["missing photo source link", f => f.save("work/office/index.html", f.page.replace('<a href="https://example.org/photo/">Source</a>', "")), "MISSING_SOURCE_LINK"],
  ["missing fragment", f => f.save("index.html", f.page + '<a href="/work/office/#absent">Missing</a>'), "BROKEN_FRAGMENT"],
  ["raw journal", f => f.save("private/journal.md", "Internal record"), "UNEXPECTED_OUTPUT"],
  ["master PDF", f => f.save("master.pdf", "private"), "UNEXPECTED_OUTPUT"],
  ["source map", f => f.save("_astro/app.js.map", "{}"), "UNEXPECTED_OUTPUT"],
  ["unselected media", f => f.save("media/unselected.jpg", "private"), "UNEXPECTED_OUTPUT"],
  ["private absolute path", f => f.save("index.html", f.page + '<p>/Users/example/private.md</p>'), "PRIVATE_OUTPUT"],
  ["unsafe link", f => f.save("index.html", f.page + '<a href="javascript:alert(1)">Bad</a>'), "UNSAFE_REFERENCE"],
  ["empty image URL", f => f.save("index.html", f.page.replace('src="/media/photo.jpg"', 'src=""')), "UNSAFE_REFERENCE"],
  ["empty srcset", f => f.save("index.html", f.page + '<img srcset="">'), "UNSAFE_REFERENCE"],
  ["external image", f => f.save("index.html", f.page + '<img src="https://example.org/unselected.jpg">'), "UNSAFE_REFERENCE"],
  ["malformed srcset", f => f.save("index.html", f.page + '<img srcset="/media/photo.jpg nope">'), "UNSAFE_REFERENCE"],
  ["changed search data", f => f.save("search.json", '[{"private":"record"}]'), "SEARCH_MISMATCH"],
  ["missing noindex", f => f.save("index.html", f.page.replace('content="noindex"', 'content="index"')), "PREVIEW_METADATA"],
  ["missing preview label", f => f.save("index.html", f.page.replace("Local review preview", "")), "PREVIEW_METADATA"],
  ["symlink asset", async f => { await rm(path.join(f.outputRoot, "media/photo.jpg")); await symlink("/etc/hosts", path.join(f.outputRoot, "media/photo.jpg")); }, "UNEXPECTED_OUTPUT"]
]) {
  test(`output rejects ${name}`, async t => {
    const f = await fixture(t);
    await mutate(f);
    await assert.rejects(checkOutput(f), error => error.code === code && Boolean(error.file));
  });
}

test("reviewed release rejects preview metadata and accepts clean rendered pages", async t => {
  const f = await fixture(t);
  f.model.reviewNotice = "";
  await assert.rejects(checkOutput(f), { code: "PREVIEW_METADATA" });
  const clean = f.page.replace('<meta name="robots" content="noindex">', '').replace('<p>Local review preview</p>', '');
  for (const file of ["index.html", "tradejournals/index.html", "work/office/index.html", "tradejournals/office/index.html"]) await f.save(file, clean);
  assert.equal((await checkOutput(f)).pages, 4);
});


test("relative references resolve from the containing page", async t => {
  const f = await fixture(t);
  await f.save("work/office/index.html", f.page + '<a href="../office/#main">Story</a><img src="../../media/photo.jpg">');
  assert.equal((await checkOutput(f)).pages, 4);
});

test("selected home hero is part of the expected public assets", async t => {
  const f = await fixture(t);
  f.model.home.hero = { src: "/media/hero.jpg" };
  await f.save("media/hero.jpg", "synthetic hero");
  await f.save("index.html", f.page + '<img src="/media/hero.jpg">');
  assert.equal((await checkOutput(f)).pages, 4);
});

test("release output rejects a leftover preview notice without noindex", async t => {
  const f = await fixture(t);
  f.model.reviewNotice = "";
  const page = f.page.replace('<meta name="robots" content="noindex">', '').replace('<p>Local review preview</p>', '<aside class="review-notice">Local review preview</aside>');
  for (const file of ["index.html", "tradejournals/index.html", "work/office/index.html", "tradejournals/office/index.html"]) await f.save(file, page);
  await assert.rejects(checkOutput(f), { code: "PREVIEW_METADATA" });
});

test("safe HTTPS story citations coexist with exact evidence source links", async t => {
  const f = await fixture(t);
  await f.save("tradejournals/office/index.html", f.page + '<a href="https://www.nps.gov/subjects/historicpreservation/index.htm">Preservation reference</a>');
  assert.equal((await checkOutput(f)).pages, 4);
});
