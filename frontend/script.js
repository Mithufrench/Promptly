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
            if (e.key === 'Enter') sendMessage();
        });
    }

    const heroPromptInput = document.getElementById('hero-prompt-input');
    if (heroPromptInput) {
        heroPromptInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendHeroPrompt();
        });
    }

    // Smooth scrolling for nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('href');
            if (target && target.startsWith('#')) {
                const sectionId = target.substring(1);
                smoothScroll(sectionId);
                updateActiveNav(link);
            }
        });
    });
}

// Update active navigation
function updateActiveNav(activeLink) {
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    activeLink.classList.add('active');
}

// Smooth scroll
function smoothScroll(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) element.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Load welcome message
function loadWelcomeMessage() {
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages && chatMessages.children.length <= 1) {
        addBotMessage("Hi! I'm your AI DevOps Assistant. Ask me to generate CI/CD pipelines, Terraform code, Kubernetes manifests, or any DevOps best practices.");
    }
}

// Copy code function (NEW)
function copyCode(elementId) {
    const codeElement = document.getElementById(elementId);
    if (!codeElement) return;

    const text = codeElement.textContent;
    navigator.clipboard.writeText(text).then(() => {
        const originalText = event.target.textContent;
        event.target.textContent = '✅ Copied!';
        setTimeout(() => {
            event.target.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Copy failed:', err);
        alert('Failed to copy code');
    });
}

// Send hero prompt
async function sendHeroPrompt() {
    const input = document.getElementById('hero-prompt-input');
    const prompt = input.value.trim();
    if (!prompt) {
        alert('Please describe your infrastructure or pipeline need');
        return;
    }

    const button = event.currentTarget || document.querySelector('.btn-prompt');
    const originalText = button.textContent;
    button.textContent = '⏳ Generating...';
    button.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: prompt })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        input.value = '';

        button.textContent = originalText;
        button.disabled = false;

        // Scroll to dashboard and show in chat
        smoothScroll('dashboard');
        setTimeout(() => {
            addUserMessage(prompt);
            addBotMessage(data.response || "Here's your generated configuration. Let me know if you need adjustments!");
            messageCount++;
            updateMetrics();
        }, 600);

    } catch (error) {
        console.error('Hero prompt error:', error);
        button.textContent = originalText;
        button.disabled = false;
        alert('❌ Error processing request. Please try again.');
    }
}

// Send chat message
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;

    addUserMessage(message);
    input.value = '';
    showTypingIndicator();

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: message })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        removeTypingIndicator();
        addBotMessage(data.response);
        messageCount++;
        updateMetrics();
    } catch (error) {
        removeTypingIndicator();
        addBotMessage('❌ Sorry, I couldn\'t reach the AI right now. Please try again.');
    }
}

// Message helpers
function addUserMessage(text) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `<div class="message-content">${escapeHtml(text)}</div>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addBotMessage(text) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `<div class="message-content">${escapeHtml(text)}</div>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;
    const indicator = document.createElement('div');
    indicator.className = 'message bot-message';
    indicator.id = 'typing-indicator';
    indicator.innerHTML = '<div class="message-content">🤖 Thinking...</div>';
    chatMessages.appendChild(indicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Health, Metrics, and other existing functions (kept & polished)
async function checkHealth() { /* your original function */ 
    // ... (keeping your full checkHealth function as-is)
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (!response.ok) throw new Error('Health check failed');
        const data = await response.json();
        
        const statusBadge = document.getElementById('status-badge');
        const healthBadge = document.getElementById('health-badge');
        const versionText = document.getElementById('version-text');

        if (statusBadge) statusBadge.textContent = '● Online';
        if (healthBadge) healthBadge.textContent = '● Healthy';
        if (versionText) versionText.textContent = data.version || '2.0.0';
        
        console.log('Health check passed:', data);
    } catch (error) {
        console.error('Health check error:', error);
    }
}

async function getMetrics() { /* your original function */ 
    // ... (keeping your full getMetrics function as-is)
    try {
        const response = await fetch(`${API_BASE}/metrics`);
        if (!response.ok) throw new Error('Metrics fetch failed');
        const data = await response.json();
        
        const requestsEl = document.getElementById('metric-requests');
        const errorsEl = document.getElementById('metric-errors');
        const statusEl = document.getElementById('metric-status');

        if (requestsEl) requestsEl.textContent = data.agent_requests_total || '0';
        if (errorsEl) errorsEl.textContent = data.agent_errors_total || '0';
        if (statusEl) statusEl.textContent = '🟢 Running';
    } catch (error) {
        console.error('Metrics error:', error);
    }
}

function updateMetrics() {
    const requests = document.getElementById('metric-requests');
    if (requests) {
        let current = parseInt(requests.textContent) || 0;
        requests.textContent = current + 1;
    }
}

// Keep your other functions (testEndpoint, openDocs, askAI, testAPI, scrollTo)
async function testEndpoint(endpoint) { /* your original */ }
function openDocs() { /* your original */ }
async function askAI(question) { /* your original */ }
async function testAPI() { /* your original */ }
function scrollTo(sectionId) { smoothScroll(sectionId); }

console.log('✅ Prompt-to-Prod script loaded successfully');
