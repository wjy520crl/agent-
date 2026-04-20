<template>
  <div class="container">
    <header>
      <div class="header-bg"></div>
      <h1>多Agent架构系统</h1>
      <p class="subtitle">利用多个专业智能体协作完成复杂任务，提升工作效率和质量</p>
    </header>

    <div class="agent-grid">
      <div class="agent-card" v-for="agent in agents" :key="agent.type">
        <div class="agent-icon">{{ agent.icon }}</div>
        <h3>{{ agent.name }}</h3>
        <p>{{ agent.description }}</p>
      </div>
    </div>

    <div class="dashboard">
      <div class="card">
        <h2>任务配置</h2>
        <form @submit.prevent="executeTask">
          <div class="form-group">
            <label for="agentType">选择Agent类型</label>
            <select id="agentType" v-model="form.agentType" style="z-index: 1000; position: relative;">
              <option value="research">Research Agent (研究)</option>
              <option value="code">Code Agent (代码)</option>
              <option value="writing">Writing Agent (写作)</option>
              <option value="multi">Multi-Agent (多Agent协作)</option>
            </select>
          </div>
          <div class="form-group">
            <label for="task">任务描述</label>
            <div style="position: relative;">
              <textarea id="task" v-model="form.task" placeholder="请输入详细的任务描述..." :class="{ 'error': hasError }"></textarea>
              <button type="button" v-if="form.task" @click="form.task = ''" style="position: absolute; right: 10px; bottom: 10px; padding: 0.5rem; font-size: 0.8rem;">清除</button>
            </div>
            <p v-if="hasError" class="error-message">请输入任务描述</p>
          </div>
          <button type="submit" class="btn" :disabled="isLoading || !form.task">{{ isLoading ? '执行中...' : '执行任务' }}</button>
        </form>
      </div>
      <div class="card">
        <h2>系统状态</h2>
        <div id="systemStatus">
          <p :class="{ 'status-ok': systemStatus.agents, 'status-error': !systemStatus.agents }">
            {{ systemStatus.agents ? '✅ 所有Agent就绪' : '❌ Agent未就绪' }}
          </p>
          <p :class="{ 'status-ok': systemStatus.api, 'status-error': !systemStatus.api }">
            {{ systemStatus.api ? '✅ API连接正常' : '❌ API连接失败' }}
          </p>
          <p :class="{ 'status-ok': systemStatus.system, 'status-error': !systemStatus.system }">
            {{ systemStatus.system ? '✅ 系统运行中' : '❌ 系统异常' }}
          </p>
        </div>
      </div>
    </div>

    <div class="results">
      <h2>执行结果</h2>
      <div class="result-content" :class="{ 'loading': isLoading }">
        <div v-if="isLoading" class="loading">
          <div class="spinner"></div>
          <span>正在执行任务，请稍候...</span>
        </div>
        <div v-else-if="result" v-html="formattedResult" class="result-text"></div>
        <div v-else class="empty-result">
          <p>执行任务后，结果将显示在这里...</p>
        </div>
      </div>
    </div>
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
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

header {
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
  animation: fadeIn 1s ease-in-out;
}

.header-bg {
  position: absolute;
  top: -50%;
  left: -10%;
  width: 120%;
  height: 200%;
  background: radial-gradient(circle at 50% 50%, rgba(217, 119, 87, 0.1) 0%, transparent 70%);
  z-index: -1;
  animation: pulse 4s ease-in-out infinite;
}

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

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

h1 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, var(--light) 0%, var(--orange) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: slideIn 1s ease-in-out 0.2s both;
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

.subtitle {
  font-size: 1.2rem;
  color: var(--mid-gray);
  max-width: 600px;
  margin: 0 auto;
  animation: slideIn 1s ease-in-out 0.4s both;
}

.dashboard {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
  animation: fadeIn 1s ease-in-out 0.6s both;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--light);
}

textarea.error {
  border-color: #e74c3c;
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.error-message {
  color: #e74c3c;
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

.status-ok {
  color: #2ecc71;
}

.status-error {
  color: #e74c3c;
}

.results {
  grid-column: 1 / -1;
  background: var(--dark);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--mid-gray);
  animation: fadeIn 1s ease-in-out 0.8s both;
}

.results h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--orange);
}

.result-content {
  background: var(--dark);
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid var(--mid-gray);
  min-height: 200px;
  font-family: 'Lora', Georgia, serif;
  transition: all 0.3s ease;
}

.result-content.loading {
  opacity: 0.7;
}

.result-text {
  animation: fadeIn 0.5s ease-in-out;
}

.empty-result {
  color: var(--mid-gray);
  text-align: center;
  padding: 2rem;
  border: 1px dashed var(--mid-gray);
  border-radius: 8px;
  animation: fadeIn 0.5s ease-in-out;
}

.result-content h1 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: var(--orange);
  animation: slideIn 0.5s ease-in-out;
}

.result-content h2 {
  font-size: 1.5rem;
  margin: 1.5rem 0 0.75rem 0;
  color: var(--blue);
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
  border-radius: 6px;
  padding: 1rem;
  margin: 1rem 0;
  overflow-x: auto;
  border: 1px solid var(--mid-gray);
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
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--mid-gray);
  border-top: 3px solid var(--orange);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.agent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
  animation: fadeIn 1s ease-in-out 0.5s both;
}

.agent-card {
  background: var(--dark);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--mid-gray);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
  animation: fadeIn 0.5s ease-in-out;
}

.agent-card:nth-child(1) {
  animation-delay: 0.6s;
}

.agent-card:nth-child(2) {
  animation-delay: 0.7s;
}

.agent-card:nth-child(3) {
  animation-delay: 0.8s;
}

.agent-card:nth-child(4) {
  animation-delay: 0.9s;
}

.agent-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
  border-color: var(--orange);
}

.agent-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, var(--orange) 0%, #c76645 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 2rem;
  transition: transform 0.3s ease;
}

.agent-card:hover .agent-icon {
  transform: scale(1.1);
}

.agent-card h3 {
  margin-bottom: 0.5rem;
  color: var(--light);
}

.agent-card p {
  color: var(--mid-gray);
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .dashboard {
    grid-template-columns: 1fr;
  }

  h1 {
    font-size: 2rem;
  }

  .container {
    padding: 1rem;
  }
}
</style>