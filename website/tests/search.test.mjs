import assert from "node:assert/strict";
import { createRequire } from "node:module";
import test from "node:test";

const require = createRequire(import.meta.url);
const { searchJournals } = require("../../site_example/journal-search.js");

const office = {
  title: "Office Restoration",
  tags: ["floors", "original door", "woodwork"],
  summary: "Floor refinishing and reclamation of an original solid-wood door.",
  area: "office",
  source: "Office journal",
  url: "/work/office-restoration/"
};

test("archive search keeps the Office record discoverable by its original door", () => {
  const results = searchJournals([office], "door");

  assert.equal(results.length, 1);
  assert.equal(results[0].entry.url, "/work/office-restoration/");
});
