# 启动服务器和测试指南

## 1. 启动服务器

在命令行中运行：

```bash
cd "d:\MyPython\Bazi agent"
python -m uvicorn server:app --port 8000
```

等待看到 "Application startup complete" 消息。

## 2. 测试后端接口（在另一个命令行窗口）

### 测试1：正常请求
```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/analyze -ContentType 'application/json' -Body '{"year":2006,"month":7,"day":21,"hour":7}'
```

预期结果：返回包含8个字段的JSON（year_pillar, month_pillar, day_pillar, hour_pillar, archetype_title, shareable_tagline, personality_summary, traits）

### 测试2：验证缓存（重复请求）
再次运行测试1的命令，应该立即返回相同结果

### 测试3：无效日期
```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/analyze -ContentType 'application/json' -Body '{"year":2006,"month":2,"day":30,"hour":7}'
```

预期结果：返回422错误，中文提示"2006年2月30日不是有效日期"

## 3. 访问前端

打开浏览器访问：http://localhost:8000/

当前会看到结果页（使用mock数据）。

## 注意事项

- 第一次启动会重建向量库，需要1-2分钟
- Agent调用可能需要10-40秒
- 不要使用 `--reload` 参数，会重复触发向量库重建
