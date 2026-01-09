// ==============================
// Configuration
// ==============================
const API_ENDPOINT = "http://localhost:8000/chat/";

// ==============================
// State
// ==============================
let sessionId = localStorage.getItem("rag_session_id");
let isNewSession = true;
let isOpen = false;

// ==============================
// DOM Ready Guard
// ==============================
function ready(fn) {
  if (document.readyState !== "loading") fn();
  else document.addEventListener("DOMContentLoaded", fn);
}

ready(() => {
  const widgetButton = document.getElementById("rag-widget-button");
  const widgetContainer = document.getElementById("rag-widget-container");
  const closeBtn = document.getElementById("rag-close-btn");
  const sendBtn = document.getElementById("rag-send-btn");
  const inputField = document.getElementById("rag-input");
  const messagesDiv = document.getElementById("rag-messages");

  if (!widgetButton || !widgetContainer) return;

  // ==============================
  // Toggle Widget (OPEN / CLOSE)
  // ==============================
  const toggleWidget = (forceState) => {
    isOpen = forceState !== undefined ? forceState : !isOpen;
    widgetContainer.classList.toggle("hidden", !isOpen);
  };

  widgetButton.onclick = () => toggleWidget();
  if (closeBtn) closeBtn.onclick = () => toggleWidget(false);

  // ==============================
  // Messaging
  // ==============================
  sendBtn.onclick = sendMessage;

  inputField.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  function addMessage(role, html) {
    const msg = document.createElement("div");
    msg.className = `rag-message ${role}`;
    msg.innerHTML = html;
    messagesDiv.appendChild(msg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    return msg;
  }

  function addTypingIndicator() {
    const indicator = document.createElement("div");
    indicator.className = "rag-message assistant typing";
    indicator.innerHTML = "<span>.</span><span>.</span><span>.</span>";
    indicator.style.display = "flex";
    indicator.style.gap = "4px";
    messagesDiv.appendChild(indicator);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    return indicator;
  }

  function formatResponse(text) {
    if (!text) return "";
    return text
      .replace(/^### (.*$)/gim, "<h4>$1</h4>")
      .replace(/^## (.*$)/gim, "<h3>$1</h3>")
      .replace(/^# (.*$)/gim, "<h2>$1</h2>")
      .replace(/^\* (.*$)/gim, "<li>$1</li>")
      .replace(/(<li>.*<\/li>)/gims, "<ul>$1</ul>")
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/`(.*?)`/g, "<code>$1</code>")
      .replace(/\n/g, "<br/>");
  }

  function sendMessage() {
    const question = inputField.value.trim();
    if (!question) return;

    addMessage("user", question);
    inputField.value = "";

    const typing = addTypingIndicator();

    fetch(API_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Session-Id": sessionId || "",
        "X-New-Session": isNewSession,
      },
      body: JSON.stringify({ question }),
    })
      .then((res) => res.json())
      .then((data) => {
        typing.remove();
        sessionId = data.session_id;
        localStorage.setItem("rag_session_id", sessionId);
        isNewSession = false;

        addMessage("assistant", formatResponse(data.answer));
      })
      .catch(() => {
        typing.remove();
        addMessage("assistant", "⚠️ Unable to contact assistant.");
      });
  }
});