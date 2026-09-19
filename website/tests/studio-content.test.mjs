import test from "node:test";
import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
import { prepareSite } from "../lib/prepare.mjs";

const repoRoot = fileURLToPath(new URL("../../", import.meta.url));
const contentRoot = fileURLToPath(new URL("../content/", import.meta.url));

test("future Studio leads the preview while current Studio and Office keep separate provenance", async () => {
  const { model } = await prepareSite({ repoRoot, contentRoot, mode: "preview" });
  const futureStudio = model.projects.find(project => project.id === "living-room-studio-restoration");
  const currentStudio = model.projects.find(project => project.id === "studio-office-restoration");
  const office = model.projects.find(project => project.id === "office-restoration");
  assert.ok(futureStudio);
  assert.ok(currentStudio);
  assert.ok(office);
  assert.equal(model.home.featuredProjectIds[0], futureStudio.id);
  assert.equal(model.site.navigation.find(item => item.label === "Work").href, futureStudio.href);
  assert.equal(model.home.hero, undefined);
  assert.equal(futureStudio.gallery.length, 3);
  assert.ok(futureStudio.gallery.every(photo => photo.id.startsWith("studio-")));
  assert.equal(futureStudio.searchImages.length, 3);
  assert.deepEqual(futureStudio.albums.map(album => album.key), ["google_photos:af1qippool3ge7t"]);
  assert.equal(futureStudio.albums[0].sourceUrl, "https://photos.app.goo.gl/Tj2NRPeVUooFLAzD9");
  assert.equal(futureStudio.albums[0].shown, 3);
  assert.match(futureStudio.evidenceBoundary, /August 30, 2026/u);
  assert.match(futureStudio.evidenceBoundary, /do not establish that the studio move has occurred/u);
  assert.equal(currentStudio.gallery.length, 5);
  assert.equal(currentStudio.searchImages.length, 2);
  assert.deepEqual(currentStudio.albums.map(album => album.key), ["flickr:72177720306207693"]);
  assert.ok(currentStudio.gallery.every(photo => photo.id.startsWith("flickr-527")));
  assert.equal(office.gallery.length, 5);
  assert.deepEqual(office.albums.map(album => album.key), ["flickr:72177720316928566"]);
  assert.ok(office.gallery.every(photo => photo.id.startsWith("flickr-539")));
});
