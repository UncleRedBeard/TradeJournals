import { defineConfig } from "astro/config";
import { satteri } from "@astrojs/markdown-satteri";
import path from "node:path";
import { assertSafeMarkdownTree } from "./lib/markdown-policy.mjs";

const mode = process.env.WK_SITE_MODE;
const siteModel = process.env.WK_SITE_MODEL;
const publicDir = process.env.WK_PUBLIC_DIR;
const outDir = process.env.WK_OUT_DIR;

if (![siteModel, publicDir, outDir].every(value => value && path.isAbsolute(value)) || !["preview", "release"].includes(mode)) {
  throw new Error("Use website/scripts/build.mjs so Astro receives validated prepared content.");
}

export default defineConfig({
  output: "static",
  // Keep the small pilot's styles with its HTML and its output contract stable.
  build: { inlineStylesheets: "always" },
  publicDir,
  outDir,
  vite: { resolve: { alias: { "@site-model": siteModel } } },
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
