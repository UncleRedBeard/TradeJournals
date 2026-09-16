import { spawn } from "node:child_process";
import { cp, mkdir, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { prepareSite } from "../lib/prepare.mjs";

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

export async function buildWebsite({ mode, repoRoot = defaultRepoRoot, websiteRoot = defaultWebsiteRoot } = {}) {
  if (!["preview", "release"].includes(mode)) throw new Error("Build mode must be preview or release.");

  const generatedRoot = path.join(websiteRoot, ".generated");
  const publicRoot = path.join(generatedRoot, "public");
  await rm(generatedRoot, { recursive: true, force: true });
  await mkdir(publicRoot, { recursive: true });

  const prepared = await prepareSite({ repoRoot, contentRoot: path.join(websiteRoot, "content"), mode });
  await writeJson(path.join(websiteRoot, "src", "generated", "site.json"), prepared.model);
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
      WK_PUBLIC_DIR: publicRoot
    },
    stdio: "inherit"
  });
  return prepared;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  buildWebsite({ mode: process.argv[2] }).catch(error => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
