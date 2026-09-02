(function initializeTradeJournals() {
  "use strict";

  const evidenceManifest = window.tradeJournalEvidence ?? {
    archive: {},
    journals: []
  };
  const journalIndex = evidenceManifest.journals;
  const chatForm = document.querySelector("#chat-form");
  const chatInput = document.querySelector("#journal-query");
  const chatLog = document.querySelector("#chat-log");
  const promptButtons = document.querySelectorAll("[data-question]");

  function createMessage(role, label, body) {
    const message = document.createElement("div");
    message.className = `chat-message ${role}`;

    const labelElement = document.createElement("span");
    labelElement.textContent = label;

    const bodyElement = document.createElement("p");
    bodyElement.textContent = body;

    message.append(labelElement, bodyElement);
    return message;
  }

  function createAnswer(results, query) {
    const response = document.createElement("div");
    response.className = "chat-message assistant";

    const label = document.createElement("span");
    label.textContent = "Journal index";

    const intro = document.createElement("p");
    intro.textContent =
      results.length > 0
        ? `I found ${results.length} useful source match${results.length === 1 ? "" : "es"} for "${query}".`
        : `I did not find a tight match for "${query}" in the current index.`;

    response.append(label, intro);

    if (results.length === 0) {
      const fallback = document.createElement("p");
      fallback.textContent =
        "Try pottery, yunomi, Vespa electrical, studio lime finish, bath work, office floors, Kodak, or Isolette.";
      response.append(fallback);
      return response;
    }

    const list = document.createElement("div");
    list.className = "answer-list";

    results.forEach(({ entry }) => {
      const card = document.createElement("article");
      card.className = "answer-card";

      const heading = document.createElement("h4");
      heading.textContent = entry.title;

      const status = document.createElement("p");
      status.className = "answer-status";
      status.textContent = `${entry.evidence.stage} · ${entry.evidence.recorded}`;

      const summary = document.createElement("p");
      summary.textContent = entry.summary;

      const source = document.createElement("a");
      source.href = entry.url;
      source.textContent = `${entry.area} | Open exact evidence`;

      const sourcePath = document.createElement("small");
      sourcePath.className = "answer-source";
      sourcePath.textContent = entry.source;

      card.append(heading, status, summary, source, sourcePath);

      if (entry.images.length > 0) {
        const media = document.createElement("div");
        media.className = "answer-media";
        entry.images.forEach((imageSource) => {
          const image = document.createElement("img");
          image.src = imageSource.src;
          image.alt = imageSource.alt;
          image.loading = "lazy";
          image.decoding = "async";
          media.append(image);
        });
        card.append(media);
      }

      list.append(card);
    });

    response.append(list);
    return response;
  }

  function askJournals(query) {
    const trimmed = query.trim();
    if (!trimmed) return;

    const results = window.TradeJournalSearch.searchJournals(journalIndex, trimmed);
    chatLog.append(createMessage("user", "You", trimmed));
    chatLog.append(createAnswer(results, trimmed));
    chatLog.lastElementChild.scrollIntoView({ block: "nearest" });
  }

  function addLedgerItem(ledger, label, value) {
    const item = document.createElement("div");
    const term = document.createElement("dt");
    const description = document.createElement("dd");
    term.textContent = label;
    description.textContent = value;
    item.append(term, description);
    ledger.append(item);
  }

  function renderEvidenceLedgers() {
    journalIndex.forEach((entry) => {
      const target = document.getElementById(entry.target);
      const ledger = target?.querySelector("[data-evidence-ledger]");
      if (!ledger) return;

      ledger.replaceChildren();
      addLedgerItem(ledger, "Stage", entry.evidence.stage);
      addLedgerItem(ledger, "Recorded", entry.evidence.recorded);
      addLedgerItem(ledger, "Evidence", entry.evidence.sourceLabel);

      const boundary = target.querySelector("[data-evidence-boundary]");
      if (boundary && entry.evidence.boundary) {
        boundary.textContent = entry.evidence.boundary;
      }
    });
  }

  function renderManifestFacts() {
    document.querySelectorAll("[data-archive-count]").forEach((element) => {
      const key = element.dataset.archiveCount;
      const value = evidenceManifest.archive[key];
      if (Number.isInteger(value)) element.textContent = String(value).padStart(2, "0");
    });

    const albums = journalIndex.flatMap((entry) => entry.albums);
    const albumByKey = new Map(albums.map((album) => [album.key, album]));

    document.querySelectorAll("[data-album-count]").forEach((element) => {
      const album = albumByKey.get(element.dataset.albumCount);
      if (album) element.textContent = album.count;
    });

    document.querySelectorAll("[data-album-caption]").forEach((element) => {
      const album = albumByKey.get(element.dataset.albumCaption);
      if (!album) return;
      element.textContent = album.shown > 0
        ? `Representative evidence · ${album.shown} of ${album.count} photographs shown.`
        : `Source record · ${album.count} photographs reviewed; no representative image published here yet.`;
    });
  }

  renderManifestFacts();
  renderEvidenceLedgers();

  chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    askJournals(chatInput.value);
    chatInput.value = "";
  });

  promptButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const question = button.dataset.question;
      chatInput.value = question;
      askJournals(question);
      chatInput.value = "";
    });
  });
})();
