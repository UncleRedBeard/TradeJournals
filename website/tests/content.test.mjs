import test from "node:test";
import assert from "node:assert/strict";
import { rename, symlink } from "node:fs/promises";
import path from "node:path";
import { loadContent, validateContent } from "../lib/content.mjs";
import { makeFixture, writeFixture } from "./fixtures.mjs";

test("a missing featured project identifies the exact selection", () => {
  const raw = makeFixture();
  raw.home.featuredProjectIds = ["missing-project"];
  assert.throws(() => validateContent(raw), error =>
    error.code === "MISSING_REFERENCE" && error.recordId === "home" &&
    error.field === "home.featuredProjectIds[0]"
  );
});

test("project occupancy is explicit and album ownership is exclusive", () => {
  const raw = makeFixture();
  raw.projects[0].occupancy = { state: "current", label: "Current barre studio" };
  assert.equal(validateContent(raw).projects[0].occupancy.state, "current");
  raw.projects[1].albumKeys = [...raw.projects[0].albumKeys];
  raw.projects[1].sourceRefs = structuredClone(raw.projects[0].sourceRefs);
  assert.throws(() => validateContent(raw), { code: "DUPLICATE_REFERENCE" });
});

for (const [name, change, code] of [
  ["duplicate project IDs", raw => raw.projects.push(raw.projects[0]), "DUPLICATE_ID"],
  ["unsupported schema", raw => raw.projects[0].schemaVersion = 2, "INVALID_CONTENT"],
  ["unknown project field", raw => raw.projects[0].privateNotes = "private", "INVALID_CONTENT"],
  ["empty title", raw => raw.projects[0].title = " ", "INVALID_CONTENT"],
  ["invalid occupancy state", raw => raw.projects[0].occupancy = { state: "moved", label: "Moved" }, "INVALID_CONTENT"],
  ["blank occupancy label", raw => raw.projects[0].occupancy = { state: "current", label: " " }, "INVALID_CONTENT"],
  ["invalid dimensions", raw => raw.media[0].width = 0, "INVALID_CONTENT"],
  ["illustration in gallery", raw => raw.media[0].kind = "illustration", "INVALID_EVIDENCE"],
  ["out-of-range focal point", raw => raw.projects[0].gallery[0].focalPoint = [101, 0], "INVALID_CONTENT"],
  ["missing gallery image", raw => raw.projects[0].gallery[0].mediaId = "missing", "MISSING_REFERENCE"],
  ["missing search image", raw => raw.projects[0].searchMediaIds = ["missing"], "MISSING_REFERENCE"],
  ["missing service", raw => raw.home.serviceIds = ["missing"], "MISSING_REFERENCE"],
  ["missing service project", raw => raw.services[0].projectIds = ["missing"], "MISSING_REFERENCE"],
  ["missing album reference", raw => raw.projects[0].albumKeys = ["flickr:222"], "MISSING_REFERENCE"],
  ["duplicate gallery selection", raw => raw.projects[0].gallery.push(raw.projects[0].gallery[0]), "DUPLICATE_REFERENCE"],
  ["traversal asset", raw => raw.media[0].assetPath = "images/../private.jpg", "INVALID_CONTENT"],
  ["executable asset", raw => raw.media[0].assetPath = "images/photo.svg", "INVALID_CONTENT"],
  ["inventory without anchor", raw => delete raw.projects[0].sourceRefs[1].anchor, "INVALID_CONTENT"]
]) {
  test(`content rejects ${name}`, () => {
    const raw = makeFixture();
    change(raw);
    assert.throws(() => validateContent(raw), error => error.code === code);
  });
}

for (const href of ["javascript:run()", "data:text/html,hello", "file:///private/a", "//example.org/", "/\\example.org/", "/%2fexample.org/", "/work/../private/", "/%0a/private/"]) {
  test(`navigation rejects unsafe destination ${href}`, () => {
    const raw = makeFixture();
    raw.site.navigation[0].href = href;
    assert.throws(() => validateContent(raw), { code: "INVALID_CONTENT" });
  });
}

test("an external source must be HTTPS without credentials", () => {
  const raw = makeFixture();
  for (const url of ["http://example.org/", "https:example.org/path", "https:/example.org/path", "https://user:secret@example.org/", "https://example.org/\n"]) {
    raw.media[0].sourceUrl = url;
    assert.throws(() => validateContent(raw), { code: "INVALID_CONTENT" });
  }
});

test("loadContent preserves record values and validates filenames", async t => {
  const fixture = await writeFixture(t);
  const records = await loadContent(fixture.contentRoot);
  assert.deepEqual(records, fixture.raw);
  assert.deepEqual(validateContent(records), records);
  await rename(path.join(fixture.contentRoot, "projects/project-one.json"), path.join(fixture.contentRoot, "projects/wrong-name.json"));
  await assert.rejects(loadContent(fixture.contentRoot), { code: "ID_FILENAME_MISMATCH" });
});

test("loadContent rejects malformed JSON and escaped record symlinks", async t => {
  const fixture = await writeFixture(t);
  await fixture.save("website/content/projects/broken.json", "{");
  await assert.rejects(loadContent(fixture.contentRoot), { code: "INVALID_JSON" });
  await fixture.saveRecord("projects/broken.json", { ...fixture.raw.projects[0], id: "broken" });
  await fixture.save("outside.json", JSON.stringify({ ...fixture.raw.projects[0], id: "escaped" }));
  await symlink(path.join(fixture.repoRoot, "outside.json"), path.join(fixture.contentRoot, "projects/escaped.json"));
  await assert.rejects(loadContent(fixture.contentRoot), { code: "INVALID_PATH" });
});
