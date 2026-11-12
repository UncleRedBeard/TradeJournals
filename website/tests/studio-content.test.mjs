import test from "node:test";
import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
import { prepareSite } from "../lib/prepare.mjs";

const repoRoot = fileURLToPath(new URL("../../", import.meta.url));
const contentRoot = fileURLToPath(new URL("../content/", import.meta.url));

test("restored Studio leads the homepage while remaining distinct from the earlier Studio", async () => {
  const { model } = await prepareSite({ repoRoot, contentRoot, mode: "preview" });
  const restoredStudio = model.projects.find(project => project.id === "living-room-studio-restoration");
  const earlierStudio = model.projects.find(project => project.id === "studio-office-restoration");
  const office = model.projects.find(project => project.id === "office-restoration");
  assert.ok(restoredStudio);
  assert.ok(earlierStudio);
  assert.ok(office);
  assert.equal(model.home.featuredProjectIds[0], "living-room-studio-restoration");
  assert.equal(model.site.navigation.find(item => item.label === "Work").href, "/work/entry-restoration/");
  assert.equal(model.home.hero.id, "flickr-55338112557");
  assert.equal(restoredStudio.gallery.length, 5);
  assert.ok(restoredStudio.gallery.every(photo => photo.id.startsWith("studio-")));
  assert.equal(restoredStudio.searchImages.length, 5);
  assert.deepEqual(restoredStudio.albums.map(album => album.key), ["google_photos:af1qippool3ge7t"]);
  assert.equal(restoredStudio.albums[0].sourceUrl, "https://photos.app.goo.gl/Tj2NRPeVUooFLAzD9");
  assert.equal(restoredStudio.albums[0].shown, 5);
  assert.match(restoredStudio.evidenceBoundary, /August\/September 2026/u);
  assert.match(restoredStudio.evidenceBoundary, /do not establish an exact move day/u);
  assert.equal(restoredStudio.occupancy.state, "current");
  assert.equal(earlierStudio.occupancy.state, "former");
  assert.equal(earlierStudio.gallery.length, 7);
  assert.equal(earlierStudio.searchImages.length, 2);
  assert.deepEqual(earlierStudio.albums.map(album => album.key), ["flickr:72177720306207693"]);
  assert.ok(earlierStudio.gallery.every(photo => photo.id.startsWith("flickr-527")));
  assert.deepEqual(earlierStudio.gallery.slice(-2).map(photo => photo.id), [
    "flickr-52704581571", "flickr-52704058327"
  ]);
  assert.ok(!earlierStudio.gallery.some(photo => photo.id === "flickr-52704581761"));
  assert.match(earlierStudio.evidenceBoundary, /do not establish that the finished door was reinstalled/u);
  assert.equal(office.gallery.length, 6);
  assert.deepEqual(office.albums.map(album => album.key), ["flickr:72177720316928566"]);
  assert.ok(office.gallery.slice(0, 5).every(photo => photo.id.startsWith("flickr-539")));
  assert.equal(office.gallery.at(-1).id, "flickr-53718846780");
});
