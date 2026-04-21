<template>
  <div class="container">
    <header>
      <nav class="nav">
        <div class="nav-left">
          <h1 class="nav-title">多Agent架构系统</h1>
        </div>
        <div class="nav-right">
          <a href="#" class="nav-link">文档</a>
          <a href="#" class="nav-link">GitHub</a>
        </div>
      </nav>
      <div class="hero">
        <h1 class="hero-title">多Agent架构系统</h1>
        <p class="hero-subtitle">利用多个专业智能体协作完成复杂任务，提升工作效率和质量</p>
        <div class="hero-stats">
          <div class="stat">
            <span class="stat-number">4</span>
            <span class="stat-label">专业Agent</span>
          </div>
          <div class="stat">
            <span class="stat-number">100%</span>
            <span class="stat-label">任务成功率</span>
          </div>
          <div class="stat">
            <span class="stat-number">实时</span>
            <span class="stat-label">系统状态</span>
          </div>
        </div>
      </div>
    </header>

    <div class="features">
      <h2 class="section-title">核心功能</h2>
      <div class="feature-grid">
        <div class="feature-card" v-for="agent in agents" :key="agent.type">
          <div class="feature-icon">{{ agent.icon }}</div>
          <h3 class="feature-title">{{ agent.name }}</h3>
          <p class="feature-description">{{ agent.description }}</p>
        </div>
      </div>
    </div>

    <div class="dashboard">
      <div class="card">
        <h3 class="card-title">任务配置</h3>
        <form @submit.prevent="executeTask">
          <div class="form-group">
            <label for="agentType">选择Agent类型</label>
            <select id="agentType" v-model="form.agentType" class="form-select">
              <option value="research">Research Agent (研究)</option>
              <option value="code">Code Agent (代码)</option>
              <option value="writing">Writing Agent (写作)</option>
              <option value="multi">Multi-Agent (多Agent协作)</option>
            </select>
          </div>
          <div class="form-group">
            <label for="task">任务描述</label>
            <div class="textarea-container">
              <textarea id="task" v-model="form.task" placeholder="请输入详细的任务描述..." :class="{ 'error': hasError }" class="form-textarea"></textarea>
              <button type="button" v-if="form.task" @click="form.task = ''" class="clear-button">清除</button>
            </div>
            <p v-if="hasError" class="error-message">请输入任务描述</p>
          </div>
          <button type="submit" class="btn" :disabled="isLoading || !form.task">{{ isLoading ? '执行中...' : '执行任务' }}</button>
        </form>
      </div>
      <div class="card">
        <h3 class="card-title">系统状态</h3>
        <div class="status-section">
          <div class="status-item" :class="{ 'status-ok': systemStatus.agents, 'status-error': !systemStatus.agents }">
            <span class="status-icon">{{ systemStatus.agents ? '✅' : '❌' }}</span>
            <span class="status-text">{{ systemStatus.agents ? '所有Agent就绪' : 'Agent未就绪' }}</span>
          </div>
          <div class="status-item" :class="{ 'status-ok': systemStatus.api, 'status-error': !systemStatus.api }">
            <span class="status-icon">{{ systemStatus.api ? '✅' : '❌' }}</span>
            <span class="status-text">{{ systemStatus.api ? 'API连接正常' : 'API连接失败' }}</span>
          </div>
          <div class="status-item" :class="{ 'status-ok': systemStatus.system, 'status-error': !systemStatus.system }">
            <span class="status-icon">{{ systemStatus.system ? '✅' : '❌' }}</span>
            <span class="status-text">{{ systemStatus.system ? '系统运行中' : '系统异常' }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="results">
      <h2 class="section-title">执行结果</h2>
      <div class="result-content" :class="{ 'loading': isLoading }">
        <div v-if="isLoading" class="loading">
          <div class="spinner"></div>
          <span>正在执行任务，请稍候...</span>
        </div>
        <div v-else-if="result" v-html="formattedResult" class="result-text"></div>
        <div v-else class="empty-result">
          <div class="empty-icon">📋</div>
          <h3>执行任务后，结果将显示在这里</h3>
          <p>输入任务描述并选择Agent类型开始执行</p>
        </div>
      </div>
    </div>

    <footer class="footer">
      <p>多Agent架构系统 © 2026</p>
      <div class="footer-links">
        <a href="#" class="footer-link">文档</a>
        <a href="#" class="footer-link">GitHub</a>
        <a href="#" class="footer-link">关于</a>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const form = ref({
  agentType: 'research',
  task: ''
});

const isLoading = ref(false);
const result = ref('');
const hasError = ref(false);
const systemStatus = ref({
  agents: true,
  api: true,
  system: true
});

const agents = ref([
  {
    type: 'research',
    name: 'Research Agent',
    description: '信息收集和分析专家，擅长研究和整理信息',
    icon: '🔍'
  },
  {
    type: 'code',
    name: 'Code Agent',
    description: '代码生成和执行专家，擅长编程和调试',
    icon: '💻'
  },
  {
    type: 'data',
    name: 'Data Agent',
    description: '数据分析专家，擅长处理和分析数据',
    icon: '📊'
  },
  {
    type: 'writing',
    name: 'Writing Agent',
    description: '内容创作专家，擅长撰写和编辑内容',
    icon: '✍️'
  }
]);

const formattedResult = computed(() => {
  return result.value
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/\n\n/gim, '<br><br>')
    .replace(/```(.*?)```/gims, '<pre><code>$1</code></pre>');
});

const executeTask = async () => {
  if (!form.value.task) {
    hasError.value = true;
    return;
  }
  
  hasError.value = false;
  isLoading.value = true;
  
  try {
    // 调用后端API（通过Vite代理）
    const response = await fetch('/api/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        agent_type: form.value.agentType,
        task: form.value.task
      })
    });
    
    if (!response.ok) {
      throw new Error('API调用失败');
    }
    
    const data = await response.json();
    result.value = data.result;
  } catch (error) {
    result.value = `# 错误\n\n执行任务时发生错误：${error.message}`;
    systemStatus.value.api = false;
  } finally {
    isLoading.value = false;
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

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Navigation */
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 0;
  border-bottom: var(--border);
}

.nav-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--light);
  margin: 0;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: var(--mid-gray);
  text-decoration: none;
  font-weight: 500;
  transition: var(--transition);
}

.nav-link:hover {
  color: var(--primary);
}

/* Hero Section */
.hero {
  text-align: center;
  padding: 4rem 0;
  background: linear-gradient(135deg, rgba(0, 102, 255, 0.1) 0%, rgba(249, 115, 22, 0.1) 100%);
  border-radius: var(--radius);
  margin: 2rem 0;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: var(--light);
  animation: fadeIn 1s ease-in-out;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--mid-gray);
  max-width: 600px;
  margin: 0 auto 2rem;
  animation: fadeIn 1s ease-in-out 0.2s both;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 3rem;
  animation: fadeIn 1s ease-in-out 0.4s both;
}

.stat {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 0.25rem;
}

.stat-label {
  color: var(--mid-gray);
  font-size: 0.875rem;
}

/* Features Section */
.features {
  margin: 4rem 0;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--light);
  margin-bottom: 2rem;
  text-align: center;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: var(--dark);
  border: var(--border);
  border-radius: var(--radius);
  padding: 2rem;
  text-align: center;
  transition: var(--transition);
  animation: fadeIn 0.5s ease-in-out;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--light);
  margin-bottom: 0.75rem;
}

.feature-description {
  color: var(--mid-gray);
  line-height: 1.5;
}

/* Dashboard */
.dashboard {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin: 3rem 0;
  animation: fadeIn 1s ease-in-out 0.6s both;
}

.card {
  background: var(--dark);
  border: var(--border);
  border-radius: var(--radius);
  padding: 1.5rem;
  box-shadow: var(--shadow);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--light);
  margin-bottom: 1.5rem;
  border-bottom: var(--border);
  padding-bottom: 0.75rem;
}

/* Form Styles */
.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--light);
}

.form-select {
  width: 100%;
  padding: 0.75rem;
  border: var(--border);
  border-radius: var(--radius);
  background: var(--dark);
  color: var(--light);
  font-size: 1rem;
  transition: var(--transition);
}

.form-select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
}

.textarea-container {
  position: relative;
}

.form-textarea {
  width: 100%;
  min-height: 150px;
  padding: 0.75rem;
  border: var(--border);
  border-radius: var(--radius);
  background: var(--dark);
  color: var(--light);
  font-size: 1rem;
  resize: vertical;
  transition: var(--transition);
}

.form-textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
}

.form-textarea.error {
  border-color: var(--red);
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.clear-button {
  position: absolute;
  right: 10px;
  bottom: 10px;
  padding: 0.5rem;
  font-size: 0.8rem;
  background: var(--secondary);
  color: var(--light);
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: var(--transition);
}

.clear-button:hover {
  background: var(--mid-gray);
}

.error-message {
  color: var(--red);
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

.btn {
  width: 100%;
  padding: 0.75rem 1.5rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
}

.btn:hover:not(:disabled) {
  background: #0052cc;
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Status Section */
.status-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: var(--radius);
  transition: var(--transition);
}

.status-item.status-ok {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-item.status-error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.status-icon {
  font-size: 1.25rem;
}

.status-text {
  color: var(--light);
  font-weight: 500;
}

/* Results Section */
.results {
  margin: 3rem 0;
  animation: fadeIn 1s ease-in-out 0.8s both;
}

.result-content {
  background: var(--dark);
  border: var(--border);
  border-radius: var(--radius);
  padding: 2rem;
  min-height: 300px;
  font-family: 'Lora', Georgia, serif;
  transition: var(--transition);
}

.result-content.loading {
  opacity: 0.7;
}

.result-text {
  animation: fadeIn 0.5s ease-in-out;
  line-height: 1.6;
}

.empty-result {
  text-align: center;
  padding: 4rem 2rem;
  border: 2px dashed var(--border);
  border-radius: var(--radius);
  animation: fadeIn 0.5s ease-in-out;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-result h3 {
  color: var(--light);
  margin-bottom: 0.5rem;
}

.empty-result p {
  color: var(--mid-gray);
}

.result-content h1 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: var(--primary);
  animation: slideIn 0.5s ease-in-out;
}

.result-content h2 {
  font-size: 1.5rem;
  margin: 1.5rem 0 0.75rem 0;
  color: var(--orange);
  animation: slideIn 0.5s ease-in-out 0.1s both;
}

.result-content h3 {
  font-size: 1.2rem;
  margin: 1.2rem 0 0.5rem 0;
  color: var(--light);
  animation: slideIn 0.5s ease-in-out 0.2s both;
}

.result-content pre {
  background: rgba(0, 0, 0, 0.3);
  border-radius: var(--radius);
  padding: 1rem;
  margin: 1rem 0;
  overflow-x: auto;
  border: var(--border);
  animation: slideIn 0.5s ease-in-out 0.3s both;
}

.result-content code {
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: var(--light);
}

.result-content ul, .result-content ol {
  margin: 1rem 0 1rem 2rem;
  animation: slideIn 0.5s ease-in-out 0.4s both;
}

.result-content li {
  margin-bottom: 0.5rem;
  color: var(--light);
}

/* Loading */
.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 4rem 2rem;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--mid-gray);
  border-top: 3px solid var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Footer */
.footer {
  margin-top: auto;
  padding: 2rem 0;
  border-top: var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  animation: fadeIn 1s ease-in-out 1s both;
}

.footer p {
  color: var(--mid-gray);
  margin: 0;
}

.footer-links {
  display: flex;
  gap: 1.5rem;
}

.footer-link {
  color: var(--mid-gray);
  text-decoration: none;
  transition: var(--transition);
}

.footer-link:hover {
  color: var(--primary);
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .dashboard {
    grid-template-columns: 1fr;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-stats {
    flex-direction: column;
    gap: 1.5rem;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }

  .footer {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .nav {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .nav-right {
    justify-content: center;
  }
}
</style>