# 八字人格结果页

这是一个"东方版MBTI"的前端展示页面，基于方案A（极简印章系）开发。

## 功能特性

- ✅ 1-2秒加载动画（四柱飞入 + 印章盖下效果）
- ✅ 五行动态配色系统（金/木/水/火/土）
- ✅ 印章式图形符号（每种五行独立的几何图案）
- ✅ 响应式设计（移动端优先）
- ✅ 分享卡片生成功能（可下载为图片）
- ✅ 深色背景 + 极简美学

## 技术栈

- React 18
- Vite
- Tailwind CSS
- html-to-image (分享卡片生成)

## 快速开始

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

## 项目结构

```
bazi-result-frontend/
├── src/
│   ├── components/
│   │   ├── LoadingAnimation.jsx  # 加载动画
│   │   ├── SealSymbol.jsx        # 印章符号
│   │   └── BaziResult.jsx        # 主结果页
│   ├── data/
│   │   └── mockData.js           # Mock数据（五种五行各一组）
│   ├── App.jsx                   # 主应用
│   ├── main.jsx                  # 入口文件
│   └── index.css                 # 全局样式
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## 设计说明

### 方案A：极简印章系

- **背景**: 深灰渐变（#1a1a1a → #2d2d2d）
- **字体**: 思源宋体（称号）+ 苹方（正文）
- **印章符号**: 方形边框 + 五行抽象几何图案
  - 金：锐角三角（象征锋利）
  - 木：生长线条（象征向上生长）
  - 水：流动曲线（象征水的流动）
  - 火：上扬尖角（象征火焰）
  - 土：稳定方块（象征厚重）

### 五行配色

| 五行 | 主色 | 描述 |
|------|------|------|
| 金 | #E8E8E8 | 冷调精致的银白色 |
| 木 | #4A6E58 | 沉稳的墨绿色 |
| 水 | #2C4F7C | 辽阔的深蓝色 |
| 火 | #C45D47 | 克制的赭红色 |
| 土 | #A67C52 | 厚重的驼色 |

## 开发测试

页面底部有五行切换器，可以快速预览不同五行的配色效果。生产环境需要移除此功能。

## 后端接口对接

修改 `src/App.jsx`，将 `mockBaziData` 替换为实际的 API 调用：

```javascript
// 示例
const fetchBaziResult = async (birthInfo) => {
  const response = await fetch('/api/bazi/calculate', {
    method: 'POST',
    body: JSON.stringify(birthInfo)
  });
  return await response.json();
};
```

## 字体说明

项目使用系统字体回退方案：
- 思源宋体（建议通过 CDN 引入或本地安装）
- 苹方（macOS/iOS 系统自带）
- 其他系统会自动回退到默认衬线/无衬线字体

如需引入思源宋体，在 `index.html` 添加：

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap" rel="stylesheet">
```

## License

MIT
