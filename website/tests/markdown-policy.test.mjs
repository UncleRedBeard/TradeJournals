import assert from "node:assert/strict";
import test from "node:test";
import { assertSafeMarkdownTree } from "../lib/markdown-policy.mjs";

test("rejects raw HTML before an Office story can be rendered", () => {
  assert.throws(
    () => assertSafeMarkdownTree({
      type: "root",
      children: [{ type: "html", value: "<script>run()</script>" }]
    }),
    error => error.code === "INVALID_MARKDOWN"
  );
});

test("rejects unsafe public links", () => {
  assert.throws(
    () => assertSafeMarkdownTree({
      type: "root",
      children: [{
        type: "paragraph",
        children: [{ type: "link", url: "javascript:alert(1)", children: [{ type: "text", value: "bad" }] }]
      }]
    }),
    error => error.code === "INVALID_MARKDOWN"
  );
});

test("allows an ordinary public story tree", () => {
  assert.doesNotThrow(() => assertSafeMarkdownTree({
    type: "root",
    children: [{ type: "heading", depth: 1, children: [{ type: "text", value: "Office Restoration" }] }]
  }));
});
