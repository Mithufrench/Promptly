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
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    activeLink.classList.add('active');
}

// Smooth scroll to section
function smoothScroll(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
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

    if (!message) {
        alert('Please enter a question');
        return;
    }

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

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        removeTypingIndicator();
        addBotMessage(data.response);
        messageCount++;
        updateMetrics();
    } catch (error) {
        removeTypingIndicator();
        console.error('Chat error:', error);
        addBotMessage('❌ Error: Could not reach the server. Please try again.');
    }
}

// Add message to chat
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

// Typing indicator
function showTypingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;
    
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
        if (!response.ok) throw new Error('Health check failed');
        
        const data = await response.json();

        const statusBadge = document.getElementById('status-badge');
        const healthBadge = document.getElementById('health-badge');
        const versionText = document.getElementById('version-text');

        if (statusBadge) {
            statusBadge.textContent = '● Online';
            statusBadge.className = 'badge badge-online';
        }
        if (healthBadge) {
            healthBadge.textContent = '● Healthy';
            healthBadge.className = 'badge badge-healthy';
        }
        if (versionText) {
            versionText.textContent = data.version || '2.0.0';
        }

        alert('✅ Health Check Passed!\n\n' + JSON.stringify(data, null, 2));
        return true;
    } catch (error) {
        console.error('Health check error:', error);
        const statusBadge = document.getElementById('status-badge');
        if (statusBadge) {
            statusBadge.textContent = '● Offline';
            statusBadge.className = 'badge';
        }
        alert('❌ API Health Check Failed\n\n' + error.message);
        return false;
    }
}

// Get metrics
async function getMetrics() {
    try {
        const response = await fetch(`${API_BASE}/metrics`);
        if (!response.ok) throw new Error('Metrics fetch failed');
        
        const data = await response.json();

        const requestsEl = document.getElementById('metric-requests');
        const errorsEl = document.getElementById('metric-errors');
        const statusEl = document.getElementById('metric-status');

        if (requestsEl) requestsEl.textContent = data.agent_requests_total || '0';
        if (errorsEl) errorsEl.textContent = data.agent_errors_total || '0';
        if (statusEl) statusEl.textContent = data.agent_status === 'running' ? '🟢 Running' : '🔴 Down';

        console.log('Metrics updated:', data);
    } catch (error) {
        console.error('Metrics error:', error);
        alert('❌ Failed to fetch metrics\n\n' + error.message);
    }
}

// Update metrics after chat
function updateMetrics() {
    const requests = document.getElementById('metric-requests');
    if (requests) {
        const current = parseInt(requests.textContent) || 0;
        requests.textContent = current + 1;
    }
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

        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        alert(`✅ Success!\n\nEndpoint: ${endpoint}\n\n${JSON.stringify(data, null, 2)}`);
    } catch (error) {
        console.error('Endpoint test error:', error);
        alert(`❌ Error Testing ${endpoint}\n\n${error.message}`);
    }
}

// Open docs
function openDocs() {
    const docsUrl = `${API_BASE}/docs`;
    window.open(docsUrl, '_blank');
    console.log('Opening docs:', docsUrl);
}

// Ask AI predefined question
async function askAI(question) {
    const input = document.getElementById('chat-input');
    if (input) {
        input.value = question;
        input.focus();
        setTimeout(() => sendMessage(), 100);
    }
}

// Test API
async function testAPI() {
    try {
        const isHealthy = await checkHealth();
        if (isHealthy) {
            await getMetrics();
        }
    } catch (error) {
        console.error('API test error:', error);
        alert('❌ API Test Failed\n\n' + error.message);
    }
}

// Console logging for debugging
console.log('Script loaded');
console.log('API Base:', API_BASE);
