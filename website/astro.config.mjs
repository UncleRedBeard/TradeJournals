import { defineConfig } from "astro/config";
import { satteri } from "@astrojs/markdown-satteri";
import { assertSafeMarkdownTree } from "./lib/markdown-policy.mjs";

const mode = process.env.WK_SITE_MODE;
const publicDir = process.env.WK_PUBLIC_DIR;

if (!publicDir || !["preview", "release"].includes(mode)) {
  throw new Error("Use website/scripts/build.mjs so Astro receives validated prepared content.");
}

export default defineConfig({
  output: "static",
  // Keep the small pilot's styles with its HTML and its output contract stable.
  build: { inlineStylesheets: "always" },
  publicDir,
  outDir: mode === "preview" ? "./.preview-dist" : "./dist",
  markdown: {
    processor: satteri({
      mdastPlugins: [{
        name: "safe-markdown",
        before(tree) {
          assertSafeMarkdownTree(tree);
        }
      }]
    })
  }
});
