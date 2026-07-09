
---

# 蓝马甲陪护者护航 MCP
**2026 小X宝开源医疗社区黑客松 · 志愿者全流程辅助系统**

### 💡 一句话介绍
> 志愿者只需粘贴群聊中的家属倾诉或服务记录，MCP 服务端即可自动识别情境、输出“阶梯式共情话术”与“志愿者行动指南”，同时集成了**压力可视化测评、交接简报一键下载、公众号推文自动生成**等落地工具，为非医疗背景的志愿者提供全方位支持。

---

### ⚖️ 合规与安全声明（操作红线）
- 🚫 **不构成诊疗**：本工具仅提供同伴支持辅助，不构成医疗诊断、心理咨询或治疗建议。
- 🔒 **隐私保护**：禁止在系统中输入包含真实患者姓名、身份证号、床位号等可识别隐私信息。
- 🚨 **危机干预**：若输入内容涉及自伤/自杀/伤人风险，请**立即终止AI交互**，直接拨打 **120** 或心理危机干预热线 **400-161-9995**。

---

### 🛠️ MCP 工具清单（共 9 个）
根据 `mcp_server.py` 底层服务，系统向 AI Agent 暴露了以下完整工具链：

| 工具名称 | 核心作用 |
| :--- | :--- |
| `classify_caregiver_moment` | 识别当前家属情绪与对话情境（如情绪崩溃、资源求助等） |
| `generate_peer_response_card` | 生成志愿者应对的“阶梯共情话术”与禁忌红线 |
| `suggest_next_steps` | 输出立即可以执行的心理支持与转介行动建议 |
| `caregiver_load_screening` | 家属/志愿者压力负荷快速筛查（1-5分） |
| `hospice_resource_checklist` | 根据输入属地，输出真实安宁资源核对清单 |
| `route_community_assistant` | 依据情境，导航至具体的社区支持工具路线 |
| `care_handoff_brief` | 生成结构化、可下载的志愿者交接简报 |
| `full_volunteer_workflow` | **推荐演示**：一键触发完整流程（接话卡+循证资料+干预方案） |
| `generate_wechat_draft` | **独家亮点**：将群聊精彩内容一键转化为排版精美的公众号暖文 |

---

### 🌟 交互与落地亮点（区别于纯文字体验）
1. **📈 心理负荷可视化图**：压力测评不仅输出文字结论，还会同步生成**柱状图**，直观展现失眠、疲惫、焦虑等维度的压力峰值。
2. **📥 交接简报一键下载**：生成的志愿者交接简报支持 **Markdown 排版预览**和 **纯文本复制**，并提供 **`.txt` 文件直接下载**，方便打印或发微信群。
3. **📝 群聊金句转推文**：只需复制群里的一段优质对话，点击按钮，AI 即可将其改写成符合**微信公众号排版风格的治愈文章**，大幅减轻社工宣发负担。

---

### 💻 本地运行指南
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 配置环境变量（创建 `.env` 文件，填入你的 API 密钥）：
   ```text
   LLM_BASE_URL=https://api.stepfun.com/v1
   LLM_API_KEY=你的StepFun大模型API_KEY
   LLM_MODEL=step-3.7-flash
   KNOWS_API_KEY=你的Knows医学API_KEY
   KNOWS_BASE_URL=https://api.nullht.com
   ```
3. 启动应用程序：
   ```bash
   python app.py
   ```

---

### 📤 平台提交说明（魔搭/飞书）
*   **MCP 服务端提交**: [https://modelscope.cn/mcp/servers/create](https://modelscope.cn/mcp/servers/create)
*   **Studio 空间部署**: [https://modelscope.cn/studios/create](https://modelscope.cn/studios/create)
*   **飞书正式表单提交**: [https://uei55ql5ok.feishu.cn/share/base/form/shrcn8RVcW8oVxgyRxQP15Tkgbh](https://uei55ql5ok.feishu.cn/share/base/form/shrcn8RVcW8oVxgyRxQP15Tkgbh)

*(注：在飞书表单的“项目描述”栏中，直接粘贴本介绍即可；在“代码仓库”中提交你的 GitHub 或魔搭 ModelScope 代码链接。)*

---

### 📜 开源许可
本项目采用 **MIT License** 开源协议，欢迎广大开发者、安宁疗护志愿者共同参与改进。

---

