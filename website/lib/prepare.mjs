import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile, realpath } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { containedFile, loadContent, validateContent } from "./content.mjs";
import { contentError, isHttpsUrl, StableId } from "./schema.mjs";
import { compareReview, digestRecord } from "./review.mjs";

const inspectorPath = fileURLToPath(new URL("../../scripts/inspect_website_sources.py", import.meta.url));
const sourceKey = ref => `${ref.kind}:${ref.path}${ref.anchor ? `#${ref.anchor}` : ""}`;
const recordDigest = (kind, record) => ({ key: `${kind}:${record.id}`, sha256: digestRecord(record) });
const byKey = (a, b) => a.key.localeCompare(b.key, "en");
const isInside = (root, target) => {
  const relative = path.relative(root, target);
  return relative !== ".." && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative);
};

// Validate the subprocess boundary before using any of its facts in public data.
export function parseInspectionResult(output, requests) {
  const invalid = () => contentError("INVALID_SOURCE_RESPONSE", "sources", "inspector", "Source inspector returned incomplete or invalid facts");
  let facts;
  try { facts = JSON.parse(output); } catch { throw invalid(); }
  if (!Array.isArray(facts) || facts.length !== requests.length) throw invalid();
  const expected = new Map(requests.map(request => [request.key, request]));
  for (const fact of facts) {
    const request = expected.get(fact?.key);
    if (!request || typeof fact.sha256 !== "string" || !/^[a-f0-9]{64}$/.test(fact.sha256)) throw invalid();
    const allowed = request.kind === "inventory" ? ["key", "sha256", "count", "label", "sourceUrl"] : ["key", "sha256"];
    if (Object.keys(fact).some(key => !allowed.includes(key))) throw invalid();
    if (request.kind === "inventory" && (
      !Number.isSafeInteger(fact.count) || fact.count < 0 ||
      typeof fact.label !== "string" || !fact.label.trim() || !isHttpsUrl(fact.sourceUrl)
    )) throw invalid();
    expected.delete(fact.key);
  }
  return facts;
}

function inspectSources(repoRoot, requests) {
  const process = spawnSync("python3", [inspectorPath, "--repo-root", repoRoot], {
    input: JSON.stringify(requests), encoding: "utf8", timeout: 30000,
    maxBuffer: 1024 * 1024
  });
  if (process.error || process.status !== 0) {
    let diagnostic;
    try { diagnostic = JSON.parse(process.stderr); } catch { /* Non-JSON launch/usage failure. */ }
    if (diagnostic && ["code", "recordId", "field", "message"].every(key => typeof diagnostic[key] === "string")) {
      throw contentError(diagnostic.code, diagnostic.recordId, diagnostic.field, diagnostic.message);
    }
    throw contentError("SOURCE_ERROR", "sources", "inspector", "Source inspection failed; verify Python and the selected local sources");
  }
  return parseInspectionResult(process.stdout, requests);
}

function publicImage(media, placement) {
  const image = {
    id: media.id, src: `/media/${media.id}${path.extname(media.assetPath).toLowerCase()}`,
    alt: placement?.alt ?? media.alt, width: media.width, height: media.height,
    sourceUrl: media.sourceUrl
  };
  if (placement) {
    image.caption = placement.caption;
    image.role = placement.role;
    if (placement.focalPoint) image.focalPoint = [...placement.focalPoint];
  }
  return image;
}

function publicProject(project, mediaById, facts) {
  const gallery = project.gallery.map(placement => publicImage(mediaById.get(placement.mediaId), placement));
  const albums = project.albumKeys.map(key => {
    const references = project.sourceRefs.filter(ref => ref.kind === "inventory" && ref.anchor === `album-${key.split(":")[1]}`);
    if (references.length !== 1) throw contentError("AMBIGUOUS_SOURCE", project.id, "albumKeys", `Album ${key} needs exactly one inventory source`);
    const fact = facts.get(sourceKey(references[0]));
    const shown = project.gallery.filter(placement => mediaById.get(placement.mediaId).albumKey === key).length;
    if (shown > fact.count) throw contentError("INVALID_EVIDENCE", project.id, "gallery", "Shown photos exceed the recorded album count");
    return { key, label: fact.label, count: fact.count, sourceUrl: fact.sourceUrl, shown };
  });
  const result = {
    id: project.id, title: project.title, area: project.area, summary: project.summary,
    stage: project.stage, recorded: project.recorded, sourceLabel: project.sourceLabel,
    href: `/work/${project.id}/`, archiveHref: `/tradejournals/${project.id}/`,
    albums, gallery, searchImages: project.searchMediaIds.map(id => publicImage(mediaById.get(id)))
  };
  if (project.occupancy) result.occupancy = { ...project.occupancy };
  for (const field of ["introduction", "storyId", "evidenceBoundary"]) {
    if (project[field]) result[field] = project[field];
  }
  return result;
}

export async function prepareSite({ repoRoot, contentRoot, contentBoundaryRoot = repoRoot, mode, assetOverrides = new Map() }) {
  if (!["preview", "release"].includes(mode)) throw contentError("INVALID_MODE", "site", "mode", "Choose preview or release");
  let root, content, boundary;
  try {
    root = await realpath(repoRoot);
    content = await realpath(contentRoot);
    boundary = await realpath(contentBoundaryRoot);
  } catch {
    throw contentError("INVALID_PATH", "site", "contentRoot", "Repository, content and boundary roots must exist");
  }
  if (!isInside(boundary, content)) {
    throw contentError("INVALID_PATH", "site", "contentRoot", "Content must be inside its allowed boundary");
  }
  const records = validateContent(await loadContent(content));
  // Project JSON files are the explicitly curated public catalog. Images and
  // services are emitted only when referenced; the archive itself is never scanned.
  const mediaById = new Map(records.media.map(media => [media.id, media]));
  const selectedIds = new Set(records.projects.flatMap(project => [
    ...project.gallery.map(placement => placement.mediaId), ...project.searchMediaIds
  ]));
  if (records.home.heroMediaId) selectedIds.add(records.home.heroMediaId);
  const selectedMedia = records.media.filter(media => selectedIds.has(media.id));
  if (!(assetOverrides instanceof Map)) {
    throw contentError("INVALID_CONTENT", "site", "assetOverrides", "Asset overrides must be a Map");
  }
  const validatedOverrides = new Map();
  for (const [id, absolute] of assetOverrides) {
    if (!StableId.safeParse(id).success || !mediaById.has(id)) {
      throw contentError("MISSING_REFERENCE", id, "assetOverrides", `Unknown media override: ${id}`);
    }
    if (typeof absolute !== "string" || !path.isAbsolute(absolute)) {
      throw contentError("INVALID_PATH", id, "assetOverrides", "Asset override paths must be absolute");
    }
    validatedOverrides.set(id, await containedFile(boundary, path.relative(boundary, absolute), id));
  }
  const serviceById = new Map(records.services.map(service => [service.id, service]));
  const selectedServices = records.home.serviceIds.map(id => serviceById.get(id));
  const requests = new Map();
  for (const project of records.projects) {
    for (const ref of project.sourceRefs) requests.set(sourceKey(ref), { key: sourceKey(ref), ...ref });
  }
  for (const media of selectedMedia) {
    if (!validatedOverrides.has(media.id)) requests.set(`media:${media.id}`, { key: `media:${media.id}`, kind: "media", path: media.assetPath });
  }
  const facts = inspectSources(root, [...requests.values()]);
  // Private promotions do not exist at their eventual canonical path yet.
  // Keep their source snapshot key stable, hashing only the validated private file.
  for (const media of selectedMedia) {
    const override = validatedOverrides.get(media.id);
    if (override) facts.push({ key: `media:${media.id}`, sha256: createHash("sha256").update(await readFile(override)).digest("hex") });
  }
  const recordSnapshots = [
    recordDigest("site", records.site), recordDigest("home", records.home),
    ...selectedServices.map(record => recordDigest("service", record)),
    ...records.projects.map(record => recordDigest("project", record)),
    ...selectedMedia.map(record => recordDigest("media", record))
  ];
  for (const id of new Set(records.projects.flatMap(project => project.storyId ? [project.storyId] : []))) {
    const file = await containedFile(content, `stories/${id}.md`, id);
    const sha256 = createHash("sha256").update(await readFile(file)).digest("hex");
    recordSnapshots.push({ key: `story:${id}`, sha256 });
  }
  const snapshot = {
    records: recordSnapshots.sort(byKey),
    sources: facts.map(({ key, sha256 }) => ({ key, sha256 })).sort(byKey)
  };
  const review = compareReview(records.review, snapshot);
  if (mode === "release" && review.state !== "current") {
    throw contentError(review.state === "candidate" ? "UNREVIEWED_CONTENT" : "SOURCE_STALE", "pilot", "review", `Release requires current reviewed content; state is ${review.state}`);
  }
  const projects = records.projects.map(project => publicProject(project, mediaById, new Map(facts.map(fact => [fact.key, fact]))));
  const destinations = new Set(["/", "/tradejournals/", "/search.json", ...projects.flatMap(project => [project.href, project.archiveHref])]);
  for (const [i, link] of records.site.navigation.entries()) {
    const pathname = new URL(link.href, "https://website.invalid").pathname;
    if (!destinations.has(pathname)) throw contentError("MISSING_DESTINATION", "site", `navigation[${i}].href`, `No pilot route exists for ${link.href}`);
  }
  const site = {
    name: records.site.name, descriptor: records.site.descriptor, serviceLine: records.site.serviceLine,
    navigation: records.site.navigation.map(({ label, href }) => ({ label, href }))
  };
  if (records.site.contact) site.contact = { label: records.site.contact.label, href: records.site.contact.href };
  const home = {
    headline: records.home.headline, intro: records.home.intro,
    featuredProjectIds: [...records.home.featuredProjectIds],
    workshopProjectIds: [...(records.home.workshopProjectIds ?? [])],
    serviceIds: [...records.home.serviceIds]
  };
  if (records.home.heroMediaId) home.hero = publicImage(mediaById.get(records.home.heroMediaId));
  const searchEntries = projects.map((project, index) => ({
    title: project.title, area: project.area,
    summary: records.projects[index].searchSummary.trim() ? records.projects[index].searchSummary : project.summary,
    tags: [...records.projects[index].tags], source: project.archiveHref, url: project.href,
    images: project.searchImages,
    evidence: {
      stage: project.stage, recorded: project.recorded, sourceLabel: project.sourceLabel,
      ...(project.occupancy && { occupancy: { ...project.occupancy } })
    }
  }));
  const assetCopies = [];
  for (const media of selectedMedia) assetCopies.push({
    sourceAbsolute: validatedOverrides.get(media.id) ?? await containedFile(root, media.assetPath, media.id),
    publicRelative: publicImage(media).src.slice(1)
  });
  return {
    model: {
      site, home,
      services: selectedServices.map(({ id, title, description, projectIds }) => ({ id, title, description, projectIds: [...projectIds] })),
      projects, searchEntries,
      reviewNotice: mode === "release" ? "" : review.state === "current"
        ? "Local preview — reviewed content; this preview is not a deployment."
        : review.state === "candidate"
          ? "Local review preview — content and photo selections await review."
          : "Local review preview — selected content or sources changed since review."
    },
    report: { ...review, snapshot }, assetCopies
  };
}
