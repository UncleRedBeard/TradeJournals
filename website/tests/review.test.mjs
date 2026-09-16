import test from "node:test";
import assert from "node:assert/strict";
import { compareReview, digestRecord } from "../lib/review.mjs";

const digest = value => [{ key: "journal:journal-a", sha256: value.repeat(64) }];

test("candidate snapshots remain candidates, even when fingerprints match", () => {
  const actual = { records: [], sources: digest("a") };
  const review = { schemaVersion: 1, id: "pilot", state: "candidate", ...actual };
  const before = structuredClone(review);
  assert.deepEqual(compareReview(review, actual), { state: "candidate", changedKeys: [] });
  assert.deepEqual(review, before);
});

test("reviewed snapshots detect changed, added, and removed selections", () => {
  const saved = { state: "reviewed", records: [], sources: digest("a") };
  assert.deepEqual(compareReview(saved, { records: [], sources: digest("a") }), { state: "current", changedKeys: [] });
  assert.deepEqual(compareReview(saved, { records: [], sources: digest("b") }), { state: "stale", changedKeys: ["journal:journal-a"] });
  assert.deepEqual(compareReview(saved, { records: [], sources: [] }), { state: "stale", changedKeys: ["journal:journal-a"] });
  assert.equal(compareReview({ ...saved, sources: [] }, { records: [], sources: digest("a") }).state, "stale");
});

test("content changes expire a saved review while array order is intentional", () => {
  const record = { nested: { b: 2, a: 1 }, ids: ["one", "two"] };
  assert.equal(digestRecord(record), digestRecord({ ids: ["one", "two"], nested: { a: 1, b: 2 } }));
  assert.notEqual(digestRecord(record), digestRecord({ ...record, ids: ["two", "one"] }));
  const saved = { state: "reviewed", records: [{ key: "home:home", sha256: digestRecord(record) }], sources: [] };
  const actual = { records: [{ key: "home:home", sha256: digestRecord({ ...record, title: "New" }) }], sources: [] };
  assert.deepEqual(compareReview(saved, actual), { state: "stale", changedKeys: ["home:home"] });
});

test("review bookkeeping is not content, and malformed snapshots fail closed", () => {
  const actual = { records: [], sources: digest("a") };
  const reviewed = { schemaVersion: 1, id: "pilot", state: "reviewed", ...actual };
  assert.equal(compareReview(reviewed, actual).state, "current");
  for (const bad of [
    { ...reviewed, state: "published" },
    { ...reviewed, sources: [...digest("a"), ...digest("a")] },
    { ...reviewed, sources: [{ key: "journal:journal-a", sha256: "invalid" }] }
  ]) assert.throws(() => compareReview(bad, actual), { code: "INVALID_REVIEW" });
});
