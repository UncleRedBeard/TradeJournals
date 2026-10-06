import assert from "node:assert/strict";
import { cp, readFile, symlink } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { buildWebsite } from "../scripts/build.mjs";
import { writeFixture } from "./fixtures.mjs";

const websiteRoot = fileURLToPath(new URL("..", import.meta.url));
const repoRoot = fileURLToPath(new URL("../..", import.meta.url));

test("preview renders the Office record and review notice without a contact form", async () => {
  const result = await buildWebsite({ mode: "preview", repoRoot, websiteRoot });
  const page = await readFile(path.join(websiteRoot, ".preview-dist/work/office-restoration/index.html"), "utf8");

  assert.match(page, /Toil &amp; Timber Restoration/);
  assert.match(page, /Historic floors, interior woodwork, and architectural restoration\./);
  assert.ok(result.model.reviewNotice);
  assert.ok(page.includes(result.model.reviewNotice));
  assert.match(page, /https:\/\/www\.flickr\.com\/photos\/boocher\/53921322250\/in\/set-72177720316928566\//);
  assert.match(page, /\/media\/flickr-53921322250\.jpg/);
  assert.doesNotMatch(page, /<form[^>]*action=/);
  assert.doesNotMatch(page, /01_the_residence_1894/);
});

test("homepage links every selected project in folio order and keeps inquiries disabled", async () => {
  await buildWebsite({ mode: "preview", repoRoot, websiteRoot });
  const page = await readFile(path.join(websiteRoot, ".preview-dist/index.html"), "utf8");

  assert.match(page, /href="#documented-projects"/);
  assert.match(page, /id="documented-projects"/);
  assert.match(page, /href="#practice"/);
  assert.match(page, /id="practice"/);
  assert.match(page, /href="#workshop-studies"/);
  assert.match(page, /id="workshop-studies"/);
  const cards = [...page.matchAll(/<article\b[^>]*>.*?<\/article>/gs)].map(match => match[0]);
  const projectIds = ["living-room-studio-restoration", "entry-restoration", "guest-bath-dresser-vanity", "master-bedroom-restoration", "returning-to-clay", "agfa-isolette"];
  assert.equal(cards.length, projectIds.length);
  for (const [index, id] of projectIds.entries()) {
    assert.ok(cards[index].includes(`href="/work/${id}/"`), `${id} has a working story link in the selected order`);
    assert.match(cards[index], /<img[^>]+alt="[^"]+"/);
  }
  const contactButtons = [...page.matchAll(/<button\b[^>]*>Email us — coming soon<\/button>/g)];
  assert.ok(contactButtons.length > 0);
  for (const [button] of contactButtons) assert.match(button, /\bdisabled\b/);
  assert.doesNotMatch(page, /mailto:/);
  assert.doesNotMatch(page, /<form\b/);
});

test("shared frame reaches homepage sections from every inner route and retains font licensing and keyboard access", async () => {
  const { model } = await buildWebsite({ mode: "preview", repoRoot, websiteRoot });
  const routes = ["/", "/tradejournals/", ...model.projects.flatMap(project => [project.href, project.archiveHref])];
  for (const route of routes) {
    const page = await readFile(path.join(websiteRoot, ".preview-dist", route.slice(1), "index.html"), "utf8");
    const header = page.match(/<header\b[^>]*>.*?<\/header>/s)?.[0];
    const footer = page.match(/<footer\b[^>]*>.*?<\/footer>/s)?.[0];
    assert.ok(header && footer, `${route} has the shared landmarks`);
    assert.equal([...page.matchAll(/<header\b/g)].length, 1);
    assert.equal([...page.matchAll(/<footer\b/g)].length, 1);
    const prefix = route === "/" ? "" : "/";
    for (const fragment of ["documented-projects", "practice", "workshop-studies"]) {
      assert.ok(header.includes(`href="${prefix}#${fragment}"`), `${route} links to the homepage ${fragment} section`);
    }
    assert.match(header, /href="\/tradejournals\/"/);
    assert.match(header, /aria-label="Primary navigation"/);
    assert.match(footer, /<button\b[^>]*\bdisabled\b[^>]*>Email us — coming soon<\/button>/);
    assert.match(page, /href="#main-content"[^>]*>Skip to content/);
    assert.match(page, /<main\b[^>]*id="main-content"[^>]*tabindex="-1"/);
    assert.match(page, /@font-face[^}]*data:font\/woff2;base64,/);
    assert.match(page, /<template id="font-license">.*SIL OPEN FONT LICENSE.*<\/template>/s);
    assert.equal([...page.matchAll(/id="font-license"/g)].length, 1);
  }
});

test("every route has one distinct description and preserves preview noindex", async () => {
  const { model } = await buildWebsite({ mode: "preview", repoRoot, websiteRoot });
  const routes = ["/", "/tradejournals/", ...model.projects.flatMap(project => [project.href, project.archiveHref])];
  const descriptions = new Set();
  for (const route of routes) {
    const page = await readFile(path.join(websiteRoot, ".preview-dist", route.slice(1), "index.html"), "utf8");
    const tags = [...page.matchAll(/<meta\b[^>]*name="description"[^>]*>/g)];
    assert.equal(tags.length, 1, `${route} has exactly one description`);
    const description = tags[0][0].match(/content="([^"]+)"/)?.[1];
    assert.ok(description?.trim(), `${route} has useful text`);
    assert.ok(!descriptions.has(description), `${route} has distinct text`);
    descriptions.add(description);
    assert.match(page, /<meta name="robots" content="noindex, nofollow"/);
  }
});

test("candidate preview renders explicit occupancy and selected services with their evidence links", async t => {
  const fixture = await writeFixture(t);
  const fixtureWebsiteRoot = path.join(fixture.repoRoot, "website");
  fixture.raw.projects[0].summary = 'A "record" of <original> boards & careful repair.';
  fixture.raw.projects[0].occupancy = { state: "current", label: "Current barre studio" };
  await fixture.saveRecord("projects/project-one.json", fixture.raw.projects[0]);
  await fixture.saveRecord("services/historic-floors.json", {
    ...fixture.raw.services[0], description: "Keep <original> boards & document choices."
  });
  await fixture.saveRecord("services/unselected-service.json", {
    ...fixture.raw.services[0], id: "unselected-service", title: "Unselected service"
  });
  await cp(path.join(websiteRoot, "astro.config.mjs"), path.join(fixtureWebsiteRoot, "astro.config.mjs"));
  await cp(path.join(websiteRoot, "lib"), path.join(fixtureWebsiteRoot, "lib"), { recursive: true });
  await cp(path.join(websiteRoot, "src"), path.join(fixtureWebsiteRoot, "src"), { recursive: true });
  await symlink(path.join(websiteRoot, "node_modules"), path.join(fixtureWebsiteRoot, "node_modules"));
  await cp(path.join(repoRoot, "site_example"), path.join(fixture.repoRoot, "site_example"), { recursive: true });

  await buildWebsite({ mode: "preview", repoRoot: fixture.repoRoot, websiteRoot: fixtureWebsiteRoot });
  const page = await readFile(path.join(fixtureWebsiteRoot, ".preview-dist/work/project-one/index.html"), "utf8");

  assert.match(page, /<strong[^>]*>Stage:<\/strong> Recorded work/);
  assert.match(page, /<strong[^>]*>Recorded:<\/strong> 2026/);
  assert.equal([...page.matchAll(/Current barre studio/g)].length, 1);
  assert.match(page, /href="\/#documented-projects"/);
  assert.doesNotMatch(page, /href="\/#workshop-studies"/);

  const journal = await readFile(path.join(fixtureWebsiteRoot, ".preview-dist/tradejournals/project-one/index.html"), "utf8");
  assert.equal([...journal.matchAll(/<h1\b/g)].length, 1, "a journal without a story retains one page heading");
  assert.match(journal, /<meta name="description" content="TradeJournal: A &quot;record&quot; of <original> boards &amp; careful repair\."/);
  assert.match(journal, /href="\/work\/project-one\/"/);

  const homepage = await readFile(path.join(fixtureWebsiteRoot, ".preview-dist/index.html"), "utf8");
  const practice = homepage.match(/<section\b[^>]*id="practice"[^>]*>.*?<\/section>/s)?.[0];
  assert.ok(practice, "selected services have a navigable practice section");
  assert.match(practice, /Keep &lt;original&gt; boards &amp; document choices\./);
  assert.match(practice, /href="\/work\/project-one\/"[^>]*>Recorded project-one<\/a>/);
  assert.doesNotMatch(practice, /Unselected service|<original>/);

  await fixture.saveRecord("home.json", { ...fixture.raw.home, serviceIds: [] });
  await buildWebsite({ mode: "preview", repoRoot: fixture.repoRoot, websiteRoot: fixtureWebsiteRoot });
  const withoutServices = await readFile(path.join(fixtureWebsiteRoot, ".preview-dist/index.html"), "utf8");
  assert.match(withoutServices, /<aside\b[^>]*id="practice"/);
  assert.equal([...withoutServices.matchAll(/id="practice"/g)].length, 1);
  assert.doesNotMatch(withoutServices, /Services and assessment/);
});

test("each journal keeps one story heading and links to its project and archive", async () => {
  const { model } = await buildWebsite({ mode: "preview", repoRoot, websiteRoot });
  for (const project of model.projects) {
    const page = await readFile(path.join(websiteRoot, ".preview-dist", project.archiveHref.slice(1), "index.html"), "utf8");
    const main = page.match(/<main\b[^>]*>.*?<\/main>/s)?.[0];
    assert.ok(main, `${project.id} has journal content`);
    assert.equal([...main.matchAll(/<h1\b/g)].length, 1, `${project.id} has one story title`);
    assert.ok(main.includes('href="/tradejournals/"'), `${project.id} provides a return to the archive`);
    assert.ok(main.includes(`href="${project.href}"`), `${project.id} links to its own project`);
    assert.equal([...main.matchAll(/aria-label="Project record"/g)].length, 1);
  }
});

test("project photographs remain in approved order with captions and source links behind a working gallery jump", async () => {
  const { model } = await buildWebsite({ mode: "preview", repoRoot, websiteRoot });
  const escapeHtml = value => value.replaceAll("&", "&amp;").replaceAll('"', "&quot;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
  const escapeHtmlText = value => escapeHtml(value).replaceAll("'", "&#39;");
  for (const project of model.projects) {
    const page = await readFile(path.join(websiteRoot, ".preview-dist", project.href.slice(1), "index.html"), "utf8");
    assert.ok(page.includes('href="#project-photographs"'), `${project.id} lets visitors jump to photographs`);
    assert.match(page, /<section\b[^>]*id="project-photographs"[^>]*aria-labelledby="project-photographs-heading"/);
    assert.match(page, /<h2\b[^>]*id="project-photographs-heading"/);
    const figures = [...page.matchAll(/<figure\b[^>]*>.*?<\/figure>/gs)].map(match => match[0]);
    assert.equal(figures.length, project.gallery.length, `${project.id} keeps every selected image once`);
    for (const [index, image] of project.gallery.entries()) {
      const figure = figures[index];
      assert.ok(figure.includes(`src="${escapeHtml(image.src)}"`), `${project.id} preserves image order`);
      assert.ok(figure.includes(`alt="${escapeHtml(image.alt)}"`));
      assert.ok(figure.includes(`href="${escapeHtml(image.sourceUrl)}"`));
      if (image.caption) assert.ok(figure.includes(escapeHtmlText(image.caption)), `${project.id} preserves the caption`);
    }
    assert.ok(page.includes(`href="${project.archiveHref}"`), `${project.id} retains its journal link`);
  }
});
