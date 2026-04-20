此次合并主要添加了一个完整的前端Vue项目，同时更新了后端依赖版本为范围版本。前端项目实现了多Agent架构系统的可视化界面，包含任务配置和结果展示功能。
| 文件 | 变更 |
|------|---------|
| examples/test_form.html | 删除了该HTML表单测试文件 |
| frontend/.gitignore | 新增前端项目的git忽略文件，定义了需要忽略的文件和目录 |
| frontend/.vscode/extensions.json | 新增VSCode扩展配置，指定了前端开发推荐的扩展 |
| frontend/README.md | 新增前端项目的README文件，提供项目基本信息 |
| frontend/index.html | 新增前端项目的入口HTML文件，设置了页面基本结构 |
| frontend/package.json | 新增前端项目的npm配置文件，定义了项目依赖和脚本 |
| frontend/public/favicon.svg | 新增网站图标文件 |
| frontend/public/icons.svg | 新增图标文件，包含各种图标资源 |
| frontend/src/App.vue | 新增主Vue组件，实现了多Agent系统的界面，包括任务配置和结果展示功能 |
| frontend/src/assets/hero.png | 新增英雄图资源文件 |
| frontend/src/assets/vite.svg | 新增Vite图标资源文件 |
| frontend/src/assets/vue.svg | 新增Vue图标资源文件 |
| frontend/src/components/HelloWorld.vue | 新增示例Vue组件 |
| frontend/src/main.js | 新增前端项目入口文件，初始化Vue应用 |
| frontend/src/style.css | 新增全局样式文件，定义了项目的颜色变量和基本样式 |
| frontend/vite.config.js | 新增Vite配置文件，设置了Vue插件 |
| requirements.txt | 将依赖版本从固定版本改为范围版本，提高了依赖的灵活性 |