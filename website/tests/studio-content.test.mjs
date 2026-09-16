import test from "node:test";
import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
import { prepareSite } from "../lib/prepare.mjs";

const repoRoot = fileURLToPath(new URL("../../", import.meta.url));
const contentRoot = fileURLToPath(new URL("../content/", import.meta.url));

test("Studio leads the preview with its own provenance and no borrowed Office photos", async () => {
  const { model } = await prepareSite({ repoRoot, contentRoot, mode: "preview" });
  const studio = model.projects.find(project => project.id === "studio-restoration");
  const office = model.projects.find(project => project.id === "office-restoration");
  assert.ok(studio);
  assert.ok(office);
  assert.equal(model.home.featuredProjectIds[0], studio.id);
  assert.equal(model.site.navigation.find(item => item.label === "Work").href, studio.href);
  assert.equal(model.home.hero, undefined);
  assert.deepEqual(studio.gallery, []);
  assert.deepEqual(studio.searchImages, []);
  assert.deepEqual(studio.albums.map(album => album.key), ["google_photos:af1qippool3ge7t"]);
  assert.equal(studio.albums[0].sourceUrl, "https://photos.app.goo.gl/Tj2NRPeVUooFLAzD9");
  assert.equal(studio.albums[0].shown, 0);
  assert.match(studio.evidenceBoundary, /August 30, 2026/);
  assert.match(studio.evidenceBoundary, /not yet been selected/);
  assert.equal(office.gallery.length, 10);
});
