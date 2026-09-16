import { spawnSync } from "node:child_process";
import { readFile, readdir, realpath, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { isHttpsUrl } from "../lib/schema.mjs";

const websiteRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const parserPath = path.resolve(websiteRoot, "..", "scripts", "check_website_html.py");

function outputError(code, file, message) {
  return Object.assign(new Error(`${file}: ${message}`), { code, file });
}

function pathForUrl(urlPath) {
  const decoded = decodeURIComponent(urlPath);
  if (!decoded.startsWith("/") || decoded.startsWith("//") || decoded.includes("\\") || decoded.split("/").some(part => part === "..")) return null;
  if (decoded === "/") return "index.html";
  const relative = decoded.slice(1);
  return path.extname(relative) ? relative : `${relative.replace(/\/$/u, "")}/index.html`;
}

function srcsetValues(value) {
  if (!value.trim()) return [];
  return value.split(",").map(part => {
    const tokens = part.trim().split(/\s+/u);
    if (tokens.length < 1 || tokens.length > 2 || !tokens[0]) return null;
    if (tokens[1] && !/^(?:\d+(?:\.\d+)?x|\d+w)$/u.test(tokens[1])) return null;
    return tokens[0];
  });
}

async function filesUnder(root) {
  const result = [];
  async function visit(relative) {
    const directory = path.join(root, relative);
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const next = path.join(relative, entry.name);
      if (entry.isSymbolicLink()) throw outputError("UNEXPECTED_OUTPUT", next, "Output may not contain symbolic links");
      if (entry.isDirectory()) await visit(next);
      else if (entry.isFile()) result.push(next.split(path.sep).join("/"));
      else throw outputError("UNEXPECTED_OUTPUT", next, "Output contains a non-regular file");
    }
  }
  await visit("");
  return result.sort();
}

function parseDocuments(documents) {
  const run = spawnSync("python3", [parserPath], { input: JSON.stringify(documents), encoding: "utf8", maxBuffer: 1024 * 1024 });
  if (run.error || run.status !== 0) throw outputError("PARSER_ERROR", "scripts/check_website_html.py", "HTML parser failed while validating output");
  try { return JSON.parse(run.stdout); }
  catch { throw outputError("PARSER_ERROR", "scripts/check_website_html.py", "HTML parser returned invalid JSON"); }
}

function expectedPages(model) {
  return ["index.html", "tradejournals/index.html", ...model.projects.flatMap(project => [
    pathForUrl(project.href), pathForUrl(project.archiveHref)
  ])].sort();
}

function selectedMedia(model) {
  return new Set([
    ...(model.home.hero ? [model.home.hero.src.slice(1)] : []),
    ...model.projects.flatMap(project => [
      ...project.gallery.map(image => image.src.slice(1)),
      ...project.searchImages.map(image => image.src.slice(1))
    ])
  ]);
}

export async function checkOutput({ outputRoot, model }) {
  const root = await realpath(outputRoot).catch(() => { throw outputError("MISSING_OUTPUT", outputRoot, "Output directory is unavailable"); });
  if (!(await stat(root)).isDirectory()) throw outputError("MISSING_OUTPUT", outputRoot, "Output root must be a directory");
  const files = await filesUnder(root);
  const pages = expectedPages(model);
  const allowed = new Set([...pages, "search.json", "scripts/journal-search.js", "scripts/archive-search.js", ...selectedMedia(model)]);
  for (const file of files) {
    if (!allowed.has(file)) throw outputError("UNEXPECTED_OUTPUT", file, "Output contains an unplanned file");
  }
  for (const file of allowed) {
    if (!files.includes(file)) throw outputError("MISSING_OUTPUT", file, "Expected output file is missing");
  }
  let search;
  try { search = JSON.parse(await readFile(path.join(root, "search.json"), "utf8")); }
  catch { throw outputError("SEARCH_MISMATCH", "search.json", "Search output is not valid JSON"); }
  if (JSON.stringify(search) !== JSON.stringify(model.searchEntries)) throw outputError("SEARCH_MISMATCH", "search.json", "Search output differs from the prepared public model");

  for (const file of files.filter(file => /\.(?:html|json|js|css)$/u.test(file))) {
    const text = await readFile(path.join(root, file), "utf8");
    if (/\/(?:Users|private|home)\/[A-Za-z0-9_./-]+/u.test(text) || /file:\/\//iu.test(text)) {
      throw outputError("PRIVATE_OUTPUT", file, "Output contains a private local path");
    }
  }
  const documents = await Promise.all(pages.map(async file => ({ path: file, html: await readFile(path.join(root, file), "utf8") })));
  const parsed = parseDocuments(documents);
  const byPage = new Map(parsed.map(document => [document.path, document]));
  let references = 0;
  for (const document of parsed) {
    const html = documents.find(item => item.path === document.path).html;
    if (new Set(document.ids).size !== document.ids.length) {
      throw outputError("BROKEN_FRAGMENT", document.path, "Output contains duplicate fragment targets");
    }
    const hasNotice = /class=["'][^"']*\breview-notice\b/u.test(html);
    const hasNoindex = document.robots.some(value => /(?:^|[,\s])noindex(?:$|[,\s])/iu.test(value));
    if (model.reviewNotice ? !hasNoindex || !html.includes(model.reviewNotice) : hasNoindex || hasNotice) {
      throw outputError("PREVIEW_METADATA", document.path, "Preview metadata does not match the prepared review state");
    }
    for (const reference of document.references) {
      references += 1;
      if (reference.attribute !== "href" && !reference.value.trim()) {
        throw outputError("UNSAFE_REFERENCE", document.path, `Empty ${reference.attribute} reference`);
      }
      const values = reference.attribute === "srcset" ? srcsetValues(reference.value) : [reference.value];
      if (!values || values.some(value => value === null)) throw outputError("UNSAFE_REFERENCE", document.path, `Invalid ${reference.attribute} value`);
      for (const value of values) {
        if (!value) continue;
        if (reference.tag === "base" || value.startsWith("//") || /[\\\x00-\x20]/u.test(value)) {
          throw outputError("UNSAFE_REFERENCE", document.path, `Unsafe reference ${value}`);
        }
        let parsedUrl;
        try { parsedUrl = new URL(value, `https://output.invalid/${document.path.replace(/index\.html$/u, "")}`); }
        catch { throw outputError("UNSAFE_REFERENCE", document.path, `Invalid reference ${value}`); }
        if (parsedUrl.origin !== "https://output.invalid") {
          if (reference.tag !== "a" || reference.attribute !== "href" || !isHttpsUrl(value)) {
            throw outputError("UNSAFE_REFERENCE", document.path, `Unexpected external reference ${value}`);
          }
          continue;
        }
        const target = pathForUrl(parsedUrl.pathname);
        if (!target || !files.includes(target)) throw outputError("BROKEN_REFERENCE", document.path, `Missing local reference ${value}`);
        if (parsedUrl.hash) {
          const targetDocument = byPage.get(target);
          if (!targetDocument || !targetDocument.ids.includes(decodeURIComponent(parsedUrl.hash.slice(1)))) {
            throw outputError("BROKEN_FRAGMENT", document.path, `Missing fragment target ${value}`);
          }
        }
      }
    }
  }
  for (const project of model.projects) {
    const file = pathForUrl(project.href);
    const links = new Set(byPage.get(file).references.filter(ref => ref.attribute === "href").map(ref => ref.value));
    for (const source of [...project.gallery, ...project.albums]) {
      if (!links.has(source.sourceUrl)) throw outputError("MISSING_SOURCE_LINK", file, `Missing source link ${source.sourceUrl}`);
    }
  }
  return { pages: pages.length, files: files.length, references };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const outputArg = process.argv[2];
  if (!outputArg) throw new Error("Usage: node scripts/check-output.mjs <output-directory>");
  const model = JSON.parse(await readFile(path.join(websiteRoot, "src", "generated", "site.json"), "utf8"));
  const report = await checkOutput({ outputRoot: path.resolve(websiteRoot, outputArg), model });
  process.stdout.write(`Validated ${report.pages} pages and ${report.files} files.\n`);
}
