import { mkdtemp, mkdir, writeFile, rm, realpath } from "node:fs/promises";
import path from "node:path";
import os from "node:os";

export function makeFixture() {
  const project = id => ({
    schemaVersion: 1, id, title: `Recorded ${id}`, area: "Residence",
    summary: "A documented room project.", searchSummary: "", tags: ["floor"],
    stage: "Recorded work", recorded: "2026", sourceLabel: "Local journal and album",
    sourceRefs: [
      { kind: "journal", path: `journals/${id}.md` },
      { kind: "inventory", path: "albums.md", anchor: "album-111" }
    ],
    albumKeys: ["flickr:111"],
    gallery: [{ mediaId: "photo-one", caption: "Recorded surface", role: "detail" }],
    searchMediaIds: ["photo-one"]
  });
  const media = id => ({
    schemaVersion: 1, id, kind: "evidence", assetPath: `images/${id}.jpg`,
    sourceUrl: `https://example.org/photos/${id}/`, albumKey: "flickr:111",
    alt: `Recorded ${id}`, width: 800, height: 600
  });
  return {
    site: {
      schemaVersion: 1, id: "site", name: "Worth Keeping",
      descriptor: "Time & Timber Restoration",
      serviceLine: "Historic floors, interior woodwork, and architectural restoration.",
      navigation: [{ label: "Work", href: "/work/project-one/" }]
    },
    home: {
      schemaVersion: 1, id: "home", headline: "Keep what makes it home.",
      intro: "Documented craft work.", featuredProjectIds: ["project-one"],
      serviceIds: ["historic-floors"]
    },
    services: [{
      schemaVersion: 1, id: "historic-floors", title: "Historic floors",
      description: "Care grounded in recorded work.", projectIds: ["project-one"]
    }],
    projects: [project("project-one"), project("project-two")],
    media: [media("photo-one"), media("photo-two"), media("unselected-photo")],
    review: { schemaVersion: 1, id: "pilot", state: "candidate", records: [], sources: [] }
  };
}

export async function writeFixture(t, raw = makeFixture()) {
  const repoRoot = await realpath(await mkdtemp(path.join(os.tmpdir(), "wk-content-")));
  t.after(() => rm(repoRoot, { recursive: true, force: true }));
  const contentRoot = path.join(repoRoot, "website/content");
  const save = async (relative, value) => {
    const target = path.join(repoRoot, relative);
    await mkdir(path.dirname(target), { recursive: true });
    await writeFile(target, value);
  };
  const saveRecord = (relative, record) => save(`website/content/${relative}`, JSON.stringify(record));
  await saveRecord("site.json", raw.site);
  await saveRecord("home.json", raw.home);
  await saveRecord("reviews/pilot.json", raw.review);
  for (const group of ["services", "projects", "media"]) {
    for (const record of raw[group]) await saveRecord(`${group}/${record.id}.json`, record);
  }
  for (const project of raw.projects) await save(`journals/${project.id}.md`, `# ${project.title}\n`);
  for (const media of raw.media) await save(media.assetPath, `synthetic image ${media.id}`);
  await save("albums.md", [
    "# Inventories", '<a id="album-111"></a>', "### First album",
    "- Album URL: [First album](https://example.org/albums/111/)", "- Photos: 12", "",
    '<a id="album-222"></a>', "### Unrelated album",
    "- Album URL: [Other album](https://example.org/albums/222/)", "- Photos: 99", ""
  ].join("\n"));
  return { repoRoot, contentRoot, raw, save, saveRecord };
}
