// Tilly AI - Frontend Application

class TillyApp {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.messages = [];
        this.isTyping = false;
        
        this.initElements();
        this.initEventListeners();
        this.checkHealth();
    }

    initElements() {
        this.messagesContainer = document.getElementById('messagesContainer');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.newChatBtn = document.getElementById('newChatBtn');
        this.welcomeScreen = document.getElementById('welcomeScreen');
        this.statusIndicator = document.getElementById('statusIndicator');
    }

    initEventListeners() {
        // Send button click
        this.sendBtn.addEventListener('click', () => this.sendMessage());

        // Enter key to send (Shift+Enter for new line)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Enable/disable send button based on input
        this.messageInput.addEventListener('input', () => {
            this.autoResizeTextarea();
            this.sendBtn.disabled = !this.messageInput.value.trim();
        });

        // New chat button
        this.newChatBtn.addEventListener('click', () => this.startNewChat());

        // Suggestion cards
        document.querySelectorAll('.suggestion-card').forEach(card => {
            card.addEventListener('click', () => {
                const suggestion = card.dataset.suggestion;
                this.messageInput.value = suggestion;
                this.sendBtn.disabled = false;
                this.sendMessage();
            });
        });
    }

    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    async checkHealth() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            
            if (data.status === 'healthy') {
                this.updateStatus('online', 'Online');
            } else {
                this.updateStatus('warning', 'Limited');
            }
        } catch (error) {
            console.error('Health check failed:', error);
            this.updateStatus('offline', 'Offline');
        }
    }

    updateStatus(status, text) {
        const statusDot = this.statusIndicator.querySelector('.status-dot');
        const statusText = this.statusIndicator.querySelector('.status-text');
        
        statusDot.className = 'status-dot';
        statusDot.classList.add(status);
        statusText.textContent = text;
    }

    async sendMessage() {
        const messageText = this.messageInput.value.trim();
        if (!messageText || this.isTyping) return;

        // Hide welcome screen
        if (this.welcomeScreen) {
            this.welcomeScreen.style.display = 'none';
        }

        // Add user message to UI
        this.addMessage('user', messageText);
        
        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        this.sendBtn.disabled = true;

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Send message to API
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: messageText,
                    session_id: this.sessionId
                })
            });

            if (!response.ok) {
                throw new Error('Failed to get response');
            }

            const data = await response.json();

            // Remove typing indicator
            this.removeTypingIndicator();

            // Add Tilly's response
            this.addMessage('tilly', data.response, {
                intent: data.intent,
                mood: data.mood,
                model: data.model_used
            });

        } catch (error) {
            console.error('Error sending message:', error);
            this.removeTypingIndicator();
            this.addMessage('tilly', "I'm sorry, I'm having trouble connecting right now. Please try again in a moment.");
        }

        // Focus back on input
        this.messageInput.focus();
    }

    addMessage(sender, text, metadata = {}) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        
        if (sender === 'tilly') {
            const avatarImg = document.createElement('img');
            avatarImg.src = '/static/images/avatar.svg';
            avatarImg.alt = 'Tilly';
            avatarImg.onerror = () => {
                // Fallback to emoji if image not found
                avatar.textContent = '🤖';
            };
            avatar.appendChild(avatarImg);
        } else {
            avatar.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
            </svg>`;
        }

        const content = document.createElement('div');
        content.className = 'message-content';

        const header = document.createElement('div');
        header.className = 'message-header';
        header.innerHTML = `
            <span>${sender === 'tilly' ? 'Tilly' : 'You'}</span>
            <span class="message-time">${this.formatTime(new Date())}</span>
        `;

        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = text;

        content.appendChild(header);
        content.appendChild(messageText);

        // Add metadata if available (only for Tilly's messages)
        if (sender === 'tilly' && Object.keys(metadata).length > 0) {
            const metadataDiv = document.createElement('div');
            metadataDiv.className = 'message-metadata';
            
            if (metadata.intent) {
                metadataDiv.innerHTML += `<span class="metadata-item">📍 ${metadata.intent}</span>`;
            }
            if (metadata.mood) {
                const moodEmoji = this.getMoodEmoji(metadata.mood);
                metadataDiv.innerHTML += `<span class="metadata-item">${moodEmoji} ${metadata.mood}</span>`;
            }
            if (metadata.model) {
                metadataDiv.innerHTML += `<span class="metadata-item">🧠 ${metadata.model}</span>`;
            }
            
            content.appendChild(metadataDiv);
        }

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);

        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();

        // Store message
        this.messages.push({
            sender,
            text,
            timestamp: new Date(),
            metadata
        });
    }

    showTypingIndicator() {
        this.isTyping = true;
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message tilly';
        typingDiv.id = 'typingIndicator';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        const avatarImg = document.createElement('img');
        avatarImg.src = '/static/images/avatar.svg';
        avatarImg.alt = 'Tilly';
        avatarImg.onerror = () => {
            avatar.textContent = '🤖';
        };
        avatar.appendChild(avatarImg);

        const content = document.createElement('div');
        content.className = 'message-content';

        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';

        content.appendChild(indicator);
        typingDiv.appendChild(avatar);
        typingDiv.appendChild(content);

        this.messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }

    removeTypingIndicator() {
        this.isTyping = false;
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    formatTime(date) {
        return date.toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        });
    }

    getMoodEmoji(mood) {
        const moodEmojis = {
            'vulnerable': '😔',
            'positive': '😊',
            'neutral': '😐',
            'agitated': '😤'
        };
        return moodEmojis[mood.toLowerCase()] || '💭';
    }

    startNewChat() {
        // Clear messages
        this.messages = [];
        this.messagesContainer.innerHTML = '';
        
        // Generate new session ID
        this.sessionId = this.generateSessionId();
        
        // Show welcome screen again
        const welcomeScreen = document.createElement('div');
        welcomeScreen.className = 'welcome-screen';
        welcomeScreen.id = 'welcomeScreen';
        welcomeScreen.innerHTML = `
            <div class="avatar-large">
                <img src="/static/images/avatar.svg" alt="Tilly Avatar" id="avatarImage">
            </div>
            <h2>Hello! I'm Tilly 💜</h2>
            <p>Your empathetic AI companion focused on mental wellness and genuine human connection.</p>
            <div class="suggestions">
                <h3>Try asking me about:</h3>
                <div class="suggestion-cards">
                    <button class="suggestion-card" data-suggestion="I'm feeling anxious today">
                        <span class="emoji">😟</span>
                        <span>I'm feeling anxious</span>
                    </button>
                    <button class="suggestion-card" data-suggestion="Tell me something to make me smile">
                        <span class="emoji">😊</span>
                        <span>Make me smile</span>
                    </button>
                    <button class="suggestion-card" data-suggestion="How can I manage stress better?">
                        <span class="emoji">🧘</span>
                        <span>Managing stress</span>
                    </button>
                    <button class="suggestion-card" data-suggestion="Just want to chat">
                        <span class="emoji">💬</span>
                        <span>Casual chat</span>
                    </button>
                </div>
            </div>
        `;
        
        this.messagesContainer.appendChild(welcomeScreen);
        this.welcomeScreen = welcomeScreen;
        
        // Reinit suggestion cards
        document.querySelectorAll('.suggestion-card').forEach(card => {
            card.addEventListener('click', () => {
                const suggestion = card.dataset.suggestion;
                this.messageInput.value = suggestion;
                this.sendBtn.disabled = false;
                this.sendMessage();
            });
        });
        
        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        this.sendBtn.disabled = true;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.tillyApp = new TillyApp();
});
