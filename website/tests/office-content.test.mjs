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
  ["office/05.jpg", "53919981267", "72177720316928566"],
  ["studio-office/01.jpg", "52705240435", "72177720306207693"],
  ["studio-office/02.jpg", "52705240380", "72177720306207693"],
  ["studio-office/03.jpg", "52705240355", "72177720306207693"],
  ["studio-office/04.jpg", "52704298727", "72177720306207693"],
  ["studio-office/05.jpg", "52705240320", "72177720306207693"]
];

test("Office preserves the selected gallery, original Flickr URLs, and distinct search copy", async () => {
  const records = validateContent(await loadContent(contentRoot));
  const office = records.projects.find(project => project.id === "office-restoration");
  assert.ok(office);
  assert.equal(office.gallery.length, 10);
  assert.deepEqual(office.searchMediaIds, [
    "flickr-53921322250", "flickr-52705240435", "flickr-52705240380"
  ]);
  assert.notEqual(office.summary, office.searchSummary);
  assert.match(office.introduction, /author's 1894 home/);

  const mediaById = new Map(records.media.map(media => [media.id, media]));
  for (const [relativeAsset, photoId, albumId] of officePhotos) {
    const media = mediaById.get(`flickr-${photoId}`);
    assert.equal(media.assetPath, `site_example/assets/flickr/${relativeAsset}`);
    assert.equal(media.albumKey, `flickr:${albumId}`);
    assert.equal(media.sourceUrl, `https://www.flickr.com/photos/boocher/${photoId}/in/set-${albumId}/`);
  }
});

test("Office is an explicit candidate, with the approved public identity and no contact action", async () => {
  const records = validateContent(await loadContent(contentRoot));
  assert.equal(records.review.state, "candidate");
  assert.equal(records.site.name, "Toil & Timber Restoration");
  assert.equal(records.site.descriptor, "Historic floors, interior woodwork, and architectural restoration.");
  assert.equal(records.site.serviceLine, "Historic floors, interior woodwork, and architectural restoration.");
  assert.equal(records.site.contact, undefined);
  assert.ok(records.projects.some(project => project.id === "office-restoration"));
  assert.deepEqual(records.home.serviceIds, ["historic-floors"]);
});

test("Office candidate prepares a local preview but cannot prepare a release", async () => {
  const repoRoot = fileURLToPath(new URL("../../", import.meta.url));
  const preview = await prepareSite({ repoRoot, contentRoot, mode: "preview" });
  assert.equal(preview.report.state, "candidate");
  assert.equal(preview.model.projects.find(project => project.id === "office-restoration").gallery.length, 10);
  assert.match(preview.model.reviewNotice, /await review/u);
  await assert.rejects(
    prepareSite({ repoRoot, contentRoot, mode: "release" }),
    { code: "UNREVIEWED_CONTENT" }
  );
});
