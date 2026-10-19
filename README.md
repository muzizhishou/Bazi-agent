# 八字命理 AI Agent 项目

基于 LangChain 和向量检索的智能八字分析系统，结合传统命理学知识与现代 AI 技术，为用户提供个性化的命理解读。

## 项目简介

本项目使用 FastAPI 构建后端服务，通过 OpenAI GPT-4 和向量数据库 Chroma 实现智能八字分析。系统能够根据用户的出生年月日时自动计算四柱八字，并生成包含人格原型、性格特质等信息的详细分析报告。

### 核心特性

- **精确八字计算**：基于天干地支和节气的专业八字推算
- **AI 驱动分析**：利用 LangChain Agent 和 RAG 技术生成个性化解读
- **向量知识库**：使用 HuggingFace Embeddings 和 Chroma 存储命理知识
- **智能缓存**：内存缓存机制提升响应速度
- **结果校验**：多次重试机制确保输出准确性
- **RESTful API**：简洁的 HTTP 接口便于前端集成

## 技术栈

- **后端框架**：FastAPI
- **AI 框架**：LangChain
- **LLM 模型**：OpenAI GPT-4
- **向量数据库**：Chroma
- **嵌入模型**：HuggingFace sentence-transformers
- **Python 版本**：3.8+

## 项目结构

```
bazi_core_project/
├── server.py              # FastAPI 服务主文件
├── Bazi_agent.py          # LangChain Agent 核心逻辑
├── Bazi_calculate.py      # 八字计算工具
├── knowledge.txt          # 命理知识库文本
├── test_backend.py        # 后端接口测试
├── START_SERVER.md        # 启动与测试指南
└── README.md              # 项目说明文档
```

## 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install fastapi uvicorn langchain langchain-openai langchain-chroma langchain-huggingface pydantic

# 设置 OpenAI API Key
export OPENAI_API_KEY="your-api-key-here"
```

### 2. 启动服务

```bash
cd "d:\MyPython\Bazi agent\bazi_core_project"
python -m uvicorn server:app --port 8000
```

首次启动会自动构建向量库，需要 1-2 分钟。看到 "Application startup complete" 后即可使用。

### 3. 测试接口

**正常请求示例**（PowerShell）：

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/analyze `
  -ContentType 'application/json' `
  -Body '{"year":2006,"month":7,"day":21,"hour":7}'
```

**cURL 示例**：

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"year":2006,"month":7,"day":21,"hour":7}'
```

### 4. 响应格式

```json
{
  "year_pillar": "丙戌",
  "month_pillar": "乙未",
  "day_pillar": "甲寅",
  "hour_pillar": "戊辰",
  "archetype_title": "拔地苍木·滋养成长者",
  "shareable_tagline": "林木向阳而生，扎根深处自成风景",
  "personality_summary": "你如同春日里的参天大树...",
  "traits": [
    "生命力旺盛，执行力强",
    "善于规划，注重长期价值",
    "需要警惕过度刚强"
  ]
}
```

## API 文档

### POST /api/analyze

分析用户八字并返回详细解读。

**请求参数**：

| 字段 | 类型 | 必填 | 范围 | 说明 |
|------|------|------|------|------|
| year | int | 是 | 1900-2100 | 出生年份 |
| month | int | 是 | 1-12 | 出生月份 |
| day | int | 是 | 1-31 | 出生日期 |
| hour | int | 是 | 0-23 | 出生小时（24小时制） |

**响应字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| year_pillar | string | 年柱（天干地支） |
| month_pillar | string | 月柱 |
| day_pillar | string | 日柱 |
| hour_pillar | string | 时柱 |
| archetype_title | string | 人格原型称号 |
| shareable_tagline | string | 可分享的一句话标语 |
| personality_summary | string | 性格总结（200-300字） |
| traits | array | 特质列表（3-5条） |

**错误响应**：

- `422 Unprocessable Entity`：无效日期
- `502 Bad Gateway`：AI 生成失败或校验未通过

## 核心机制

### 八字计算

使用 `Bazi_calculate.py` 实现：
- 支持 1900-2100 年范围
- 节气精确计算（月柱依据节气而非公历月份）
- 时辰自动转换为时柱

### AI Agent 工作流

1. **工具准备**：提供八字五行信息查询工具
2. **知识检索**：从向量库中检索相关命理知识
3. **分析生成**：Agent 调用工具并结合知识生成结构化输出
4. **结果校验**：验证四柱准确性和称号一致性
5. **重试机制**：最多重试 2 次确保质量

### 向量知识库

- **来源**：`knowledge.txt` 文件
- **嵌入模型**：`sentence-transformers/all-MiniLM-L6-v2`
- **存储位置**：`./chroma_db`
- **自动重建**：首次启动或知识文件更新后自动重建

## 注意事项

⚠️ **重要提示**：

- 不要使用 `--reload` 参数启动，会导致向量库重复构建
- Agent 调用通常需要 10-40 秒，请耐心等待
- 建议生产环境配置更大的缓存或持久化存储
- OpenAI API Key 需要有 GPT-4 访问权限

## 开发测试

运行后端测试脚本：

```bash
python test_backend.py
```

测试覆盖：
- 正常八字分析请求
- 缓存机制验证
- 无效日期处理
- 错误场景处理

## 扩展方向

- [ ] 添加前端界面（已有前端项目可集成）
- [ ] 支持更多命理分析维度（大运、流年等）
- [ ] 实现用户系统和历史记录
- [ ] 优化向量检索策略
- [ ] 支持多种 LLM 后端

## 许可证

本项目仅供学习交流使用。

## 联系方式

如有问题或建议，请通过项目 Issue 反馈。
