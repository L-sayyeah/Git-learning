const API_BASE = 'http://localhost:8088';
const PROXY_API = 'http://localhost:8088/chat';
let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
let isProcessing = false;

// 状态管理
let appState = {
    searchEnabled: localStorage.getItem('searchEnabled') !== 'false',
    contextWindow: 0 // 保留3轮对话
};

// 初始化UI状态
function initUI() {
    document.getElementById('searchToggle').checked = appState.searchEnabled;
    updateSearchStatus();
}

// 更新搜索状态指示
function updateSearchStatus() {
    const indicator = document.getElementById('searchStatus');
    indicator.className = appState.searchEnabled ? 
        'status-indicator active' : 'status-indicator';
}

// 切换搜索状态
document.getElementById('searchToggle').addEventListener('change', (e) => {
    appState.searchEnabled = e.target.checked;
    localStorage.setItem('searchEnabled', appState.searchEnabled);
    updateSearchStatus();
});

// 新增上下文管理函数
function manageContext(question, needsSearch) {
    // 保留最近3轮对话
    if (chatHistory.length >= 6) {
        chatHistory = chatHistory.slice(-4);
    }
    chatHistory.push({ role: "user", content: question });
    return chatHistory;
}

async function sendWithContext(question) {
    const useSearch = document.getElementById('searchToggle').checked;
    
    const payload = {
        question,
        use_search: useSearch,
        messages: chatHistory.slice(-3) // 保留最近3轮
    };

    try {
        const response = await fetch(PROXY_API, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        // 更新历史记录...
        return data;
    } catch (error) {
        // 错误处理...
    }
}

// 修改后的发送逻辑
async function sendTest() {
    const question = document.getElementById('question').value;
    if (!question) return;

    const needsSearch = appState.searchEnabled && 
        await checkIfNeedsSearch(question);
    
    const result = await sendWithContext(question);
    updateChatUI(result);
}

// 智能判断是否需要搜索
async function checkIfNeedsSearch(question) {
    try {
        const response = await fetch(`${API_BASE}/needs_search`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ question })
        });
        return (await response.json()).search_required;
    } catch {
        return true; // 失败时默认需要搜索
    }
}

// 更新聊天界面
function updateChatUI(result) {
    const chatBox = document.getElementById('result');
    const entry = document.createElement('div');
    entry.className = `chat-entry ${result.sources?.length ? 'with-source' : ''}`;
    
    entry.innerHTML = `
        <div class="question">${result.question}</div>
        <div class="answer">${result.answer}</div>
        ${result.sources?.length ? 
            `<div class="sources">
                <h4>参考来源：</h4>
                ${result.sources.map(s => `
                    <div class="source">
                        <a href="${s.url}" target="_blank">${s.title}</a>
                    </div>
                `).join('')}
            </div>` : ''
        }
    `;
    
    chatBox.appendChild(entry);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// 页面加载时初始化
window.onload = initUI;

async function checkHealth() {
    const statusDiv = document.getElementById('health-status');
    statusDiv.textContent = '检查中...';
    
    try {
        const response = await fetch(API_BASE);
        const data = await response.json();
        statusDiv.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        statusDiv.textContent = `健康检查失败：${error.message}`;
    }
}

// 初始化函数
function init() {
    // 恢复历史记录加载（关键修改）
    chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
    
    // 绑定事件监听
    const sendBtn = document.querySelector('.send-button');
    const textarea = document.getElementById('question');
    
    sendBtn.addEventListener('click', handleSend);
    textarea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });

    // 恢复历史记录渲染（重要）
    renderHistory();

    // 自动调整输入框高度
    autoResize(textarea);
}

function restoreSettings() {
    const searchEnabled = localStorage.getItem('searchEnabled') !== 'false';
    document.getElementById('searchToggle').checked = searchEnabled;
    updateStatusIndicator();
}

function updateStatusIndicator() {
    const indicator = document.getElementById('searchStatus');
    indicator.className = `status-indicator ${isSearchEnabled() ? 'active' : ''}`;
}

function isSearchEnabled() {
    return document.getElementById('searchToggle').checked;
}

function setupEventListeners() {
    document.getElementById('searchToggle').addEventListener('change', () => {
        localStorage.setItem('searchEnabled', isSearchEnabled());
        updateStatusIndicator();
    });
    
    document.getElementById('question').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !isProcessing) sendQuestion();
    });
}

async function sendQuestion() {
    if (isProcessing) return;
    
    const input = document.getElementById('question');
    const question = input.value.trim();
    if (!question) return;

    isProcessing = true;
    input.disabled = true;
    toggleLoading(true);
    
    try {
        addMessage('user', question);
        
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                question,
                use_search: isSearchEnabled(),
                history: chatHistory
            })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || `请求失败 (状态码: ${response.status})`);
        }

        addMessage('assistant', data.answer, data.sources);
        chatHistory = data.history;
        persistChatHistory();
    } catch (error) {
        showError(error.message);
    } finally {
        isProcessing = false;
        input.disabled = false;
        input.value = '';
        toggleLoading(false);
    }
}

function addMessage(role, content, sources = []) {
    // 安全配置Markdown解析
    marked.setOptions({
        highlight: (code, lang) => hljs.highlightAuto(code).value,
        breaks: true,
        sanitize: true
    });

    const container = document.getElementById('chatHistory');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    // 转换Markdown为HTML
    const formattedContent = marked.parse(content);
    
    messageDiv.innerHTML = `
        <div class="content">${formattedContent}</div>
        ${sources.length ? `
            <div class="sources">
                <div class="source-title">📚 数据来源</div>
                ${sources.map((s, i) => `
                    <a href="${s.url}" target="_blank" rel="noopener" class="source-link">
                        【${i+1}】${s.title}
                    </a>
                `).join('')}
            </div>
        ` : ''}
    `;

    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
    
    // 激活代码高亮
    hljs.highlightAll();
}

function toggleLoading(show) {
    const button = document.querySelector('button');
    button.querySelector('.loading-indicator').style.display = show ? 'block' : 'none';
    button.querySelector('.button-text').style.visibility = show ? 'hidden' : 'visible';
    button.disabled = show;
}

function showError(message) {
    const container = document.getElementById('chatHistory');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'message error';
    errorDiv.innerHTML = `
        <div class="error-header">⚠️ 请求遇到问题</div>
        <div class="error-content">${message}</div>
        <div class="error-tip">建议：检查网络连接或稍后重试</div>
    `;
    container.appendChild(errorDiv);
    container.scrollTop = container.scrollHeight;
}

function renderHistory() {
    const container = document.getElementById('chatHistory');
    container.innerHTML = '';
    
    chatHistory
        .filter(msg => msg.role !== 'system')
        .forEach(msg => {
            if (msg.role === 'assistant') {
                addMessage('assistant', msg.content, msg.sources || []);
            } else if (msg.role === 'user') {
                addMessage('user', msg.content);
            }
        });
}

// 持久化聊天记录
function persistChatHistory() {
    try {
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    } catch (e) {
        console.error('本地存储失败:', e);
        showError('本地存储空间已满，部分功能可能受限');
    }
}

// 发送处理函数
async function handleSend() {
    const question = document.getElementById('question').value.trim();
    const sendBtn = document.querySelector('.send-button');
    
    if (!question || sendBtn.disabled) return;

    try {
        // 禁用按钮
        sendBtn.disabled = true;
        sendBtn.querySelector('.loading-indicator').style.display = 'block';
        sendBtn.querySelector('i').style.display = 'none';

        // 添加用户消息
        addMessage('user', question);
        
        // 发送请求
        const response = await fetch('http://localhost:8088/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question,
                use_search: document.getElementById('searchToggle').checked
            })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const data = await response.json();
        addMessage('assistant', data.answer, data.sources);
        
    } catch (error) {
        console.error('请求失败:', error);
        showError('请求失败，请检查网络连接');
    } finally {
        // 重置状态
        sendBtn.disabled = false;
        sendBtn.querySelector('.loading-indicator').style.display = 'none';
        sendBtn.querySelector('i').style.display = 'inline-block';
        document.getElementById('question').value = '';
    }
}

// 自动调整输入框高度
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// 在初始化中添加
document.getElementById('question').addEventListener('input', function() {
    autoResize(this);
});

// 启动初始化
window.addEventListener('DOMContentLoaded', init);

function scrollToBottom() {
    const chatHistory = document.getElementById('chatHistory');
    chatHistory.scrollTo({
        top: chatHistory.scrollHeight,
        behavior: 'smooth'
    });
}

