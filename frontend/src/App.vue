<template>
  <div class="app-container">
    <!-- 左侧线程管理 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <h1 class="app-title">Deer Flow</h1>
        <button class="new-chat-btn" @click="newChat">+ 新建对话</button>
      </div>
      <div class="threads-list">
        <div 
          v-for="thread in threads" 
          :key="thread.id" 
          class="thread-item" 
          :class="{ 'active': activeThreadId === thread.id }"
          @click="switchThread(thread.id)"
        >
          <div class="thread-content">
            <div class="thread-title">{{ thread.title }}</div>
            <div class="thread-preview">{{ thread.preview }}</div>
          </div>
          <button class="thread-delete" @click.stop="deleteThread(thread.id)">×</button>
        </div>
      </div>
      <div class="sidebar-footer">
        <div class="model-info">
          <span class="model-label">当前模型:</span>
          <select v-model="selectedModel" class="model-select">
            <option value="minimax-2.7">Minimax 2.7</option>
            <option value="claude-3-opus">Claude 3 Opus</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 右侧聊天区域 -->
    <div class="chat-container">
      <!-- 聊天头部 -->
      <div class="chat-header">
        <div class="chat-title">{{ currentThread?.title || '新对话' }}</div>
        <div class="chat-actions">
          <button class="action-btn" title="系统状态">
            <span class="status-icon" :class="{ 'status-ok': systemStatus.api, 'status-error': !systemStatus.api }">
              {{ systemStatus.api ? '✅' : '❌' }}
            </span>
          </button>
          <button class="action-btn" title="设置">⚙️</button>
        </div>
      </div>

      <!-- 聊天内容 -->
      <div class="chat-messages" ref="chatMessages">
        <div v-if="currentThread?.messages.length === 0" class="empty-chat">
          <div class="empty-icon">💬</div>
          <h3>开始新的对话</h3>
          <p>选择一个Agent并输入任务描述，开始与AI协作</p>
        </div>
        <div v-else v-for="(message, index) in currentThread?.messages" :key="index" class="message-wrapper">
          <div v-if="message.role === 'user'" class="message user-message">
            <div class="message-avatar">👤</div>
            <div class="message-content">
              <div class="message-text">{{ message.content }}</div>
              <div class="message-meta">
                <span class="message-time">{{ message.timestamp }}</span>
                <span class="message-agent">{{ getAgentName(message.agentType) }}</span>
              </div>
            </div>
          </div>
          <div v-else class="message ai-message">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
              <div class="message-text" v-html="formatMessage(message.content)"></div>
              <div class="message-meta">
                <span class="message-time">{{ message.timestamp }}</span>
                <span class="message-model">{{ selectedModel }}</span>
              </div>
            </div>
          </div>
        </div>
        <div v-if="isLoading" class="loading-message">
          <div class="loading-spinner"></div>
          <span>AI正在生成回复...</span>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="chat-input">
        <div class="input-header">
          <select v-model="form.agentType" class="agent-select">
            <option value="research">Research Agent (研究)</option>
            <option value="code">Code Agent (代码)</option>
            <option value="writing">Writing Agent (写作)</option>
            <option value="multi">Multi-Agent (多Agent协作)</option>
          </select>
        </div>
        <div class="input-container">
          <textarea 
            v-model="form.task" 
            placeholder="输入任务描述..." 
            class="input-textarea"
            @keydown.enter.exact.prevent="executeTask"
            @keydown.enter.shift="$event.target.value += '\n'"
          ></textarea>
          <button 
            class="send-btn" 
            :disabled="isLoading || !form.task"
            @click="executeTask"
          >
            {{ isLoading ? '发送中...' : '发送' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';

const form = ref({
  agentType: 'research',
  task: ''
});

const isLoading = ref(false);
const systemStatus = ref({
  agents: true,
  api: true,
  system: true
});

const chatMessages = ref(null);
const selectedModel = ref('minimax-2.7');

// 线程管理
const threads = ref([
  {
    id: '1',
    title: '新对话',
    preview: '开始与AI协作',
    messages: []
  }
]);

const activeThreadId = ref('1');

const currentThread = computed(() => {
  return threads.value.find(thread => thread.id === activeThreadId.value);
});

// 生成唯一ID
const generateId = () => {
  return Math.random().toString(36).substr(2, 9);
};

// 新建对话
const newChat = () => {
  const newThreadId = generateId();
  threads.value.unshift({
    id: newThreadId,
    title: '新对话',
    preview: '开始与AI协作',
    messages: []
  });
  activeThreadId.value = newThreadId;
};

// 切换对话
const switchThread = (threadId) => {
  activeThreadId.value = threadId;
};

// 删除对话
const deleteThread = (threadId) => {
  const index = threads.value.findIndex(thread => thread.id === threadId);
  if (index !== -1) {
    threads.value.splice(index, 1);
    if (threads.value.length === 0) {
      newChat();
    } else if (activeThreadId.value === threadId) {
      activeThreadId.value = threads.value[0].id;
    }
  }
};

// 获取Agent名称
const getAgentName = (agentType) => {
  const agentMap = {
    research: 'Research Agent',
    code: 'Code Agent',
    writing: 'Writing Agent',
    multi: 'Multi-Agent'
  };
  return agentMap[agentType] || agentType;
};

// 格式化消息内容
const formatMessage = (content) => {
  return content
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/\n\n/gim, '<br><br>')
    .replace(/```(.*?)```/gims, '<pre><code>$1</code></pre>');
};

// 执行任务
const executeTask = async () => {
  if (!form.value.task) {
    return;
  }
  
  isLoading.value = true;
  
  // 添加用户消息
  const userMessage = {
    role: 'user',
    content: form.value.task,
    agentType: form.value.agentType,
    timestamp: new Date().toLocaleString()
  };
  
  currentThread.value.messages.push(userMessage);
  
  // 更新线程标题和预览
  if (currentThread.value.title === '新对话') {
    currentThread.value.title = form.value.task.substring(0, 30) + (form.value.task.length > 30 ? '...' : '');
  }
  currentThread.value.preview = form.value.task.substring(0, 50) + (form.value.task.length > 50 ? '...' : '');
  
  // 清空输入框
  form.value.task = '';
  
  // 滚动到底部
  await nextTick();
  scrollToBottom();
  
  try {
    // 调用后端API（通过Vite代理）
    const response = await fetch('/api/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        agent_type: userMessage.agentType,
        task: userMessage.content
      })
    });
    
    if (!response.ok) {
      throw new Error('API调用失败');
    }
    
    const data = await response.json();
    
    // 添加AI回复
    const aiMessage = {
      role: 'assistant',
      content: data.result,
      timestamp: new Date().toLocaleString()
    };
    
    currentThread.value.messages.push(aiMessage);
  } catch (error) {
    // 添加错误消息
    const errorMessage = {
      role: 'assistant',
      content: `# 错误\n\n执行任务时发生错误：${error.message}`,
      timestamp: new Date().toLocaleString()
    };
    
    currentThread.value.messages.push(errorMessage);
    systemStatus.value.api = false;
  } finally {
    isLoading.value = false;
    // 滚动到底部
    await nextTick();
    scrollToBottom();
  }
};

// 滚动到底部
const scrollToBottom = () => {
  if (chatMessages.value) {
    chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
  }
};

// 检查系统状态
const checkSystemStatus = async () => {
  try {
    const response = await fetch('/api/health');
    if (response.ok) {
      systemStatus.value.api = true;
    } else {
      systemStatus.value.api = false;
    }
  } catch (error) {
    systemStatus.value.api = false;
  }
};

// 组件挂载时检查系统状态
onMounted(() => {
  checkSystemStatus();
  // 每30秒检查一次系统状态
  setInterval(checkSystemStatus, 30000);
});
</script>

<style scoped>
:root {
  --primary: #0066ff;
  --secondary: #6b7280;
  --dark: #1e1e2e;
  --light: #f9fafb;
  --mid-gray: #6b7280;
  --orange: #f97316;
  --green: #10b981;
  --red: #ef4444;
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --border: 1px solid #374151;
  --radius: 8px;
  --transition: all 0.3s ease;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: var(--dark);
  color: var(--light);
  line-height: 1.6;
}

.app-container {
  display: flex;
  min-height: 100vh;
}

/* 左侧边栏 */
.sidebar {
  width: 320px;
  background-color: #16161e;
  border-right: var(--border);
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.sidebar-header {
  margin-bottom: 1.5rem;
}

.app-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 1rem;
}

.new-chat-btn {
  width: 100%;
  padding: 0.75rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
}

.new-chat-btn:hover {
  background: #0052cc;
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

/* 线程列表 */
.threads-list {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.thread-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-radius: var(--radius);
  cursor: pointer;
  transition: var(--transition);
  margin-bottom: 0.5rem;
}

.thread-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.thread-item.active {
  background-color: rgba(0, 102, 255, 0.1);
  border-left: 3px solid var(--primary);
}

.thread-content {
  flex: 1;
  overflow: hidden;
}

.thread-title {
  font-weight: 600;
  color: var(--light);
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.thread-preview {
  font-size: 0.875rem;
  color: var(--mid-gray);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.thread-delete {
  background: none;
  border: none;
  color: var(--mid-gray);
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: var(--radius);
  transition: var(--transition);
}

.thread-delete:hover {
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--red);
}

/* 侧边栏底部 */
.sidebar-footer {
  border-top: var(--border);
  padding-top: 1rem;
}

.model-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.model-label {
  font-size: 0.875rem;
  color: var(--mid-gray);
}

.model-select {
  width: 100%;
  padding: 0.5rem;
  border: var(--border);
  border-radius: var(--radius);
  background: var(--dark);
  color: var(--light);
  font-size: 0.875rem;
  transition: var(--transition);
}

.model-select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
}

/* 右侧聊天区域 */
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: var(--dark);
}

/* 聊天头部 */
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: var(--border);
  background-color: #1a1a2e;
}

.chat-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--light);
}

.chat-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  background: none;
  border: none;
  color: var(--mid-gray);
  font-size: 1rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: var(--radius);
  transition: var(--transition);
}

.action-btn:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: var(--light);
}

.status-icon {
  font-size: 1rem;
}

.status-icon.status-ok {
  color: var(--green);
}

.status-icon.status-error {
  color: var(--red);
}

/* 聊天内容 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.empty-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-chat h3 {
  color: var(--light);
  margin-bottom: 0.5rem;
}

.empty-chat p {
  color: var(--mid-gray);
  max-width: 400px;
}

/* 消息样式 */
.message-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.message {
  display: flex;
  gap: 1rem;
  max-width: 80%;
  animation: fadeIn 0.3s ease-in-out;
}

.user-message {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.ai-message {
  align-self: flex-start;
}

.message-avatar {
  font-size: 1.25rem;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
}

.message-content {
  flex: 1;
}

.message-text {
  padding: 1rem;
  border-radius: var(--radius);
  line-height: 1.6;
}

.user-message .message-text {
  background-color: var(--primary);
  color: white;
  border-bottom-right-radius: 4px;
}

.ai-message .message-text {
  background-color: rgba(255, 255, 255, 0.05);
  color: var(--light);
  border: var(--border);
  border-bottom-left-radius: 4px;
}

.message-meta {
  display: flex;
  gap: 0.75rem;
  font-size: 0.75rem;
  color: var(--mid-gray);
  margin-top: 0.25rem;
}

.user-message .message-meta {
  justify-content: flex-end;
}

.ai-message .message-meta {
  justify-content: flex-start;
}

.message-time {
  white-space: nowrap;
}

.message-agent, .message-model {
  background-color: rgba(255, 255, 255, 0.05);
  padding: 0.125rem 0.5rem;
  border-radius: 12px;
  font-weight: 500;
}

/* 加载消息 */
.loading-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.05);
  border: var(--border);
  border-radius: var(--radius);
  align-self: flex-start;
  max-width: 80%;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--mid-gray);
  border-top: 2px solid var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 输入区域 */
.chat-input {
  border-top: var(--border);
  padding: 1rem 1.5rem;
  background-color: #1a1a2e;
}

.input-header {
  margin-bottom: 0.75rem;
}

.agent-select {
  width: 100%;
  padding: 0.5rem;
  border: var(--border);
  border-radius: var(--radius);
  background: var(--dark);
  color: var(--light);
  font-size: 0.875rem;
  transition: var(--transition);
}

.agent-select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
}

.input-container {
  display: flex;
  gap: 0.75rem;
  align-items: flex-end;
}

.input-textarea {
  flex: 1;
  min-height: 100px;
  max-height: 300px;
  padding: 1rem;
  border: var(--border);
  border-radius: var(--radius);
  background: var(--dark);
  color: var(--light);
  font-size: 1rem;
  resize: vertical;
  font-family: inherit;
  transition: var(--transition);
}

.input-textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
}

.send-btn {
  padding: 0.75rem 1.5rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  align-self: flex-end;
}

.send-btn:hover:not(:disabled) {
  background: #0052cc;
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.send-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* 消息内容格式化 */
.message-text h1 {
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
  color: var(--primary);
}

.message-text h2 {
  font-size: 1.25rem;
  margin: 1rem 0 0.5rem 0;
  color: var(--orange);
}

.message-text h3 {
  font-size: 1.125rem;
  margin: 0.75rem 0 0.375rem 0;
  color: var(--light);
}

.message-text pre {
  background: rgba(0, 0, 0, 0.3);
  border-radius: var(--radius);
  padding: 1rem;
  margin: 1rem 0;
  overflow-x: auto;
  border: var(--border);
}

.message-text code {
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: var(--light);
}

.message-text ul, .message-text ol {
  margin: 1rem 0 1rem 2rem;
}

.message-text li {
  margin-bottom: 0.5rem;
  color: var(--light);
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* 动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    height: 200px;
    border-right: none;
    border-bottom: var(--border);
  }

  .threads-list {
    display: flex;
    overflow-x: auto;
    flex-direction: row;
    gap: 0.5rem;
  }

  .thread-item {
    min-width: 200px;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .thread-delete {
    align-self: flex-end;
  }

  .message {
    max-width: 90%;
  }
}
</style>