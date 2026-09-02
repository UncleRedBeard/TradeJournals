(function exposeJournalSearch(root, factory) {
  const api = factory();

  if (typeof module === "object" && module.exports) {
    module.exports = api;
    return;
  }

  root.TradeJournalSearch = api;
})(typeof window !== "undefined" ? window : this, function createJournalSearch() {
  "use strict";

  const stopWords = new Set([
    "about",
    "albums",
    "and",
    "are",
    "can",
    "completion",
    "covers",
    "document",
    "documents",
    "does",
    "evidence",
    "for",
    "from",
    "images",
    "journal",
    "journals",
    "path",
    "show",
    "source",
    "status",
    "strongest",
    "the",
    "what",
    "which",
    "with",
    "work"
  ]);

  function normalize(value) {
    return String(value)
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function normalizeWord(value) {
    return value.length > 4 && value.endsWith("s") ? value.slice(0, -1) : value;
  }

  function tokenize(value) {
    return normalize(value)
      .split(" ")
      .filter((token) => token.length > 2 && !stopWords.has(token));
  }

  function containsToken(value, token) {
    const normalizedToken = normalizeWord(token);
    return normalize(value)
      .split(" ")
      .some((word) => normalizeWord(word) === normalizedToken);
  }

  function scoreEntry(entry, tokens, normalizedQuery) {
    const title = normalize(entry.title);
    const tags = entry.tags.map(normalize);
    const summary = normalize(entry.summary);
    const context = normalize(`${entry.area} ${entry.source}`);
    let score = 0;
    let matchedTokens = 0;

    tokens.forEach((token) => {
      let tokenScore = 0;
      if (containsToken(title, token)) tokenScore = 8;
      else if (tags.some((tag) => containsToken(tag, token))) tokenScore = 6;
      else if (containsToken(summary, token)) tokenScore = 3;
      else if (containsToken(context, token)) tokenScore = 1;

      if (tokenScore > 0) {
        score += tokenScore;
        matchedTokens += 1;
      }
    });

    const searchableText = normalize(
      `${entry.title} ${entry.tags.join(" ")} ${entry.summary}`
    );
    if (normalizedQuery && searchableText.includes(normalizedQuery)) {
      score += 10;
    }

    return {
      score,
      coverage: tokens.length === 0 ? 1 : matchedTokens / tokens.length
    };
  }

  function searchJournals(entries, query, limit = 3) {
    const tokens = tokenize(query);
    if (tokens.length === 0) {
      return entries.slice(0, limit).map((entry) => ({
        entry,
        score: 1,
        coverage: 1
      }));
    }

    const normalizedQuery = tokens.join(" ");
    const minimumCoverage = tokens.length > 1 ? 0.66 : 1;
    const results = entries
      .map((entry) => ({
        entry,
        ...scoreEntry(entry, tokens, normalizedQuery)
      }))
      .filter((result) => result.score > 0 && result.coverage >= minimumCoverage)
      .sort((left, right) =>
        right.score - left.score ||
        right.coverage - left.coverage ||
        left.entry.title.localeCompare(right.entry.title)
      );
    const topScore = results[0]?.score ?? 0;

    return results
      .filter((result) => result.score >= topScore * 0.45)
      .slice(0, limit);
  }

  return Object.freeze({ normalize, tokenize, searchJournals });
});
