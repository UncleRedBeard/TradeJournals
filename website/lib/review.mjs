import { createHash } from "node:crypto";
import { contentError } from "./schema.mjs";

function ordered(value) {
  if (Array.isArray(value)) return value.map(ordered);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.keys(value).sort().map(key => [key, ordered(value[key])]));
  }
  return value;
}

export function digestRecord(record) {
  return createHash("sha256").update(JSON.stringify(ordered(record))).digest("hex");
}

function snapshots(value) {
  const result = new Map();
  for (const group of ["records", "sources"]) {
    if (!Array.isArray(value?.[group])) throw contentError("INVALID_REVIEW", "pilot", group, "Expected fingerprint records");
    for (const entry of value[group]) {
      if (!entry || typeof entry.key !== "string" || !entry.key.trim() || !/^[a-f0-9]{64}$/.test(entry.sha256)) {
        throw contentError("INVALID_REVIEW", "pilot", group, "Expected a key and SHA-256 fingerprint");
      }
      const key = `${group}:${entry.key}`;
      if (result.has(key)) throw contentError("INVALID_REVIEW", "pilot", group, `Duplicate fingerprint key: ${entry.key}`);
      result.set(key, { ...entry });
    }
  }
  return result;
}

export function compareReview(review, actual) {
  if (!["candidate", "reviewed"].includes(review?.state)) throw contentError("INVALID_REVIEW", "pilot", "state", "Expected candidate or reviewed");
  const saved = snapshots(review);
  const current = snapshots(actual);
  const changedKeys = [...new Set([...saved.keys(), ...current.keys()])]
    .filter(key => saved.get(key)?.sha256 !== current.get(key)?.sha256)
    .map(key => (current.get(key) ?? saved.get(key)).key);
  return {
    state: review.state === "candidate" ? "candidate" : changedKeys.length ? "stale" : "current",
    changedKeys: [...new Set(changedKeys)].sort()
  };
}
