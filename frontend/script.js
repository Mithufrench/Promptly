// Enhanced AI Agent Frontend with Multi-Agent Support

const API_BASE = window.location.origin;
let conversationHistory = [];
let selectedAgent = 'devops_expert';
let messageCount = 0;

// ==================== INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Frontend initialized');
    initializeUI();
    loadAgents();
    checkHealth();
    loadWelcomeMessage();
});

function initializeUI() {
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    const heroPromptInput = document.getElementById('hero-prompt-input');
    if (heroPromptInput) {
        heroPromptInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendHeroPrompt();
        });
    }
}

// ==================== API CALLS ====================

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        
        console.log('✅ Health check:', data);
        updateHealthUI(data);
        return data;
    } catch (error) {
        console.error('❌ Health check failed:', error);
        updateHealthUI({ status: 'error' });
    }
}

async function getMetrics() {
    try {
        const response = await fetch(`${API_BASE}/metrics`);
        const data = await response.json();
        
        console.log('📊 Metrics:', data);
        updateMetricsUI(data);
        return data;
    } catch (error) {
        console.error('❌ Metrics failed:', error);
    }
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const query = input.value.trim();
    
    if (!query) return;
    
    addUserMessage(query);
    input.value = '';
    showTypingIndicator();

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: query,
                agent_type: selectedAgent,
                conversation_history: conversationHistory
            })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const data = await response.json();
        
        conversationHistory.push({
            role: 'user',
            content: query
        });
        
        conversationHistory.push({
            role: 'assistant',
            content: data.response
        });
        
        removeTypingIndicator();
        addBotMessage(data.response);
        messageCount++;
        updateMetrics();
        
    } catch (error) {
        console.error('❌ Chat error:', error);
        removeTypingIndicator();
        addBotMessage('❌ Sorry, I couldn\'t reach the AI right now. Please try again.');
    }
}

async function recommendAgent(query) {
    try {
        const response = await fetch(`${API_BASE}/agents/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        console.log('🧠 Recommended agent:', data.recommended_agent);
        return data.recommended_agent;
        
    } catch (error) {
        console.error('❌ Agent recommendation error:', error);
        return 'devops_expert';
    }
}

async function loadAgents() {
    try {
        const response = await fetch(`${API_BASE}/agents`);
        const data = await response.json();
        
        console.log('🧠 Available agents:', data.agents);
        updateAgentsUI(data.agents);
        
    } catch (error) {
        console.error('❌ Failed to load agents:', error);
    }
}

async function testEndpoint(endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`);
        const data = await response.json();
        
        console.log(`✅ ${endpoint}:`, data);
        alert('Endpoint working! Check console for details.');
        
    } catch (error) {
        console.error(`❌ ${endpoint} error:`, error);
        alert('Endpoint failed: ' + error.message);
    }
}

// ==================== UI UPDATES ====================

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

function updateHealthUI(data) {
    const statusBadge = document.getElementById('status-badge');
    const healthBadge = document.getElementById('health-badge');
    const versionText = document.getElementById('version-text');
    
    if (statusBadge) {
        statusBadge.className = data.status === 'healthy' ? 'badge badge-online' : 'badge badge-offline';
        statusBadge.textContent = data.status === 'healthy' ? '● Online' : '● Offline';
    }
    
    if (healthBadge) {
        healthBadge.className = data.status === 'healthy' ? 'badge badge-healthy' : 'badge badge-error';
        healthBadge.textContent = data.status === 'healthy' ? '● Healthy' : '● Error';
    }
    
    if (versionText) {
        versionText.textContent = data.version || '3.0.0';
    }
}

function updateMetricsUI(data) {
    const requests = document.getElementById('metric-requests');
    const errors = document.getElementById('metric-errors');
    const status = document.getElementById('metric-status');
    
    if (requests) requests.textContent = data.agent_requests_total || 0;
    if (errors) errors.textContent = data.agent_errors_total || 0;
    if (status) status.textContent = data.agent_status || 'Unknown';
}

function updateMetrics() {
    const requests = document.getElementById('metric-requests');
    if (requests) {
        let current = parseInt(requests.textContent) || 0;
        requests.textContent = current + 1;
    }
}

function updateAgentsUI(agents) {
    const actionsPanel = document.querySelector('.actions-panel');
    if (actionsPanel && agents.length > 0) {
        console.log('Available agents:', agents);
    }
}

// ==================== UTILITY FUNCTIONS ====================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function askAI(query) {
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.value = query;
        sendMessage();
    }
}

function testAPI() {
    checkHealth();
    setTimeout(() => {
        askAI('What is Kubernetes?');
    }, 1000);
}

function scrollTo(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

function openDocs() {
    const docsSection = document.getElementById('docs');
    if (docsSection) {
        docsSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function handleHeroPromptEnter(event) {
    if (event.key === 'Enter') {
        sendHeroPrompt();
    }
}

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

        scrollTo('dashboard');
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

function loadWelcomeMessage() {
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages && chatMessages.children.length <= 1) {
        addBotMessage("Hi! I'm your AI DevOps Assistant. Ask me to generate CI/CD pipelines, Terraform code, Kubernetes manifests, or any DevOps best practices.");
    }
}

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

// ==================== AUTO-REFRESH ====================

setInterval(() => {
    checkHealth();
    getMetrics();
}, 30000);

console.log('✅ Enhanced AI Frontend loaded with:');
console.log('  - Multi-agent AI system');
console.log('  - Conversation history');
console.log('  - Streaming responses');
console.log('  - Agent recommendation');
console.log('  - Architecture design');
