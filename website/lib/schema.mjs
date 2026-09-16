import { z } from "zod";

export function contentError(code, recordId, field, message) {
  return Object.assign(new Error(message), { code, recordId, field });
}

export const StableId = z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/);
export const Version = z.literal(1);
const text = z.string().refine(value => value.trim().length > 0, "Must not be blank");
const strings = z.array(StableId);

export function isHttpsUrl(value) {
  if (typeof value !== "string" || !/^https:\/\//iu.test(value) || /[\s\\\u0000-\u001f<>]/u.test(value)) return false;
  try {
    const url = new URL(value);
    return url.protocol === "https:" && Boolean(url.hostname) && !url.username && !url.password;
  } catch {
    return false;
  }
}

export function isLocalUrl(value) {
  if (typeof value !== "string") return false;
  try {
    const decoded = decodeURIComponent(value);
    if (!decoded.startsWith("/") || decoded.startsWith("//") || /[\s\\\u0000-\u001f<>]/u.test(decoded)) return false;
    const pathname = decoded.split(/[?#]/u)[0];
    return !pathname.split("/").some(part => part === "." || part === "..");
  } catch {
    return false;
  }
}

export function isRelativePath(value) {
  return typeof value === "string" && value.length > 0 && !value.startsWith("/") &&
    !/[\\\u0000-\u001f:]/u.test(value) &&
    !value.split("/").some(part => part === "." || part === ".." || part === "");
}

const https = text.refine(isHttpsUrl, "Expected an HTTPS URL without credentials");
const localUrl = text.refine(isLocalUrl, "Expected a root-relative website destination");
const relativePath = text.refine(isRelativePath, "Expected a contained relative file path");
const base = { schemaVersion: Version, id: StableId };
const sourceRef = z.discriminatedUnion("kind", [
  z.strictObject({ kind: z.literal("inventory"), path: relativePath, anchor: text.regex(/^album-[A-Za-z0-9_-]+$/) }),
  z.strictObject({ kind: z.enum(["journal", "reference"]), path: relativePath })
]);
const albumKey = text.regex(/^[a-z][a-z_]*:[A-Za-z0-9_-]+$/);

export const schemas = {
  site: z.strictObject({
    ...base, id: z.literal("site"), name: text, descriptor: text, serviceLine: text,
    navigation: z.array(z.strictObject({ label: text, href: localUrl })),
    contact: z.strictObject({ label: text, href: https }).optional()
  }),
  home: z.strictObject({
    ...base, id: z.literal("home"), headline: text, intro: text,
    featuredProjectIds: strings, serviceIds: strings, heroMediaId: StableId.optional()
  }),
  service: z.strictObject({ ...base, title: text, description: text, projectIds: strings }),
  project: z.strictObject({
    ...base, title: text, area: text, summary: text, searchSummary: z.string(),
    tags: z.array(text).min(1), stage: text, recorded: text, sourceLabel: text,
    sourceRefs: z.array(sourceRef).min(1), albumKeys: z.array(albumKey),
    gallery: z.array(z.strictObject({
      mediaId: StableId, caption: text,
      role: z.enum(["context", "condition", "process", "detail", "result"]),
      focalPoint: z.tuple([z.number().min(0).max(100), z.number().min(0).max(100)]).optional(),
      alt: text.optional()
    })),
    searchMediaIds: strings, introduction: text.optional(), storyId: StableId.optional(),
    evidenceBoundary: text.optional()
  }),
  media: z.strictObject({
    ...base, kind: z.enum(["evidence", "illustration"]),
    assetPath: relativePath.refine(value => /\.(?:jpe?g|png|webp|avif)$/i.test(value), "Unsupported image type"),
    sourceUrl: https, albumKey, alt: text, width: z.number().int().positive(), height: z.number().int().positive()
  }),
  review: z.strictObject({
    ...base, id: z.literal("pilot"), state: z.enum(["candidate", "reviewed"]),
    records: z.array(z.strictObject({ key: text, sha256: z.string().regex(/^[a-f0-9]{64}$/) })),
    sources: z.array(z.strictObject({ key: text, sha256: z.string().regex(/^[a-f0-9]{64}$/) }))
  })
};

export function parseRecord(kind, record, label) {
  const result = schemas[kind].safeParse(record);
  if (result.success) return result.data;
  const issue = result.error.issues[0];
  const field = [label, ...issue.path].join(".");
  throw contentError("INVALID_CONTENT", record?.id ?? label, field, `${field}: ${issue.message}`);
}
