import test from "node:test";
import assert from "node:assert/strict";
import { readFile, symlink } from "node:fs/promises";
import path from "node:path";
import { prepareSite, parseInspectionResult } from "../lib/prepare.mjs";
import { writeFixture } from "./fixtures.mjs";

const prepare = (fixture, mode = "preview") => prepareSite({
  repoRoot: fixture.repoRoot, contentRoot: fixture.contentRoot, mode
});
async function acceptFixture(fixture) {
  const { report } = await prepare(fixture);
  await fixture.saveRecord("reviews/pilot.json", {
    ...fixture.raw.review, state: "reviewed", ...report.snapshot
  });
}

test("offline preview resolves selected public records, counts and source links", async t => {
  const fixture = await writeFixture(t);
  fixture.raw.projects[0].searchSummary = "A distinct search summary";
  fixture.raw.projects[0].gallery[0].alt = "A contextual gallery description";
  await fixture.saveRecord("projects/project-one.json", fixture.raw.projects[0]);
  const reviewBefore = await readFile(path.join(fixture.contentRoot, "reviews/pilot.json"));
  const result = await prepare(fixture);
  assert.equal(result.report.state, "candidate");
  assert.match(result.model.reviewNotice, /review/i);
  assert.equal(result.model.projects.length, 2);
  assert.deepEqual(result.model.projects[0].albums, [{
    key: "flickr:111", label: "First album", count: 12,
    sourceUrl: "https://example.org/albums/111/", shown: 1
  }]);
  const project = result.model.projects[0];
  assert.equal(project.gallery[0].sourceUrl, fixture.raw.media[0].sourceUrl);
  assert.equal(project.gallery[0].alt, "A contextual gallery description");
  assert.equal(project.searchImages[0].alt, fixture.raw.media[0].alt);
  assert.equal(result.model.searchEntries[0].summary, "A distinct search summary");
  assert.equal(result.model.searchEntries[1].summary, fixture.raw.projects[1].summary);
  assert.equal(result.model.searchEntries[0].source, "/tradejournals/project-one/");
  assert.equal(result.model.searchEntries[0].url, "/work/project-one/");
  assert.deepEqual(result.assetCopies, [{
    sourceAbsolute: path.join(fixture.repoRoot, "images/photo-one.jpg"), publicRelative: "media/photo-one.jpg"
  }]);
  const output = JSON.stringify(result.model);
  for (const forbidden of [fixture.repoRoot, "journals/project-one.md", "assetPath", "sourceRefs", "unselected-photo", "sha256"]) {
    assert.ok(!output.includes(forbidden), `public output must omit ${forbidden}`);
  }
  assert.deepEqual(await readFile(path.join(fixture.contentRoot, "reviews/pilot.json")), reviewBefore);
  assert.ok(!result.report.snapshot.records.some(record => record.key.startsWith("review:")));
});

test("offline preview preserves project occupancy in public and search evidence", async t => {
  const fixture = await writeFixture(t);
  fixture.raw.projects[0].occupancy = { state: "current", label: "Current barre studio" };
  await fixture.saveRecord("projects/project-one.json", fixture.raw.projects[0]);

  const result = await prepare(fixture);

  assert.deepEqual(result.model.projects[0].occupancy, { state: "current", label: "Current barre studio" });
  assert.deepEqual(result.model.searchEntries[0].evidence.occupancy, { state: "current", label: "Current barre studio" });
});

test("only synthetic reviewed snapshots pass release; candidate content is never promoted", async t => {
  const fixture = await writeFixture(t);
  await assert.rejects(prepare(fixture, "release"), { code: "UNREVIEWED_CONTENT" });
  await acceptFixture(fixture);
  const preview = await prepare(fixture);
  assert.match(preview.model.reviewNotice, /preview/i);
  const result = await prepare(fixture, "release");
  assert.equal(result.report.state, "current");
  assert.equal(result.model.reviewNotice, "");
  const reviewed = JSON.parse(await readFile(path.join(fixture.contentRoot, "reviews/pilot.json"), "utf8"));
  assert.equal(reviewed.state, "reviewed");
});

test("selected source and copy changes expire review; unrelated inventory and media do not", async t => {
  const fixture = await writeFixture(t);
  await acceptFixture(fixture);
  const inventory = await readFile(path.join(fixture.repoRoot, "albums.md"), "utf8");
  await fixture.save("albums.md", inventory.replace("Photos: 99", "Photos: 100"));
  await fixture.save("images/unselected-photo.jpg", "new unselected bytes");
  await fixture.save("journals/unselected-project.md", "unselected journal");
  assert.equal((await prepare(fixture, "release")).report.state, "current");
  await fixture.save("journals/project-one.md", "Changed selected source");
  const changed = await prepare(fixture);
  assert.equal(changed.report.state, "stale");
  assert.deepEqual(changed.report.changedKeys, ["journal:journals/project-one.md"]);
  await assert.rejects(prepare(fixture, "release"), { code: "SOURCE_STALE" });
  await acceptFixture(fixture);
  fixture.raw.projects[0].summary = "A revised interpretation";
  await fixture.saveRecord("projects/project-one.json", fixture.raw.projects[0]);
  assert.deepEqual((await prepare(fixture)).report.changedKeys, ["project:project-one"]);
  await assert.rejects(prepare(fixture, "release"), { code: "SOURCE_STALE" });
});

test("equivalent JSON and inventory newlines preserve review; selected photo bytes do not", async t => {
  const fixture = await writeFixture(t);
  await acceptFixture(fixture);
  await fixture.save("website/content/site.json", JSON.stringify(fixture.raw.site, null, 4));
  const inventory = await readFile(path.join(fixture.repoRoot, "albums.md"), "utf8");
  await fixture.save("albums.md", inventory.replaceAll("\n", "\r\n"));
  assert.equal((await prepare(fixture, "release")).report.state, "current");
  await fixture.save("images/photo-one.jpg", "changed selected pixels");
  assert.deepEqual((await prepare(fixture)).report.changedKeys, ["media:photo-one"]);
});

test("optional story is resolved and fingerprinted without copying source prose into model", async t => {
  const fixture = await writeFixture(t);
  fixture.raw.projects[0].storyId = "project-one";
  await fixture.saveRecord("projects/project-one.json", fixture.raw.projects[0]);
  await assert.rejects(prepare(fixture), { code: "MISSING_FILE" });
  await fixture.save("website/content/stories/project-one.md", "---\nschemaVersion: 1\nid: project-one\n---\nA curated narrative.");
  await acceptFixture(fixture);
  const result = await prepare(fixture, "release");
  assert.equal(result.model.projects[0].storyId, "project-one");
  assert.ok(!JSON.stringify(result.model).includes("A curated narrative"));
  await fixture.save("website/content/stories/project-one.md", "A changed story.");
  assert.deepEqual((await prepare(fixture)).report.changedKeys, ["story:project-one"]);
});

test("hero images are explicit selections with dimensions and their own fingerprint", async t => {
  const fixture = await writeFixture(t);
  fixture.raw.home.heroMediaId = "photo-two";
  await fixture.saveRecord("home.json", fixture.raw.home);
  const result = await prepare(fixture);
  assert.equal(result.model.home.hero.id, "photo-two");
  assert.equal(result.model.home.hero.width, 800);
  assert.equal(result.assetCopies.length, 2);
  assert.ok(result.report.snapshot.sources.some(record => record.key === "media:photo-two"));
});

test("invalid source and image paths fail even in preview mode", async t => {
  const fixture = await writeFixture(t);
  fixture.raw.projects[0].sourceRefs[0].path = "journals/missing.md";
  await fixture.saveRecord("projects/project-one.json", fixture.raw.projects[0]);
  await assert.rejects(prepare(fixture), { code: "MISSING_SOURCE" });
  fixture.raw.projects[0].sourceRefs[0].path = "journals/project-one.md";
  await fixture.saveRecord("projects/project-one.json", fixture.raw.projects[0]);
  await symlink("/etc/hosts", path.join(fixture.repoRoot, "images/escaped.jpg"));
  fixture.raw.media[0].assetPath = "images/escaped.jpg";
  await fixture.saveRecord("media/photo-one.json", fixture.raw.media[0]);
  await assert.rejects(prepare(fixture), { code: "INVALID_PATH" });
});

test("unknown mode, unavailable routes and implausible shown counts fail precisely", async t => {
  const fixture = await writeFixture(t);
  await assert.rejects(prepare(fixture, "publish"), { code: "INVALID_MODE" });
  fixture.raw.site.navigation[0].href = "/about/";
  await fixture.saveRecord("site.json", fixture.raw.site);
  await assert.rejects(prepare(fixture), { code: "MISSING_DESTINATION" });
  fixture.raw.site.navigation[0].href = "/work/project-one/";
  await fixture.saveRecord("site.json", fixture.raw.site);
  const inventory = await readFile(path.join(fixture.repoRoot, "albums.md"), "utf8");
  await fixture.save("albums.md", inventory.replace("Photos: 12", "Photos: 0"));
  await assert.rejects(prepare(fixture), { code: "INVALID_EVIDENCE" });
});

test("malformed, partial, duplicate and unexpected inspector responses fail closed", () => {
  const requests = [{ key: "journal:a", kind: "journal", path: "a.md" }];
  const fact = { key: "journal:a", sha256: "a".repeat(64) };
  for (const output of ["not JSON", "{}", "[]", JSON.stringify([fact, fact]), JSON.stringify([{ ...fact, key: "unknown" }]), JSON.stringify([{ ...fact, sha256: "bad" }])]) {
    assert.throws(() => parseInspectionResult(output, requests), { code: "INVALID_SOURCE_RESPONSE" });
  }
  assert.deepEqual(parseInspectionResult(JSON.stringify([fact]), requests), [fact]);
});
