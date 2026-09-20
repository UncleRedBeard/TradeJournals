import test from "node:test";
import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
import { loadContent, validateContent } from "../lib/content.mjs";
import { prepareSite } from "../lib/prepare.mjs";

const contentRoot = fileURLToPath(new URL("../content/", import.meta.url));
const officePhotos = [
  ["office/01.jpg", "53921322250", "72177720316928566"],
  ["office/02.jpg", "53921322245", "72177720316928566"],
  ["office/03.jpg", "53921322215", "72177720316928566"],
  ["office/04.jpg", "53921225999", "72177720316928566"],
  ["office/05.jpg", "53919981267", "72177720316928566"]
];

test("Office preserves the selected gallery, original Flickr URLs, and distinct search copy", async () => {
  const records = validateContent(await loadContent(contentRoot));
  const office = records.projects.find(project => project.id === "office-restoration");
  assert.ok(office);
  assert.equal(office.gallery.length, 5);
  assert.deepEqual(office.searchMediaIds, ["flickr-53921322250"]);
  assert.notEqual(office.summary, office.searchSummary);
  assert.match(office.introduction, /dedicated office/u);
  assert.deepEqual(office.albumKeys, ["flickr:72177720316928566"]);

  const mediaById = new Map(records.media.map(media => [media.id, media]));
  for (const [relativeAsset, photoId, albumId] of officePhotos) {
    const media = mediaById.get(`flickr-${photoId}`);
    assert.equal(media.assetPath, `site_example/assets/flickr/${relativeAsset}`);
    assert.equal(media.albumKey, `flickr:${albumId}`);
    assert.equal(media.sourceUrl, `https://www.flickr.com/photos/boocher/${photoId}/in/set-${albumId}/`);
  }
});

test("approved site snapshot retains the disabled email placeholder", async () => {
  const records = validateContent(await loadContent(contentRoot));
  assert.equal(records.review.state, "reviewed");
  assert.equal(records.site.name, "Toil & Timber Restoration");
  assert.equal(records.site.descriptor, "Historic floors, interior woodwork, and architectural restoration.");
  assert.equal(records.site.serviceLine, "Historic floors, interior woodwork, and architectural restoration.");
  assert.deepEqual(records.site.contact, {
    label: "Email us — coming soon",
    href: null
  });
  assert.ok(records.projects.some(project => project.id === "office-restoration"));
  assert.deepEqual(records.home.serviceIds, ["historic-floors"]);
});

test("expanded approved snapshot is current for preview and release", async () => {
  const repoRoot = fileURLToPath(new URL("../../", import.meta.url));
  const preview = await prepareSite({ repoRoot, contentRoot, mode: "preview" });
  assert.equal(preview.report.state, "current");
  assert.deepEqual(preview.report.changedKeys, []);
  assert.equal(preview.model.projects.find(project => project.id === "office-restoration").gallery.length, 5);
  assert.match(preview.model.reviewNotice, /reviewed content/u);

  const release = await prepareSite({ repoRoot, contentRoot, mode: "release" });
  assert.equal(release.report.state, "current");
  assert.deepEqual(release.report.changedKeys, []);
  assert.equal(release.model.reviewNotice, "");
});
