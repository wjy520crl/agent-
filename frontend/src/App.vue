<template>
  <div class="container">
    <header>
      <div class="header-bg"></div>
      <h1>多Agent架构系统</h1>
      <p class="subtitle">利用多个专业智能体协作完成复杂任务，提升工作效率和质量</p>
    </header>

    <div class="agent-grid">
      <div class="agent-card">
        <div class="agent-icon">🔍</div>
        <h3>Research Agent</h3>
        <p>信息收集和分析专家，擅长研究和整理信息</p>
      </div>
      <div class="agent-card">
        <div class="agent-icon">💻</div>
        <h3>Code Agent</h3>
        <p>代码生成和执行专家，擅长编程和调试</p>
      </div>
      <div class="agent-card">
        <div class="agent-icon">📊</div>
        <h3>Data Agent</h3>
        <p>数据分析专家，擅长处理和分析数据</p>
      </div>
      <div class="agent-card">
        <div class="agent-icon">✍️</div>
        <h3>Writing Agent</h3>
        <p>内容创作专家，擅长撰写和编辑内容</p>
      </div>
    </div>

    <div class="dashboard">
      <div class="card">
        <h2>任务配置</h2>
        <form @submit.prevent="executeTask">
          <div class="form-group">
            <label for="agentType">选择Agent类型</label>
            <select id="agentType" v-model="form.agentType">
              <option value="research">Research Agent (研究)</option>
              <option value="code">Code Agent (代码)</option>
              <option value="writing">Writing Agent (写作)</option>
              <option value="multi">Multi-Agent (多Agent协作)</option>
            </select>
          </div>
          <div class="form-group">
            <label for="task">任务描述</label>
            <textarea id="task" v-model="form.task" placeholder="请输入详细的任务描述..."></textarea>
          </div>
          <button type="submit" class="btn" :disabled="isLoading">{{ isLoading ? '执行中...' : '执行任务' }}</button>
        </form>
      </div>
      <div class="card">
        <h2>系统状态</h2>
        <div id="systemStatus">
          <p>✅ 所有Agent就绪</p>
          <p>✅ API连接正常</p>
          <p>✅ 系统运行中</p>
        </div>
      </div>
    </div>

    <div class="results">
      <h2>执行结果</h2>
      <div class="result-content">
        <div v-if="isLoading" class="loading">
          <div class="spinner"></div>
          <span>正在执行任务，请稍候...</span>
        </div>
        <div v-else-if="result" v-html="formattedResult"></div>
        <div v-else>
          <p>执行任务后，结果将显示在这里...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const form = ref({
  agentType: 'research',
  task: ''
});

const isLoading = ref(false);
const result = ref('');

const formattedResult = computed(() => {
  return result.value
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/\n\n/gim, '<br><br>')
    .replace(/```(.*?)```/gims, '<pre><code>$1</code></pre>');
});

const executeTask = () => {
  isLoading.value = true;
  
  // 模拟API调用
  setTimeout(() => {
    let resultText = '';
    
    switch(form.value.agentType) {
      case 'research':
        resultText = '# 研究结果\n\n根据您的任务，我进行了详细的研究，发现了以下关键信息：\n\n## 核心发现\n1. **信息点一**：详细描述信息点一的内容和重要性\n2. **信息点二**：详细描述信息点二的内容和重要性\n3. **信息点三**：详细描述信息点三的内容和重要性\n\n## 结论\n这些信息可以帮助您更好地理解问题，并为决策提供依据。';
        break;
      case 'code':
        resultText = '# 代码生成结果\n\n```python\ndef fibonacci(n):\n    """计算斐波那契数列的第n项"""\n    if n <= 0:\n        return 0\n    elif n == 1:\n        return 1\n    else:\n        a, b = 0, 1\n        for _ in range(2, n):\n            a, b = b, a + b\n        return b\n\n# 测试代码\nresult = fibonacci(10)\nprint(f"斐波那契数列的第10项是: {result}")\n```\n\n## 执行结果\n```\n斐波那契数列的第10项是: 34\n```';
        break;
      case 'writing':
        resultText = '# 内容创作结果\n\n## 人工智能简介\n\n人工智能（Artificial Intelligence，简称AI）作为当代最具变革性的技术之一，正在深刻重塑人类社会的方方面面。它是一门融合计算机科学、数学、神经科学和语言学等多学科的前沿领域，旨在开发能够模拟、延伸和扩展人类智能的计算机系统。\n\n从1956年达特茅斯会议首次提出这一概念至今，人工智能已经经历了多次重大突破与低谷，如今正以前所未有的速度改变着我们的世界。\n\n## 核心技术\n- **机器学习**：让计算机从数据中学习\n- **深度学习**：模拟人脑神经网络的学习方法\n- **自然语言处理**：使计算机理解和生成人类语言\n- **计算机视觉**：让计算机理解和分析图像\n\n## 未来展望\n随着技术的不断进步，人工智能将在医疗健康、金融、教育、制造等领域发挥越来越重要的作用，成为推动社会发展的核心动力。';
        break;
      case 'multi':
        resultText = '# 多Agent协作结果\n\n## 综合分析报告\n\n### Research Agent 结果\n进行了详细的研究，收集了相关信息，发现了关键趋势和数据。\n\n### Code Agent 结果\n生成了相关代码并执行，验证了分析结果的正确性。\n\n### Writing Agent 结果\n撰写了综合报告，整合了所有Agent的发现和分析。\n\n## 综合结论\n通过多Agent的协作，成功完成了任务，提供了全面的解决方案。\n\n### 关键发现\n1. **发现一**：详细描述第一个关键发现\n2. **发现二**：详细描述第二个关键发现\n3. **发现三**：详细描述第三个关键发现\n\n### 建议\n基于分析结果，提出以下建议：\n1. **建议一**：详细描述第一个建议\n2. **建议二**：详细描述第二个建议\n3. **建议三**：详细描述第三个建议';
        break;
    }
    
    result.value = resultText;
    isLoading.value = false;
  }, 2000);
};
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
}

.header-bg {
  position: absolute;
  top: -50%;
  left: -10%;
  width: 120%;
  height: 200%;
  background: radial-gradient(circle at 50% 50%, rgba(217, 119, 87, 0.1) 0%, transparent 70%);
  z-index: -1;
}

h1 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, var(--light) 0%, var(--orange) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 1.2rem;
  color: var(--mid-gray);
  max-width: 600px;
  margin: 0 auto;
}

.dashboard {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
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

.results {
  grid-column: 1 / -1;
  background: var(--dark);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--mid-gray);
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
}

.result-content h1 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: var(--orange);
}

.result-content h2 {
  font-size: 1.5rem;
  margin: 1.5rem 0 0.75rem 0;
  color: var(--blue);
}

.result-content h3 {
  font-size: 1.2rem;
  margin: 1.2rem 0 0.5rem 0;
  color: var(--light);
}

.result-content pre {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 6px;
  padding: 1rem;
  margin: 1rem 0;
  overflow-x: auto;
  border: 1px solid var(--mid-gray);
}

.result-content code {
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: var(--light);
}

.result-content ul, .result-content ol {
  margin: 1rem 0 1rem 2rem;
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
}

.agent-card {
  background: var(--dark);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--mid-gray);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
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