import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const stories = defineCollection({
  loader: glob({ pattern: "*.md", base: "./content/stories" }),
  schema: z.object({
    schemaVersion: z.literal(1),
    id: z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/)
  }).strict()
});

export const collections = { stories };
