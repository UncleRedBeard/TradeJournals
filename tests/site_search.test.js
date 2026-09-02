"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");
const evidenceSource = require("../site_example/evidence-source.json");
const { searchJournals, tokenize } = require("../site_example/journal-search.js");

const journals = evidenceSource.journals;

test("Vespa electrical query excludes partial bath and shed matches", () => {
  const results = searchJournals(
    journals,
    "What evidence covers Vespa electrical work?"
  );

  assert.deepEqual(results.map(({ entry }) => entry.title), [
    "1964 Vespa Restoration"
  ]);
});

test("bath query returns both room-specific bath journals", () => {
  const results = searchJournals(journals, "Which albums document bath work?");
  const titles = results.map(({ entry }) => entry.title);

  assert.deepEqual(new Set(titles), new Set([
    "Guest Bath Restoration",
    "Master Bath Restoration"
  ]));
});

test("entry and landing query requires broad token coverage", () => {
  const results = searchJournals(
    journals,
    "Show the entry and landing floor work"
  );

  assert.deepEqual(results.map(({ entry }) => entry.title), [
    "Entry Restoration",
    "Landing Restoration"
  ]);
});

test("studio status query resolves the dedicated ballet studio", () => {
  const results = searchJournals(
    journals,
    "What is the ballet studio completion status?"
  );

  assert.equal(results[0].entry.title, "Ballet Barre Studio Restoration");
});

test("query boilerplate is removed before scoring", () => {
  assert.deepEqual(tokenize("Which albums document bath work?"), ["bath"]);
});
