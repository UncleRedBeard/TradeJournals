import { readFile, readdir, realpath, stat } from "node:fs/promises";
import path from "node:path";
import { contentError, isRelativePath, parseRecord } from "./schema.mjs";

// Used for both editable records and selected story files. Resolve symlinks before reading.
export async function containedFile(root, relative, recordId = relative) {
  if (!isRelativePath(relative)) throw contentError("INVALID_PATH", recordId, relative, "Expected a relative file path without traversal");
  try {
    const base = await realpath(root);
    const file = await realpath(path.join(base, relative));
    const within = path.relative(base, file);
    if (!within || within.startsWith(`..${path.sep}`) || within === ".." || path.isAbsolute(within)) {
      throw contentError("INVALID_PATH", recordId, relative, "File escapes its allowed root");
    }
    if (!(await stat(file)).isFile()) throw contentError("INVALID_PATH", recordId, relative, "Expected a regular file");
    return file;
  } catch (error) {
    if (error.recordId) throw error;
    throw contentError("MISSING_FILE", recordId, relative, `Required file is unavailable: ${relative}`);
  }
}

export async function loadContent(contentRoot) {
  const readRecord = async (relative, kind) => {
    const file = await containedFile(contentRoot, relative);
    let record;
    try { record = JSON.parse(await readFile(file, "utf8")); }
    catch { throw contentError("INVALID_JSON", relative, relative, `Cannot read JSON record: ${relative}`); }
    const expectedId = path.basename(relative, ".json");
    if (record?.id !== expectedId) {
      throw contentError("ID_FILENAME_MISMATCH", record?.id ?? expectedId, relative, `Record ID must match filename ${expectedId}`);
    }
    return parseRecord(kind, record, relative);
  };
  const collection = async (directory, kind) => {
    let names;
    try { names = await readdir(path.join(contentRoot, directory)); }
    catch (error) {
      if (error.code === "ENOENT") return [];
      throw contentError("INVALID_PATH", directory, directory, `Cannot read ${directory}`);
    }
    const records = [];
    for (const name of names.filter(name => name.endsWith(".json")).sort()) {
      records.push(await readRecord(`${directory}/${name}`, kind));
    }
    return records;
  };
  return {
    site: await readRecord("site.json", "site"),
    home: await readRecord("home.json", "home"),
    services: await collection("services", "service"),
    projects: await collection("projects", "project"),
    media: await collection("media", "media"),
    review: await readRecord("reviews/pilot.json", "review")
  };
}

function unique(values, recordId, field) {
  const seen = new Set();
  for (const [index, value] of values.entries()) {
    if (seen.has(value)) throw contentError("DUPLICATE_REFERENCE", recordId, `${field}[${index}]`, `Duplicate selection: ${value}`);
    seen.add(value);
  }
}

export function validateContent(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) throw contentError("INVALID_CONTENT", "content", "content", "Expected content records");
  const result = {};
  for (const kind of ["site", "home", "review"]) result[kind] = parseRecord(kind, raw[kind], kind);
  const maps = {};
  for (const [group, kind] of [["services", "service"], ["projects", "project"], ["media", "media"]]) {
    if (!Array.isArray(raw[group])) throw contentError("INVALID_CONTENT", group, group, "Expected a record array");
    result[group] = raw[group].map((record, i) => parseRecord(kind, record, `${group}[${i}]`));
    maps[group] = new Map();
    for (const [i, record] of result[group].entries()) {
      if (maps[group].has(record.id)) throw contentError("DUPLICATE_ID", record.id, `${group}[${i}].id`, `Duplicate ${kind} ID: ${record.id}`);
      maps[group].set(record.id, record);
    }
  }
  const lookup = (group, id, owner, field) => {
    const value = maps[group].get(id);
    if (!value) throw contentError("MISSING_REFERENCE", owner, field, `Unknown ${group} reference: ${id}`);
    return value;
  };
  const selections = (ids, group, owner, field) => {
    unique(ids, owner, field);
    ids.forEach((id, i) => lookup(group, id, owner, `${field}[${i}]`));
  };
  selections(result.home.featuredProjectIds, "projects", "home", "home.featuredProjectIds");
  selections(result.home.workshopProjectIds ?? [], "projects", "home", "home.workshopProjectIds");
  for (const [index, id] of (result.home.workshopProjectIds ?? []).entries()) {
    if (result.home.featuredProjectIds.includes(id)) {
      throw contentError("DUPLICATE_REFERENCE", "home", `home.workshopProjectIds[${index}]`, `Project ${id} is already selected for the restoration portfolio`);
    }
  }
  selections(result.home.serviceIds, "services", "home", "home.serviceIds");
  if (result.home.heroMediaId) lookup("media", result.home.heroMediaId, "home", "home.heroMediaId");
  for (const service of result.services) selections(service.projectIds, "projects", service.id, `services.${service.id}.projectIds`);
  const albumOwners = new Map();
  for (const project of result.projects) {
    const prefix = `projects.${project.id}`;
    const galleryIds = project.gallery.map(placement => placement.mediaId);
    unique(galleryIds, project.id, `${prefix}.gallery`);
    unique(project.searchMediaIds, project.id, `${prefix}.searchMediaIds`);
    unique(project.albumKeys, project.id, `${prefix}.albumKeys`);
    unique(project.sourceRefs.map(ref => `${ref.kind}:${ref.path}#${ref.anchor ?? ""}`), project.id, `${prefix}.sourceRefs`);
    for (const [index, key] of project.albumKeys.entries()) {
      const owner = albumOwners.get(key);
      if (owner && owner !== project.id) {
        throw contentError("DUPLICATE_REFERENCE", project.id, `${prefix}.albumKeys[${index}]`, `Album ${key} is already owned by project ${owner}`);
      }
      albumOwners.set(key, project.id);
      if (!project.sourceRefs.some(ref => ref.kind === "inventory" && ref.anchor === `album-${key.split(":")[1]}`)) {
        throw contentError("MISSING_REFERENCE", project.id, `${prefix}.albumKeys[${index}]`, `Album ${key} needs a matching inventory source`);
      }
    }
    for (const [field, ids] of [["gallery", galleryIds], ["searchMediaIds", project.searchMediaIds]]) {
      ids.forEach((id, i) => {
        const media = lookup("media", id, project.id, `${prefix}.${field}[${i}]`);
        if (media.kind !== "evidence") throw contentError("INVALID_EVIDENCE", project.id, `${prefix}.${field}[${i}]`, "Project selections require evidence media");
        if (!project.albumKeys.includes(media.albumKey)) throw contentError("MISSING_REFERENCE", project.id, `${prefix}.${field}[${i}]`, `Media album ${media.albumKey} is not referenced by this project`);
      });
    }
  }
  return result;
}
