import assert from "node:assert/strict";
import { cp, mkdir, readFile, symlink } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { buildWebsite } from "../scripts/build.mjs";
import { prepareSite } from "../lib/prepare.mjs";
import { writeFixture } from "./fixtures.mjs";

const installedWebsite = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

async function buildFixture(t) {
  const fixture = await writeFixture(t);
  const websiteRoot = path.join(fixture.repoRoot, "website");
  for (const file of ["src", "lib", "astro.config.mjs", "package.json"]) {
    await cp(path.join(installedWebsite, file), path.join(websiteRoot, file), { recursive: true });
  }
  await mkdir(path.join(fixture.contentRoot, "stories"), { recursive: true });
  await symlink(path.join(installedWebsite, "node_modules"), path.join(websiteRoot, "node_modules"));
  await fixture.save("site_example/journal-search.js", await readFile(path.join(installedWebsite, "../site_example/journal-search.js")));
  const build = mode => buildWebsite({ mode, repoRoot: fixture.repoRoot, websiteRoot });
  const output = (file, mode = "preview") => readFile(path.join(websiteRoot, mode === "preview" ? ".preview-dist" : "dist", file), "utf8");
  return { ...fixture, websiteRoot, build, output };
}

test("synthetic builds isolate copy, featured order and shared style, then produce a reviewed release", async t => {
  const f = await buildFixture(t);
  f.raw.home.featuredProjectIds = ["project-one", "project-two"];
  await f.saveRecord("home.json", f.raw.home);
  await f.build("preview");
  const baselineProject = await f.output("work/project-one/index.html");
  const summary = "Synthetic revised floor restoration summary.";
  f.raw.projects[0].summary = summary;
  await f.saveRecord("projects/project-one.json", f.raw.projects[0]);
  await f.build("preview");
  assert.match(await f.output("index.html"), new RegExp(summary));
  assert.match(await f.output("work/project-one/index.html"), new RegExp(summary));
  assert.equal(JSON.parse(await f.output("search.json"))[0].summary, summary);
  assert.ok(!baselineProject.includes(summary));
  const projectBeforeOrder = await f.output("work/project-one/index.html");
  f.raw.home.featuredProjectIds.reverse();
  await f.saveRecord("home.json", f.raw.home);
  const ordered = await f.build("preview");
  const home = await f.output("index.html");
  const selectedWork = home.slice(home.indexOf("Restoration portfolio"));
  assert.ok(selectedWork.indexOf("Recorded project-two") < selectedWork.indexOf("Recorded project-one"));
  assert.match(home, /href="\/work\/project-two\/"[^>]*>See the work/u);
  assert.equal(await f.output("work/project-one/index.html"), projectBeforeOrder);

  const componentPath = "website/src/components/ProjectCard.astro";
  const component = await readFile(path.join(f.repoRoot, componentPath), "utf8");
  assert.ok(component.includes("border-top: 1px solid"));
  const largerStyles = Array.from({ length: 150 }, (_, i) =>
    `.project-card .fixture-${i} { padding: ${i}px; margin: ${i}px; }`).join("\n");
  await f.save(componentPath, component.replace("border-top: 1px solid", "border-top: 3px solid")
    .replace("</style>", `${largerStyles}</style>`));
  const styled = await f.build("preview");
  assert.deepEqual(styled.model, ordered.model);
  assert.match(await f.output("index.html"), /border-top:\s*3px solid/u);
  assert.notEqual(await f.output("index.html"), home);

  await assert.rejects(f.build("release"), { code: "UNREVIEWED_CONTENT" });
  const { report } = await prepareSite({ repoRoot: f.repoRoot, contentRoot: f.contentRoot, mode: "preview" });
  await f.saveRecord("reviews/pilot.json", { ...f.raw.review, state: "reviewed", ...report.snapshot });
  const released = await f.build("release");
  assert.equal(released.output.pages, 6);
  assert.equal(released.model.reviewNotice, "");
  for (const file of ["index.html", "tradejournals/index.html", ...f.raw.projects.flatMap(project => [
    `work/${project.id}/index.html`, `tradejournals/${project.id}/index.html`
  ])]) {
    const html = await f.output(file, "release");
    assert.doesNotMatch(html, /name="robots"[^>]*noindex|<aside class="review-notice"|Local review preview/iu);
  }
});

test("homepage separates the restoration portfolio from workshop stories", async t => {
  const f = await buildFixture(t);
  f.raw.home.featuredProjectIds = ["project-one"];
  f.raw.home.workshopProjectIds = ["project-two"];
  await f.saveRecord("home.json", f.raw.home);
  await f.build("preview");
  const home = await f.output("index.html");
  assert.match(home, /Restoration portfolio/);
  assert.match(home, /From the workshop/);
  assert.ok(home.indexOf("Recorded project-one") < home.indexOf("From the workshop"));
  assert.ok(home.indexOf("From the workshop") < home.indexOf("Recorded project-two"));
});
