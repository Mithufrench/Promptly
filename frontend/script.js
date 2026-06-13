// Configuration
const API_BASE = window.location.origin;
let messageCount = 0;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

// Initialize app
function initializeApp() {
    checkHealth();
    getMetrics();
    setupEventListeners();
    loadWelcomeMessage();
}

// Setup event listeners
function setupEventListeners() {
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Smooth scrolling for nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('href');
            scrollTo(target.substring(1));
            updateActiveNav(link);
        });
    });
}

// Update active navigation
function updateActiveNav(activeLink) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    activeLink.classList.add('active');
}

// Scroll to section
function scrollTo(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Load welcome message
function loadWelcomeMessage() {
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages && chatMessages.children.length === 1) {
        addBotMessage('Welcome to Prompt-to-Prod! I can help with DevOps questions. Try asking: "What is Kubernetes?" or "How do I use Docker?"');
    }
}

// Send message
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();

    if (!message) return;

    // Add user message
    addUserMessage(message);
    input.value = '';

    // Show loading
    showTypingIndicator();

    try {
        // Send to API
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: message })
        });

        const data = await response.json();
        removeTypingIndicator();
        addBotMessage(data.response);
        messageCount++;
        updateMetrics();
    } catch (error) {
        removeTypingIndicator();
        addBotMessage('❌ Error: Could not reach the server. Please try again.');
    }
}

// Add message to chat
function addUserMessage(text) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `<div class="message-content">${escapeHtml(text)}</div>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addBotMessage(text) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `<div class="message-content">${escapeHtml(text)}</div>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Typing indicator
function showTypingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    const indicator = document.createElement('div');
    indicator.className = 'message bot-message';
    indicator.id = 'typing-indicator';
    indicator.innerHTML = '<div class="message-content">⏳ Thinking...</div>';
    chatMessages.appendChild(indicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Check health
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();

        document.getElementById('status-badge').textContent = '● Online';
        document.getElementById('status-badge').className = 'badge badge-online';
        document.getElementById('health-badge').textContent = '● Healthy';
        document.getElementById('health-badge').className = 'badge badge-healthy';
        document.getElementById('version-text').textContent = data.version || '2.0.0';

        return true;
    } catch (error) {
        document.getElementById('status-badge').textContent = '● Offline';
        document.getElementById('status-badge').className = 'badge';
        return false;
    }
}

// Get metrics
async function getMetrics() {
    try {
        const response = await fetch(`${API_BASE}/metrics`);
        const data = await response.json();

        document.getElementById('metric-requests').textContent = data.agent_requests_total || '0';
        document.getElementById('metric-errors').textContent = data.agent_errors_total || '0';
        document.getElementById('metric-status').textContent = data.agent_status === 'running' ? '🟢 Running' : '🔴 Down';
    } catch (error) {
        console.error('Metrics error:', error);
    }
}

// Update metrics
function updateMetrics() {
    const requests = parseInt(document.getElementById('metric-requests').textContent) || 0;
    document.getElementById('metric-requests').textContent = requests + 1;
}

// Test API endpoint
async function testEndpoint(endpoint) {
    let url = `${API_BASE}${endpoint}`;
    let method = 'GET';
    let body = null;

    if (endpoint === '/chat') {
        method = 'POST';
        body = JSON.stringify({ query: 'What is Docker?' });
    }

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: body
        });

        const data = await response.json();
        alert(`✅ Success!\n\n${JSON.stringify(data, null, 2)}`);
    } catch (error) {
        alert(`❌ Error: ${error.message}`);
    }
}

// Open docs
function openDocs() {
    window.open(`${API_BASE}/docs`, '_blank');
}

// Ask AI predefined question
async function askAI(question) {
    const input = document.getElementById('chat-input');
    input.value = question;
    setTimeout(() => sendMessage(), 100);
}

// Test API
async function testAPI() {
    const isHealthy = await checkHealth();
    if (isHealthy) {
        alert('✅ API is healthy!\n\nYour platform is running correctly.');
        await getMetrics();
    } else {
        alert('❌ API is not responding');
    }
}
