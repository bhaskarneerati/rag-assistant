const API_BASE = "http://localhost:8000";

let allSessions = [];
let currentSessionId = null;
let currentSessionLogs = [];

function showView(viewName) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(v => v.classList.remove('active'));

    if (viewName === 'demo') {
        document.getElementById('demo-view').classList.add('active');
        document.getElementById('nav-demo').classList.add('active');
    } else if (viewName === 'logs') {
        document.getElementById('logs-view').classList.add('active');
        document.getElementById('nav-logs').classList.add('active');
        loadSessions();
    } else if (viewName === 'detail') {
        document.getElementById('detail-view').classList.add('active');
    }
}

async function loadSessions() {
    const tbody = document.getElementById('sessions-body');
    try {
        const response = await fetch(`${API_BASE}/logs/sessions`);
        allSessions = await response.json();
        renderSessions(allSessions);
    } catch (error) {
        console.error("Error loading sessions:", error);
        tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color:red;">Error loading sessions. Make sure backend is running.</td></tr>`;
    }
}

function renderSessions(sessions) {
    const tbody = document.getElementById('sessions-body');
    if (sessions.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;">No sessions found.</td></tr>`;
        return;
    }

    tbody.innerHTML = sessions.map(s => `
    <tr onclick="openSession('${s.session_id}')">
      <td style="font-family: monospace;">${s.session_id}</td>
      <td>${formatDate(s.start_time)}</td>
      <td>${formatDate(s.last_activity)}</td>
      <td><span class="badge">${s.event_count}</span></td>
    </tr>
  `).join('');
}

function filterSessions() {
    const query = document.getElementById('session-search').value.toLowerCase();
    const filtered = allSessions.filter(s => s.session_id.toLowerCase().includes(query));
    renderSessions(filtered);
}

async function openSession(sessionId) {
    currentSessionId = sessionId;
    showView('detail');
    document.getElementById('detail-session-id').innerText = `Session: ${sessionId}`;

    const chatMessages = document.getElementById('chat-messages');
    const debugEvents = document.getElementById('debug-events');

    chatMessages.innerHTML = "Loading...";
    debugEvents.innerHTML = "Loading...";

    try {
        const response = await fetch(`${API_BASE}/logs/sessions/${sessionId}`);
        const data = await response.json();
        currentSessionLogs = data.logs;

        renderChatHistory(currentSessionLogs);
        renderDebugLogs(currentSessionLogs); // Show all logs initially
    } catch (error) {
        console.error("Error loading session details:", error);
        chatMessages.innerHTML = "Error loading history.";
    }
}

function renderChatHistory(logs) {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = "";

    // 1. Initial Chat Setup Group
    const firstWaitIndex = logs.findIndex(l => l.event === 'bot_waiting_for_input');
    const initialLogsEnd = firstWaitIndex !== -1 ? firstWaitIndex + 1 : logs.length;

    const initialBlock = document.createElement('div');
    initialBlock.className = 'chat-group';
    initialBlock.innerHTML = `
    <div class="chat-group-header">
        <span>Chat Initiated</span>
        <div class="bug-icon-mini" onclick="filterLogs(0, ${initialLogsEnd})" title="Debug Setup">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><path d="M11 8c-1 0-2 .5-2 1.5v2c0 1 1 1.5 2 1.5s2-.5 2-1.5v-2c0-1-1-1.5-2-1.5z"></path></svg>
        </div>
    </div>
  `;
    chatMessages.appendChild(initialBlock);

    // 2. Interaction Groups
    let currentGroupStart = 0;
    logs.forEach((log, index) => {
        if (log.event === 'user_question_received') {
            const groupStart = index;
            // Find next waiting point
            const nextWait = logs.slice(index).findIndex(l => l.event === 'bot_waiting_for_input');
            const groupEnd = nextWait !== -1 ? index + nextWait + 1 : logs.length;

            const userMsg = document.createElement('div');
            userMsg.className = 'msg-wrapper user-wrapper';
            userMsg.innerHTML = `
            <div class="msg user">${log.question}</div>
            <div class="bug-icon-mini side" onclick="filterLogs(${groupStart}, ${groupEnd})" title="Debug this message">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><path d="M11 8c-1 0-2 .5-2 1.5v2c0 1 1 1.5 2 1.5s2-.5 2-1.5v-2c0-1-1-1.5-2-1.5z"></path></svg>
            </div>
        `;
            chatMessages.appendChild(userMsg);
        } else if (log.event === 'answer_generated') {
            const assistantMsg = document.createElement('div');
            assistantMsg.className = 'msg-wrapper assistant-wrapper';
            assistantMsg.innerHTML = `
            <div class="msg assistant">${formatMarkdown(log.full_answer || log.answer_preview || "No answer text")}</div>
        `;
            chatMessages.appendChild(assistantMsg);
        }
    });

    if (chatMessages.innerHTML === "") {
        chatMessages.innerHTML = `<div style="text-align:center; color:gray; margin-top: 2rem;">No logs found for this session.</div>`;
    }
}

function filterLogs(start, end) {
    const filtered = currentSessionLogs.slice(start, end);
    renderDebugLogs(filtered);
    // Open the logs pane if it's hidden
    document.getElementById('debug-logs-pane').classList.remove('hidden');
}

function renderDebugLogs(logs) {
    const debugEvents = document.getElementById('debug-events');
    debugEvents.innerHTML = "";

    logs.forEach(log => {
        const tile = document.createElement('div');
        tile.className = 'event-tile';

        // Extract metadata
        const { timestamp, component, event, session_id, ...data } = log;

        tile.innerHTML = `
      <div class="event-header">
        <span class="event-name">${event} <span class="comp-tag">[${component}]</span></span>
        <span class="event-time">${formatTimeOnly(timestamp)}</span>
      </div>
      <div class="event-data">${JSON.stringify(data, null, 2)}</div>
    `;
        debugEvents.appendChild(tile);
    });

    if (logs.length === 0) {
        debugEvents.innerHTML = `<div style="text-align:center; color:gray; margin-top: 2rem;">No log events in this interaction.</div>`;
    }
}

function toggleDebugLogs() {
    const pane = document.getElementById('debug-logs-pane');
    pane.classList.toggle('hidden');
}

function formatDate(isoStr) {
    if (!isoStr) return "-";
    const date = new Date(isoStr);
    return date.toLocaleString();
}

function formatTimeOnly(isoStr) {
    if (!isoStr) return "-";
    const date = new Date(isoStr);
    return date.toLocaleTimeString();
}

function formatMarkdown(text) {
    if (!text) return "";
    // Simple markdown-ish formatter
    return text
        .replace(/\n/g, "<br/>")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/•\s+(.*?)(?=<br\/>|$)/g, "<li>$1</li>")
        .replace(/(<li>.*?<\/li>)+/g, "<ul>$&</ul>");
}

// Initial load
showView('demo');
