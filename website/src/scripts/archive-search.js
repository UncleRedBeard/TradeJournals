(() => {
  const form = document.querySelector("[data-archive-search]");
  if (!form) return;
  const input = form.querySelector("input");
  const status = document.querySelector("[data-search-status]");
  const results = document.querySelector("[data-search-results]");
  const fallback = document.querySelector("[data-archive-list]");
  let entries;

  const showEntries = matches => {
    results.replaceChildren();
    for (const { entry } of matches) {
      const article = document.createElement("article");
      const heading = document.createElement("h3");
      const link = document.createElement("a");
      const summary = document.createElement("p");
      link.href = entry.url;
      link.textContent = entry.title;
      summary.textContent = entry.summary;
      heading.append(link);
      article.append(heading, summary);
      results.append(article);
    }
    results.hidden = false;
    fallback.hidden = true;
  };

  form.addEventListener("submit", async event => {
    event.preventDefault();
    try {
      entries ??= await fetch("/search.json", { headers: { Accept: "application/json" } }).then(response => {
        if (!response.ok) throw new Error("search data unavailable");
        return response.json();
      });
      const matches = window.TradeJournalSearch.searchJournals(entries, input.value);
      showEntries(matches);
      status.textContent = matches.length ? `${matches.length} result${matches.length === 1 ? "" : "s"}.` : "No matching selected projects.";
    } catch {
      status.textContent = "Search is unavailable. The project list remains below.";
      results.hidden = true;
      fallback.hidden = false;
    }
  });
})();
