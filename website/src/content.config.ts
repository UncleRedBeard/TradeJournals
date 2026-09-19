import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const storyRoot = process.env.WK_STORY_ROOT;
if (!storyRoot) throw new Error("Use website/scripts/build.mjs so Astro receives the prepared story root.");

const stories = defineCollection({
  loader: glob({ pattern: "*.md", base: storyRoot }),
  schema: z.object({
    schemaVersion: z.literal(1),
    id: z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/)
  }).strict()
});

export const collections = { stories };
