import { contentError, isHttpsUrl, isLocalUrl } from "./schema.mjs";

function safeDestination(url) {
  return isHttpsUrl(url) || isLocalUrl(url);
}

export function assertSafeMarkdownTree(tree) {
  const walk = node => {
    if (!node || typeof node !== "object") return;
    if (node.type === "html" || node.type === "image") {
      throw contentError("INVALID_MARKDOWN", "story", node.type, `Markdown ${node.type} nodes are not allowed`);
    }
    if (["link", "definition"].includes(node.type) && !safeDestination(node.url)) {
      throw contentError("INVALID_MARKDOWN", "story", "url", "Story links must use a public local or HTTPS destination");
    }
    for (const child of node.children ?? []) walk(child);
  };
  walk(tree);
  return tree;
}

export function remarkSafeMarkdown() {
  return tree => assertSafeMarkdownTree(tree);
}
