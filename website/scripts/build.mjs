import { spawn } from "node:child_process";
import { cp, mkdir, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { prepareSite } from "../lib/prepare.mjs";
import { checkOutput } from "./check-output.mjs";

const scriptRoot = path.dirname(fileURLToPath(import.meta.url));
const defaultWebsiteRoot = path.resolve(scriptRoot, "..");
const defaultRepoRoot = path.resolve(defaultWebsiteRoot, "..");

function run(command, args, options) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, options);
    child.once("error", reject);
    child.once("exit", code => code === 0 ? resolve() : reject(new Error(`${path.basename(command)} exited with ${code}`)));
  });
}

async function writeJson(file, value) {
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, `${JSON.stringify(value, null, 2)}\n`);
}

export async function buildWebsite({
  mode,
  repoRoot = defaultRepoRoot,
  websiteRoot = defaultWebsiteRoot,
  contentRoot = path.join(websiteRoot, "content"),
  contentBoundaryRoot = repoRoot,
  generatedRoot = path.join(websiteRoot, ".generated"),
  modelPath = path.join(websiteRoot, "src", "generated", "site.json"),
  publicRoot = path.join(generatedRoot, "public"),
  outputRoot = path.join(websiteRoot, mode === "preview" ? ".preview-dist" : "dist"),
  assetOverrides = new Map()
} = {}) {
  if (!["preview", "release"].includes(mode)) throw new Error("Build mode must be preview or release.");

  await rm(generatedRoot, { recursive: true, force: true });
  await rm(publicRoot, { recursive: true, force: true });
  await mkdir(publicRoot, { recursive: true });

  const prepared = await prepareSite({ repoRoot, contentRoot, contentBoundaryRoot, mode, assetOverrides });
  await writeJson(modelPath, prepared.model);
  await writeJson(path.join(generatedRoot, "review.json"), prepared.report);

  for (const asset of prepared.assetCopies) {
    await cp(asset.sourceAbsolute, path.join(publicRoot, asset.publicRelative));
  }
  await mkdir(path.join(publicRoot, "scripts"), { recursive: true });
  await cp(path.join(repoRoot, "site_example", "journal-search.js"), path.join(publicRoot, "scripts", "journal-search.js"));
  await cp(path.join(websiteRoot, "src", "scripts", "archive-search.js"), path.join(publicRoot, "scripts", "archive-search.js"));

  const astroCli = path.join(websiteRoot, "node_modules", "astro", "bin", "astro.mjs");
  await run(process.execPath, [astroCli, "build"], {
    cwd: websiteRoot,
    env: {
      ...process.env,
      ASTRO_TELEMETRY_DISABLED: "1",
      WK_SITE_MODE: mode,
      WK_SITE_MODEL: modelPath,
      WK_STORY_ROOT: path.join(contentRoot, "stories"),
      WK_PUBLIC_DIR: publicRoot,
      WK_OUT_DIR: outputRoot
    },
    stdio: "inherit"
  });
  const output = await checkOutput({
    outputRoot,
    model: prepared.model
  });
  console.log(`Public output verified: ${output.pages} pages, ${output.files} files, ${output.references} references.`);
  return { ...prepared, output, outputRoot };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  buildWebsite({ mode: process.argv[2] }).catch(error => {
    console.error(`${error.code ?? "BUILD_ERROR"}: ${error.message}`);
    process.exitCode = 1;
  });
}
