---
name: "hiagent-cli"
description: "当用户想在本仓库里用命令行(cli-anything-hiagent / python -m cli_anything.hiagent_sdk)管理 HiAgent 配置、会话(session)、对话(chat)、工作流(workflow)、工具(tool)、知识库(knowledge)、文件上传下载(up)或观察(observe)时，务必使用这个技能给出可直接执行的命令与排障步骤。尤其适用于用户提到 agent-harness、cli_anything、--project、--json、app-key、workspace-id、VOLC_ACCESSKEY/VOLC_SECRETKEY、.hiagent/config.json。"
---
 
# hiagent-cli（agent-harness/cli_anything）
 
本技能用于在该代码库中正确、可复现地使用 HiAgent harness CLI。
 
CLI 的“已安装命令”是 `cli-anything-hiagent`；在开发态/未安装时，等价的 fallback 入口是：
 
```bash
python -m cli_anything.hiagent_sdk
```

在本技能中，`<CMD>` 代表你最终选定的入口（两者选其一）：

```bash
CMD="cli-anything-hiagent"
# 或
CMD="python -m cli_anything.hiagent_sdk"
```

## References（按需阅读）

当用户聚焦某个命令组时，优先阅读对应 reference 再输出命令，避免遗漏参数细节：

- config：`references/config.md`
- session：`references/session.md`
- chat：`references/chat.md`
- tool：`references/tool.md`
- workflow：`references/workflow.md`
- knowledge：`references/knowledge.md`
- file：`references/file.md`
- observe：`references/observe.md`
- 通用排障：`references/troubleshooting.md`
 
## 你要做什么（高层流程）
 
1. 先确定使用哪个入口（已安装命令 vs python -m fallback）。
2. 明确项目根目录（强烈建议总是显式传 `--project/-p`，避免污染用户当前目录）。
3. 能用 `--json` 就用 `--json`，方便脚本化和稳定解析。
4. 根据用户目标，选择对应命令组：config / session / chat / tool / workflow / knowledge / file / observe。
5. 如果命令需要鉴权或参数缺失，优先通过 `config show` 与环境变量排查，而不是“猜”。
 
## 入口选择（非常重要）
 
优先使用已安装命令：
 
```bash
cli-anything-hiagent --version
```
 
如果用户在开发仓库里还没安装，或 PATH 找不到命令，则改用模块入口（在 `agent-harness` 目录下执行最稳）：
 
```bash
python -m cli_anything.hiagent_sdk --version
```
 
输出命令时，遵循这个惯例：
 
- **如果用户明确说“我已 pip install -e agent-harness”**：默认 `cli-anything-hiagent ...`
- **否则**：默认 `python -m cli_anything.hiagent_sdk ...`，并建议用户执行安装命令以获得更短的入口：
  - `cd agent-harness && pip install -e .`
 
## 项目根目录（--project/-p）
 
CLI 会在 `<project_root>/.hiagent/` 下写入配置与会话数据：
 
- 配置：`<project_root>/.hiagent/config.json`
- 会话：`<project_root>/.hiagent/sessions/`
 
因此：
 
- 用户给了项目路径：始终用 `--project <path>`
- 用户没给：默认用当前仓库根或当前工作目录，并在输出里说明会写入 `.hiagent/`
- 用户希望“完全不落盘”：建议使用一个临时目录作为 `--project`（但不要在技能里写交互式命令；只给可执行方案）
 
## 安全与保密
 
- 永远不要在输出中回显用户的 `VOLC_SECRETKEY`、`app-key` 等敏感值。
- 演示命令中用占位符：`<APP_KEY>`、`<WORKSPACE_ID>`、`<VOLC_ACCESSKEY>`、`<VOLC_SECRETKEY>`。
 
## 常用命令速查（按目标选）
 
更完整的分模块说明见 `references/` 目录；这里仅保留最短可用示例。

### 配置（config）
 
查看“环境变量覆盖后的 effective 配置”和“项目落盘配置”：
 
```bash
<CMD> --json --project <PROJECT_ROOT> config show
```
 
写入项目配置（只写入你传入的字段）：
 
```bash
<CMD> --json --project <PROJECT_ROOT> config set --app-key <APP_KEY> --workspace-id <WORKSPACE_ID>
```
 
建议优先解释两层配置来源：
 
- effective：环境变量与 `~/.volc/.env` 会覆盖项目配置
- project：写在 `.hiagent/config.json` 的持久化值
 
### 会话（session）
 
创建/列出/查看/删除：
 
```bash
<CMD> --json --project <PROJECT_ROOT> session create <NAME> --conversation-id <CONV_ID> --workflow-id <WF_ID> --tool-id <TOOL_ID> --dataset-ids ds-001,ds-002
<CMD> --json --project <PROJECT_ROOT> session list
<CMD> --json --project <PROJECT_ROOT> session show <NAME>
<CMD> --json --project <PROJECT_ROOT> session delete <NAME>
```
 
如果用户只给了部分信息（比如只有 conversation-id），其余参数可以省略。
 
### 对话（chat）
 
创建会话与发送消息：
 
```bash
<CMD> --json --project <PROJECT_ROOT> chat create --app-key <APP_KEY> --user-id <USER_ID> -v name=my_agent -v version=1.0
<CMD> --json --project <PROJECT_ROOT> chat send --app-key <APP_KEY> --conversation-id <CONV_ID> --user-id <USER_ID> -q "Hello" --stream
```
 
要点：
 
- `--stream` 会输出流式响应；如果用户要脚本化采集，优先不加 stream 或说明如何处理
- 如果用户未提供 `--user-id`，可提示其通过 `config set --user-id ...` 设置默认值
 
### 工具（tool）
 
执行工具（`--input` 支持内联 JSON 或 `@file.json`）：
 
```bash
<CMD> --json --project <PROJECT_ROOT> tool execute --workspace-id <WORKSPACE_ID> --tool-id <TOOL_ID> --input '{"input":"test"}'
<CMD> --json --project <PROJECT_ROOT> tool execute --workspace-id <WORKSPACE_ID> --tool-id <TOOL_ID> --input @input.json
```
 
### 工作流（workflow）
 
获取工作流信息 / 查询状态 / 运行：
 
```bash
<CMD> --json --project <PROJECT_ROOT> workflow get --workspace-id <WORKSPACE_ID> --workflow-id <WF_ID>
<CMD> --json --project <PROJECT_ROOT> workflow status --app-key <APP_KEY> --run-id <RUN_ID> --user-id <USER_ID>
<CMD> --json --project <PROJECT_ROOT> workflow run --app-key <APP_KEY> --workspace-id <WORKSPACE_ID> --workflow-id <WF_ID> --input @input.json --stream
```
 
要点：
 
- `--async`（如果用户明确需要异步）会立刻返回 run_id，然后配合 `workflow status`
- `--input` 的 JSON 结构由工作流定义；不要瞎猜字段，优先让用户提供或先 `workflow get` 看 schema/inputs
 
### 知识库（knowledge）
 
检索数据集：
 
```bash
<CMD> --json --project <PROJECT_ROOT> knowledge retrieve --workspace-id <WORKSPACE_ID> --dataset-ids ds-001,ds-002 -q "query" --top-k 5 --score-threshold 0.5
```
 
### 文件（file / UP）
 
上传：
 
```bash
<CMD> --json --project <PROJECT_ROOT> file upload --file ./document.pdf --expire 15h
```
 
下载：
 
```bash
<CMD> --json --project <PROJECT_ROOT> file download --path "<REMOTE_PATH>" --output ./document.pdf
```
 
### 观测（observe）
 
创建 Token / 列出 Trace：
 
```bash
<CMD> --json --project <PROJECT_ROOT> observe token create --workspace-id <WORKSPACE_ID> --custom-app-id <CUSTOM_APP_ID>
<CMD> --json --project <PROJECT_ROOT> observe trace list --workspace-id <WORKSPACE_ID> --page-size 10 --sort-by StartTime --sort-order Desc
```
 
## 输出模板（你对用户的最终回答应遵循）
 
当用户提出“我要做 X”时，你的回答应包含：
 
1. **推荐的入口与变量替换**：先给 `<CMD>` 的定义（`cli-anything-hiagent` 或 `python -m ...`）
2. **可直接复制的命令**：按顺序给 1~5 条命令即可
3. **预期输出与下一步**：说明关键字段在哪里（尤其 JSON 模式下的 `success/message/data`）
4. **最小排障**：缺鉴权/缺参数/404/导入失败时该怎么查（优先 `config show`、检查 `--project`、检查 env）
 
## 常见问题与排障
 
- **命令不存在**：提示用户在 `agent-harness` 下执行 `pip install -e .`；或使用 `python -m cli_anything.hiagent_sdk ...`
- **鉴权失败**：确认 `VOLC_ACCESSKEY`/`VOLC_SECRETKEY` 或 `~/.volc/.env` 是否存在；再用 `config show` 看 effective 配置
- **workspace/app-key 不一致**：effective 配置被环境变量覆盖时最常见；让用户明确选择一种来源并统一
- **需要非交互**：不要引导进入 REPL；优先给确定的子命令调用
