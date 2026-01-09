/**
 * Drop-in embed script (LOCAL SAFE)
 *
 * Usage:
 * <script src="../widget/embed.js"></script>
 */

(function () {
  if (document.getElementById("rag-widget-button")) return;

  const root = document.createElement("div");

  root.innerHTML = `
    <link rel="stylesheet" href="../widget/widget.css" />

    <button id="rag-widget-button" aria-label="Open chat">
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="width: 28px; height: 28px; fill: white;">
        <path d="M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2ZM20 16H5.17L4 17.17V4H20V16Z"/>
      </svg>
    </button>

    <div id="rag-widget-container" class="hidden">
      <div class="rag-header">
        <div class="rag-header-title">
          <span>RAG Assistant</span>
        </div>
        <button id="rag-close-btn" aria-label="Close chat">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <div id="rag-messages"></div>

      <div class="rag-input-container">
        <input
          id="rag-input"
          type="text"
          placeholder="Type your message..."
          autocomplete="off"
        />
        <button id="rag-send-btn" aria-label="Send message">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="width: 20px; height: 20px; fill: white;">
            <path d="M2.01 21L23 12L2.01 3L2 10L17 12L2 14L2.01 21Z"/>
          </svg>
        </button>
      </div>
    </div>
  `;


  document.body.appendChild(root);

  const script = document.createElement("script");
  script.src = "../widget/widget.js";
  document.body.appendChild(script);
})();