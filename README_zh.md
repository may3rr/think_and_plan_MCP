<div style="text-align: center;">
    <img src="img/asset.jpg" alt="展示图片">
    <p>让Claude在回答任务前先进行系统化思考和规划，提高工作效率和质量！</p>
    <p>
        <a href="README_zh.md">中文</a> | <a href="README.md">English</a>
    </p>
</div>

# 📝 任务规划 MCP 服务器

一个 MCP（模型上下文协议）服务器实现，为 Claude 和其他兼容 MCP 的 AI 助手提供任务规划和跟踪工具。

## 📋 概述

这个任务规划 MCP 服务器使 AI 助手能够：

1. 创建结构化的任务计划 ✨
2. 添加并跟踪完成任务的步骤 📊
3. 在完成步骤时将其标记为完成 ✅
4. 记录并解决任务执行过程中出现的问题 🛠️
5. 查看计划的当前状态 👀

所有规划信息都存储在本地的 `plan.md` 文件中，可以由人类查看和编辑。

## ✨ 功能特点

- **结构化规划**：创建带有步骤和规划说明的有组织的任务计划 📑
- **进度跟踪**：在执行步骤时将其标记为完成 ⏱️
- **问题管理**：记录问题及其解决方案 🔍
- **审查能力**：随时查看整个计划或特定任务 👁️
- **基于文件的存储**：所有信息存储在人类可读的 Markdown 文件中 📁

## 🛠️ 提供的工具

此 MCP 服务器提供以下工具：

| 工具 | 描述 |
|------|-------------|
| `think_and_plan` | 为任务创建新的结构化计划 🧠 |
| `add_step` | 向现有任务计划添加新步骤 ➕ |
| `mark_step_complete` | 将步骤标记为已完成 ✓ |
| `review_plan` | 查看当前计划内容 📖 |
| `add_issue` | 记录特定步骤的问题 ⚠️ |
| `resolve_issue` | 标记问题已解决并提供说明 🎯 |
| `update_planning_notes` | 更新任务的规划说明 📝 |
| `check_task_completion` | 检查任务的完成状态 🔄 |

## 📥 安装

### 前提条件

- Python 3.10+ 🐍
- MCP SDK (`pip install mcp`)

### 设置

1. 克隆此仓库：
   ```
   git clone https://github.com/may3rr/think_and_plan_MCP.git
   cd think_and_plan_MCP
   ```

2. 安装依赖：
   ```
   pip install mcp
   ```

3. 直接运行服务器：
   ```
   python planner_server.py
   ```

### Claude Desktop 集成

要与 Claude Desktop 一起使用：

1. 打开 Claude Desktop 设置
2. 编辑配置文件
3. 在你的 `claude_desktop_config.json` 中添加以下内容：

```json
"TaskPlanner": {
  "command": "/path/to/python",
  "args": [
    "/path/to/think_and_plan_MCP/planner_server.py"
  ]
}
```

将 `/path/to/python` 替换为你的 Python 解释器路径，并更新 planner_server.py 文件的路径。

## 🚀 使用方法

一旦服务器运行并连接到 MCP 客户端（如 Claude Desktop），你可以在对话中使用这些工具：

### 示例工作流程

1. 从创建计划开始：
   ```
   think_and_plan("构建个人网站")
   ```

2. 添加具体步骤：
   ```
   add_step("设置开发环境")
   add_step("创建 HTML 结构")
   add_step("使用 CSS 设计样式")
   add_step("添加 JavaScript 交互")
   add_step("部署到托管服务")
   ```

3. 在工作时将步骤标记为完成：
   ```
   mark_step_complete("设置开发环境")
   ```

4. 记录任何问题：
   ```
   add_issue("CSS 样式未应用于导航菜单", "使用 CSS 设计样式")
   ```

5. 解决问题：
   ```
   resolve_issue("使用 CSS 设计样式", "通过纠正 CSS 选择器特异性解决")
   ```

6. 检查进度：
   ```
   check_task_completion("构建个人网站")
   ```

7. 随时查看计划：
   ```
   review_plan()
   ```

## 📄 plan.md 的结构

规划器创建一个具有如下结构的 `plan.md` 文件：

```markdown
# 任务计划

创建于: 2025-03-16 14:30:00

## 构建个人网站

创建: 2025-03-16 14:30:00

### 规划说明

这是对任务的初步分析。

### 步骤

[✅] 设置开发环境
[ ] 创建 HTML 结构
[ ] 使用 CSS 设计样式
    - ⚠️ 问题: CSS 样式未应用于导航菜单 (✓ 已解决: 通过纠正 CSS 选择器特异性解决)
[ ] 添加 JavaScript 交互
[ ] 部署到托管服务
```

## ❓ 故障排除

- **权限错误**：确保创建 `plan.md` 的目录具有写入权限。
- **集成问题**：检查 Claude Desktop 日志中的连接错误。
- **MCP 错误**：确保正确安装了 MCP SDK。


## 📜 许可证

MIT

## 🤝 贡献

欢迎贡献！请随时提交拉取请求。