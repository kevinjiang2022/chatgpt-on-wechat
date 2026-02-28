# 系统详细功能指南

本文档详细解析了 **Skills（技能）** 和 **Plugins（插件）** 的区别及使用方法，帮助用户更好地理解和扩展系统功能。

## 一、 系统核心模式

系统支持两种运行模式，通过 `config.json` 中的 `"agent"` 字段切换：

| 模式 | 描述 | 适用场景 | 扩展方式 |
| :--- | :--- | :--- | :--- |
| **ChatBot 模式** | 基础问答机器人，被动响应消息。 | 日常闲聊、简单问答、群管理 | **Plugins (插件)** |
| **Agent 模式** | 智能体助理，主动思考、规划任务、使用工具。 | 复杂任务处理、多步操作、系统控制 | **Skills (技能)** + Plugins |

> **注意**：
> *   **ChatBot 模式**：兼容 Python 3.7+。
> *   **Agent 模式**：必须使用 **Python 3.8+**（推荐 3.9），并需将配置改为 `"agent": true`。

---

## 二、 Skills（技能）系统指南

Skills 是 Agent 模式下的核心扩展单元，允许机器人通过自然语言理解用户意图，并调用特定的工具或流程来完成任务。

### 1. Skills 的结构

每个 Skill 是一个包含 `SKILL.md` 文件的目录，标准结构如下：

```text
workspace/skills/my-skill/    <-- Skill 根目录
├── SKILL.md                  <-- [核心] 定义元数据和指令
├── scripts/                  <-- [可选] Python/Bash 脚本
├── references/               <-- [可选] 参考文档/数据结构
└── assets/                   <-- [可选] 静态资源（模板、图片等）
```

### 2. 核心文件 `SKILL.md`

`SKILL.md` 包含两部分：
*   **Frontmatter (元数据)**：定义 Skill 的名称、描述和触发条件。
*   **Body (指令)**：具体的执行步骤和逻辑。

**示例 (`SKILL.md`)：**

```markdown
---
name: pdf-processor
description: Process PDF files including merge, split, and text extraction. Use when user asks to handle PDF documents.
---

# PDF Processor Instructions

1. Check if the input file exists.
2. If the user wants to merge, use the `scripts/merge.py` script...
```

### 3. 如何安装 Skills

Skills 存放在两个位置：
*   **内置 Skills**：项目根目录 `skills/`（如 `linkai-agent`, `openai-image-vision`）。
*   **自定义 Skills**：工作区目录 `workspace/skills/`（用户自定义）。

#### 方法 A：使用 `skill-creator`（推荐）
在 Agent 模式下，您可以直接对机器人说：
> "帮我创建一个处理 Excel 表格的 Skill，功能是读取 A 列并计算总和。"

系统内置的 `skill-creator` 会引导您生成 `SKILL.md` 并自动保存到 `workspace/skills/`。

#### 方法 B：手动安装
1.  在项目根目录下创建 `workspace/skills/` 目录（如果不存在）。
2.  在其中创建一个新文件夹，例如 `workspace/skills/weather-skill/`。
3.  在该文件夹内创建 `SKILL.md` 文件，填入元数据和指令。
4.  （可选）放入必要的脚本文件到 `scripts/` 子目录。
5.  **重启服务**：`python3 app.py`（或使用 `run.sh`/`run.py`）。

#### 方法 C：从 URL 安装
如果有人分享了 Skill 的 URL，您可以让 Agent：
> "安装这个 Skill：https://example.com/my-skill.md"

### 4. 如何使用 Skills

Skills 不需要显式的命令触发，Agent 会根据用户的自然语言自动匹配。
*   **用户输入**："帮我把这几个 PDF 合并成一个。"
*   **系统行为**：Agent 分析语义 -> 匹配到 `pdf-processor` Skill -> 读取 `SKILL.md` -> 执行合并操作。

---

## 三、 Plugins（插件）系统指南

Plugins 是基于事件监听的代码模块，适用于所有模式（ChatBot 和 Agent）。

### 1. 安装位置

所有插件存放在项目根目录的 `plugins/` 文件夹中。

### 2. 安装方法

#### 方法 A：手动安装
1.  下载插件源码。
2.  将插件文件夹解压到 `plugins/` 目录下（例如 `plugins/tool_plugin/`）。
3.  如果插件有 `requirements.txt`，运行：`pip3 install -r plugins/tool_plugin/requirements.txt`。
4.  修改配置：在 `config.json` 的 `"plugins"` 列表中添加插件名，或配置 `plugins/config.json`。

#### 方法 B：使用管理员指令（Godcmd）
在聊天窗口中发送（需要配置管理员权限）：
*   `#installp https://github.com/xxx/plugin.git`：安装插件。
*   `#scanp`：重新扫描并加载插件。

### 3. 常用插件
*   **Godcmd**：管理员命令（如 `#auth`, `#update`）。
*   **Banwords**：违禁词过滤。
*   **Agent** (`plugins/agent`)：这是通过插件形式实现的 AgentMesh 功能（通过 `$agent` 触发），与核心的 CowAgent 模式略有不同。

---

## 四、 总结与建议

| 功能 | Skills (技能) | Plugins (插件) |
| :--- | :--- | :--- |
| **核心逻辑** | 任务规划、工具调用 | 事件监听、消息回复 |
| **触发方式** | 自然语言意图识别 (AI 决策) | 关键词、前缀、消息类型 (规则匹配) |
| **开发难度** | 低 (写 Markdown 文档) | 中 (写 Python 代码) |
| **依赖环境** | **Python 3.8+**, Agent 模式 | Python 3.7+, 任意模式 |

### 建议
*   如果您当前使用的是 **Python 3.7**，建议主要使用 **Plugins** 系统。
*   如果您希望体验强大的 **Skills** 系统和 **Agent** 模式，请升级到 **Python 3.8+**（推荐 3.9），并将 `config.json` 中的 `"agent"` 设置为 `true`。
