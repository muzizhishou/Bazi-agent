const pptxgen = require('pptxgenjs');
const fs = require('fs');

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Paper Review';
pres.title = 'CNN-Based Painting Authentication';

// Color palette - Ocean Gradient theme for academic/technical content
const colors = {
  primary: '065A82',    // deep blue
  secondary: '1C7293',  // teal
  accent: '21295C',     // midnight
  light: 'F2F2F2',      // off-white
  white: 'FFFFFF',
  text: '212121'
};

// Slide 1: Title Slide
let slide = pres.addSlide();
slide.background = { color: colors.primary };

slide.addText('基于CNN与滑窗特征提取的\n绘画认证研究', {
  x: 0.5, y: 1.5, w: 9, h: 1.5,
  fontSize: 40, bold: true, color: colors.white,
  align: 'center', valign: 'middle'
});

slide.addText('Painting Authentication Using CNNs and\nSliding Window Feature Extraction', {
  x: 0.5, y: 3.2, w: 9, h: 0.8,
  fontSize: 20, color: colors.light,
  align: 'center', valign: 'middle', italic: true
});

slide.addText('Ruiz de Miras et al., 2026\nFrontiers in Artificial Intelligence', {
  x: 0.5, y: 4.3, w: 9, h: 0.6,
  fontSize: 14, color: colors.light,
  align: 'center'
});

// Slide 2: Research Background
slide = pres.addSlide();
slide.background = { color: colors.white };

slide.addText('选题背景', {
  x: 0.5, y: 0.4, w: 9, h: 0.6,
  fontSize: 36, bold: true, color: colors.primary
});

const bg1 = [
  { text: '艺术品认证的复杂性', options: { bullet: true, breakLine: true } },
  { text: '需整合历史专业知识、科学分析与计算技术', options: { bullet: { indent: 30 }, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: '深度学习在艺术分析中的应用', options: { bullet: true, breakLine: true } },
  { text: 'CNN可通过图像直接学习复杂视觉模式', options: { bullet: { indent: 30 }, breakLine: true } },
  { text: '在多项研究中展现高准确率', options: { bullet: { indent: 30 }, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: '核心挑战：数据稀缺性', options: { bullet: true, breakLine: true } },
  { text: '传统深度学习需要数百或数千张标注图像', options: { bullet: { indent: 30 }, breakLine: true } },
  { text: '单幅画作认证时，真实训练样本极为有限', options: { bullet: { indent: 30 }, breakLine: true } },
  { text: '标准深度模型易过拟合，泛化能力差', options: { bullet: { indent: 30 } } }
];

slide.addText(bg1, {
  x: 0.7, y: 1.3, w: 8.6, h: 3.8,
  fontSize: 16, color: colors.text,
  lineSpacing: 20
});

// Slide 3: Literature Search Strategy
slide = pres.addSlide();
slide.background = { color: colors.white };

slide.addText('文献检索策略', {
  x: 0.5, y: 0.4, w: 9, h: 0.6,
  fontSize: 36, bold: true, color: colors.primary
});

slide.addShape(pres.ShapeType.roundRect, {
  x: 0.7, y: 1.3, w: 4, h: 1.2,
  fill: { color: colors.secondary, transparency: 90 },
  line: { color: colors.secondary, width: 2 },
  rectRadius: 0.1
});

slide.addText('检索关键词', {
  x: 0.9, y: 1.4, w: 3.6, h: 0.3,
  fontSize: 18, bold: true, color: colors.primary
});

slide.addText('• authentication\n• CNNs\n• painting classification\n• data scarcity', {
  x: 0.9, y: 1.8, w: 3.6, h: 0.6,
  fontSize: 14, color: colors.text
});

slide.addShape(pres.ShapeType.roundRect, {
  x: 5.3, y: 1.3, w: 4, h: 1.2,
  fill: { color: colors.accent, transparency: 90 },
  line: { color: colors.accent, width: 2 },
  rectRadius: 0.1
});

slide.addText('研究焦点', {
  x: 5.5, y: 1.4, w: 3.6, h: 0.3,
  fontSize: 18, bold: true, color: colors.primary
});

slide.addText('CNN在艺术品认证中的应用\n迁移学习与预训练模型\n数据稀缺场景下的解决方案', {
  x: 5.5, y: 1.8, w: 3.6, h: 0.6,
  fontSize: 14, color: colors.text
});

const lit = [
  { text: '相关重要文献', options: { bullet: false, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: 'Elgammal et al. (2018): 艺术史风格演变的深度学习框架', options: { bullet: true, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: 'Ugail et al. (2023): 迁移学习在拉斐尔画作归属中的有效性', options: { bullet: true, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: 'Schaerf et al. (2024): Vision Transformers在梵高画作认证中的应用', options: { bullet: true } }
];

slide.addText(lit, {
  x: 0.7, y: 2.8, w: 8.6, h: 2.3,
  fontSize: 16, color: colors.text,
  lineSpacing: 18
});

// Slide 4: Authors and Institutions
slide = pres.addSlide();
slide.background = { color: colors.white };

slide.addText('作者、机构、资助背景', {
  x: 0.5, y: 0.4, w: 9, h: 0.6,
  fontSize: 36, bold: true, color: colors.primary
});

slide.addShape(pres.ShapeType.ellipse, {
  x: 0.9, y: 1.4, w: 0.15, h: 0.15,
  fill: { color: colors.secondary }
});

slide.addText('作者团队', {
  x: 1.2, y: 1.35, w: 7.8, h: 0.25,
  fontSize: 20, bold: true, color: colors.primary
});

slide.addText('Juan Ruiz de Miras (通讯作者)\nJosé Luis Vélchez\nMaría José Gacto\nDomingo Martín', {
  x: 1.2, y: 1.7, w: 7.8, h: 0.8,
  fontSize: 16, color: colors.text, lineSpacing: 22
});

slide.addShape(pres.ShapeType.ellipse, {
  x: 0.9, y: 2.7, w: 0.15, h: 0.15,
  fill: { color: colors.secondary }
});

slide.addText('研究机构', {
  x: 1.2, y: 2.65, w: 7.8, h: 0.25,
  fontSize: 20, bold: true, color: colors.primary
});

slide.addText('University of Granada, Spain\n• 软件工程系\n• 分析化学系\n• Biosanitary Research Institute (ibs.GRANADA)\n• 数据科学与计算智能研究所 (DaSCI)', {
  x: 1.2, y: 3.0, w: 7.8, h: 1.0,
  fontSize: 16, color: colors.text, lineSpacing: 20
});

slide.addShape(pres.ShapeType.ellipse, {
  x: 0.9, y: 4.2, w: 0.15, h: 0.15,
  fill: { color: colors.secondary }
});

slide.addText('资助来源', {
  x: 1.2, y: 4.15, w: 7.8, h: 0.25,
  fontSize: 20, bold: true, color: colors.primary
});

slide.addText('西班牙科学创新部 (PID2024161348OB-I00)\nCarlos III健康研究所 (PI23/00129)', {
  x: 1.2, y: 4.5, w: 7.8, h: 0.6,
  fontSize: 16, color: colors.text, lineSpacing: 22
});

// Slide 5: Research Question with Painting Image
slide = pres.addSlide();
slide.background = { color: colors.white };

slide.addText('研究问题', {
  x: 0.5, y: 0.4, w: 9, h: 0.6,
  fontSize: 36, bold: true, color: colors.primary
});

// Add the Holy Family painting image
const imageData = fs.readFileSync('holy_family_painting.png');
const imageBase64 = imageData.toString('base64');
slide.addImage({
  data: 'image/png;base64,' + imageBase64,
  x: 0.7, y: 1.2, w: 4.5, h: 3.5,
  sizing: { type: 'contain' }
});

slide.addShape(pres.ShapeType.roundRect, {
  x: 5.4, y: 1.2, w: 4.0, h: 1.5,
  fill: { color: colors.primary, transparency: 95 },
  line: { color: colors.primary, width: 3 },
  rectRadius: 0.15
});

slide.addText('研究对象', {
  x: 5.6, y: 1.35, w: 3.6, h: 0.25,
  fontSize: 20, bold: true, color: colors.primary
});

slide.addText('《圣家族》画作\n归属于Paolo Veronese\n（可能为本人、工作室或追随者）', {
  x: 5.6, y: 1.7, w: 3.6, h: 0.8,
  fontSize: 15, color: colors.text, lineSpacing: 20
});

slide.addShape(pres.ShapeType.roundRect, {
  x: 5.4, y: 2.9, w: 4.0, h: 1.8,
  fill: { color: colors.secondary, transparency: 92 },
  line: { color: colors.secondary, width: 2 },
  rectRadius: 0.15
});

slide.addText('核心挑战', {
  x: 5.6, y: 3.05, w: 3.6, h: 0.25,
  fontSize: 20, bold: true, color: colors.primary
});

const rq2 = [
  { text: '仅6幅训练画作（极度数据稀缺）', options: { bullet: true, breakLine: true } },
  { text: '限定同一主题（圣家族）', options: { bullet: true, breakLine: true } },
  { text: '聚焦风格特征而非图像内容', options: { bullet: true, breakLine: true } },
  { text: '区分大师、工作室与追随者', options: { bullet: true } }
];

slide.addText(rq2, {
  x: 5.6, y: 3.4, w: 3.6, h: 1.1,
  fontSize: 14, color: colors.text, lineSpacing: 16
});

// Slide 6: Methodology - Complete Pipeline with Image
slide = pres.addSlide();
slide.background = { color: colors.white };

slide.addText('研究方法：完整流程', {
  x: 0.5, y: 0.4, w: 9, h: 0.6,
  fontSize: 36, bold: true, color: colors.primary
});

// Step 1: Original painting
slide.addText('① 原始画作 640×640', {
  x: 0.7, y: 1.2, w: 2.2, h: 0.25,
  fontSize: 13, bold: true, color: colors.primary
});

slide.addShape(pres.ShapeType.rect, {
  x: 0.7, y: 1.5, w: 2.2, h: 1.6,
  fill: { color: colors.light }
});

slide.addText('待认证的圣家族画作\n• 裁剪为正方形\n• 归一化尺寸', {
  x: 0.8, y: 1.7, w: 2.0, h: 1.2,
  fontSize: 12, color: colors.text, lineSpacing: 18
});

// Arrow
slide.addShape(pres.ShapeType.rightArrow, {
  x: 3.0, y: 2.2, w: 0.4, h: 0.25,
  fill: { color: colors.secondary }
});

// Step 2: Multi-channel extraction
slide.addText('② 多通道提取', {
  x: 3.5, y: 1.2, w: 2.2, h: 0.25,
  fontSize: 13, bold: true, color: colors.primary
});

slide.addShape(pres.ShapeType.rect, {
  x: 3.5, y: 1.5, w: 2.2, h: 1.6,
  fill: { color: colors.secondary, transparency: 95 }
});

slide.addText('RGB (3通道)\n+\n灰度 (1通道)\n+\nCanny边缘 (1通道)', {
  x: 3.6, y: 1.65, w: 2.0, h: 1.3,
  fontSize: 11, color: colors.text, lineSpacing: 16, align: 'center'
});

// Arrow
slide.addShape(pres.ShapeType.rightArrow, {
  x: 5.8, y: 2.2, w: 0.4, h: 0.25,
  fill: { color: colors.secondary }
});

// Step 3: Sliding window
slide.addText('③ 滑窗分块', {
  x: 6.3, y: 1.2, w: 2.2, h: 0.25,
  fontSize: 13, bold: true, color: colors.primary
});

slide.addShape(pres.ShapeType.rect, {
  x: 6.3, y: 1.5, w: 2.2, h: 1.6,
  fill: { color: colors.accent, transparency: 95 }
});

slide.addText('64×64窗口\n65%重叠\n→ 729个分块\n5通道输入', {
  x: 6.4, y: 1.65, w: 2.0, h: 1.3,
  fontSize: 11, color: colors.text, lineSpacing: 16
});

// Step 4: CNN Architecture
slide.addText('④ 浅层CNN架构', {
  x: 0.7, y: 3.4, w: 4.0, h: 0.3,
  fontSize: 15, bold: true, color: colors.primary
});

slide.addShape(pres.ShapeType.rect, {
  x: 0.7, y: 3.75, w: 4.0, h: 1.1,
  fill: { color: colors.light }
});

const cnn = [
  { text: '卷积块1 (16滤波器) + 池化', options: { bullet: true, breakLine: true } },
  { text: '卷积块2 (32滤波器) + 池化 + Dropout(0.5)', options: { bullet: true, breakLine: true } },
  { text: '全连接层 → Softmax输出', options: { bullet: true } }
];

slide.addText(cnn, {
  x: 0.85, y: 3.9, w: 3.7, h: 0.8,
  fontSize: 11, color: colors.text, lineSpacing: 14
});

// Step 5: Training
slide.addText('⑤ 训练策略', {
  x: 4.9, y: 3.4, w: 4.4, h: 0.3,
  fontSize: 15, bold: true, color: colors.primary
});

slide.addShape(pres.ShapeType.rect, {
  x: 4.9, y: 3.75, w: 4.4, h: 1.1,
  fill: { color: colors.light }
});

const train = [
  { text: '6折留一法（绘画级验证，防止数据泄露）', options: { bullet: true, breakLine: true } },
  { text: 'Adam优化器 + L2正则化 + 早停', options: { bullet: true, breakLine: true } },
  { text: '数据增强：6幅画 → 4,374个训练样本', options: { bullet: true } }
];

slide.addText(train, {
  x: 5.05, y: 3.9, w: 4.1, h: 0.8,
  fontSize: 11, color: colors.text, lineSpacing: 14
});

// Slide 7: Key Results
slide = pres.addSlide();
slide.background = { color: colors.white };

slide.addText('核心结果', {
  x: 0.5, y: 0.4, w: 9, h: 0.6,
  fontSize: 36, bold: true, color: colors.primary
});

// Stat callouts
slide.addShape(pres.ShapeType.roundRect, {
  x: 0.7, y: 1.2, w: 2.0, h: 1.1,
  fill: { color: colors.primary },
  rectRadius: 0.1
});

slide.addText('94.51%', {
  x: 0.7, y: 1.4, w: 2.0, h: 0.5,
  fontSize: 32, bold: true, color: colors.white, align: 'center'
});

slide.addText('准确率', {
  x: 0.7, y: 1.95, w: 2.0, h: 0.25,
  fontSize: 14, color: colors.white, align: 'center'
});

slide.addShape(pres.ShapeType.roundRect, {
  x: 2.9, y: 1.2, w: 2.0, h: 1.1,
  fill: { color: colors.secondary },
  rectRadius: 0.1
});

slide.addText('0.99', {
  x: 2.9, y: 1.4, w: 2.0, h: 0.5,
  fontSize: 32, bold: true, color: colors.white, align: 'center'
});

slide.addText('AUC-ROC', {
  x: 2.9, y: 1.95, w: 2.0, h: 0.25,
  fontSize: 14, color: colors.white, align: 'center'
});

slide.addShape(pres.ShapeType.roundRect, {
  x: 5.1, y: 1.2, w: 2.0, h: 1.1,
  fill: { color: colors.accent },
  rectRadius: 0.1
});

slide.addText('0.87', {
  x: 5.1, y: 1.4, w: 2.0, h: 0.5,
  fontSize: 32, bold: true, color: colors.white, align: 'center'
});

slide.addText('Kappa系数', {
  x: 5.1, y: 1.95, w: 2.0, h: 0.25,
  fontSize: 14, color: colors.white, align: 'center'
});

slide.addShape(pres.ShapeType.roundRect, {
  x: 7.3, y: 1.2, w: 2.0, h: 1.1,
  fill: { color: colors.primary, transparency: 30 },
  rectRadius: 0.1
});

slide.addText('97.15%', {
  x: 7.3, y: 1.4, w: 2.0, h: 0.5,
  fontSize: 32, bold: true, color: colors.primary, align: 'center'
});

slide.addText('灵敏度', {
  x: 7.3, y: 1.95, w: 2.0, h: 0.25,
  fontSize: 14, color: colors.text, align: 'center'
});

const res1 = [
  { text: '真品Veronese画作：80-99%概率，连续高概率区域', options: { bullet: true, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: '非Veronese复制品：12-37%概率，破碎化分布', options: { bullet: true, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: '存疑画作：61%概率（中间值 → 工作室/部分真迹可能）', options: { bullet: true, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: '泛化性能超越MobileNetV2：浅层模型在测试集上建立清晰决策边界', options: { bullet: true } }
];

slide.addText(res1, {
  x: 0.7, y: 2.6, w: 8.6, h: 2.3,
  fontSize: 15, color: colors.text, lineSpacing: 14
});

// Slide 8: Strengths and Limitations
slide = pres.addSlide();
slide.background = { color: colors.white };

slide.addText('文章优缺点评述', {
  x: 0.5, y: 0.4, w: 9, h: 0.6,
  fontSize: 36, bold: true, color: colors.primary
});

slide.addShape(pres.ShapeType.rect, {
  x: 0.7, y: 1.2, w: 4.2, h: 3.7,
  fill: { color: colors.secondary, transparency: 95 }
});

slide.addText('主要优点', {
  x: 0.9, y: 1.4, w: 3.8, h: 0.3,
  fontSize: 20, bold: true, color: colors.primary
});

const str = [
  { text: '创新的分块策略有效解决极端数据稀缺问题', options: { bullet: true, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: '绘画级验证严格防止数据泄露', options: { bullet: true, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: '概率热力图提供可解释性', options: { bullet: true, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: '多通道设计捕获互补特征', options: { bullet: true, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: '定制架构优于通用预训练模型', options: { bullet: true } }
];

slide.addText(str, {
  x: 0.9, y: 1.8, w: 3.8, h: 2.9,
  fontSize: 14, color: colors.text, lineSpacing: 13
});

slide.addShape(pres.ShapeType.rect, {
  x: 5.1, y: 1.2, w: 4.2, h: 3.7,
  fill: { color: colors.accent, transparency: 95 }
});

slide.addText('局限性', {
  x: 5.3, y: 1.4, w: 3.8, h: 0.3,
  fontSize: 20, bold: true, color: colors.primary
});

const lim = [
  { text: '仅限于圣家族主题，图像学特异性', options: { bullet: true, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: '二分类框架，无法区分工作室/追随者', options: { bullet: true, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: '分块方法丧失全局构图信息', options: { bullet: true, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: '提供概率证据而非确定性归属', options: { bullet: true, breakLine: true } },
  { text: '', options: { breakLine: true } },
  { text: '需结合历史、技术、来源分析', options: { bullet: true } }
];

slide.addText(lim, {
  x: 5.3, y: 1.8, w: 3.8, h: 2.9,
  fontSize: 14, color: colors.text, lineSpacing: 13
});

// Slide 9: Personal Insights
slide = pres.addSlide();
slide.background = { color: colors.primary };

slide.addText('个人启发', {
  x: 0.5, y: 0.6, w: 9, h: 0.6,
  fontSize: 36, bold: true, color: colors.white
});

slide.addShape(pres.ShapeType.ellipse, {
  x: 1.0, y: 1.6, w: 0.2, h: 0.2,
  fill: { color: colors.white }
});

slide.addText('定制浅层模型在特定领域可超越大型预训练模型', {
  x: 1.4, y: 1.55, w: 7.6, h: 0.3,
  fontSize: 17, color: colors.white
});

slide.addText('小数据场景下，领域特化比模型规模更重要', {
  x: 1.4, y: 1.9, w: 7.6, h: 0.25,
  fontSize: 14, color: colors.light, italic: true
});

slide.addShape(pres.ShapeType.ellipse, {
  x: 1.0, y: 2.4, w: 0.2, h: 0.2,
  fill: { color: colors.white }
});

slide.addText('智能分块数据增强的威力', {
  x: 1.4, y: 2.35, w: 7.6, h: 0.3,
  fontSize: 17, color: colors.white
});

slide.addText('从6幅画扩展到4374个有意义的样本，关键在于保留局部特征连续性', {
  x: 1.4, y: 2.7, w: 7.6, h: 0.25,
  fontSize: 14, color: colors.light, italic: true
});

slide.addShape(pres.ShapeType.ellipse, {
  x: 1.0, y: 3.2, w: 0.2, h: 0.2,
  fill: { color: colors.white }
});

slide.addText('领域约束帮助聚焦风格而非内容', {
  x: 1.4, y: 3.15, w: 7.6, h: 0.3,
  fontSize: 17, color: colors.white
});

slide.addText('限定同一主题，迫使模型学习执行技巧而非语义构图', {
  x: 1.4, y: 3.5, w: 7.6, h: 0.25,
  fontSize: 14, color: colors.light, italic: true
});

slide.addShape(pres.ShapeType.ellipse, {
  x: 1.0, y: 4.0, w: 0.2, h: 0.2,
  fill: { color: colors.white }
});

slide.addText('可视化增强人机协作', {
  x: 1.4, y: 3.95, w: 7.6, h: 0.3,
  fontSize: 17, color: colors.white
});

slide.addText('热力图使算法决策透明化，为专家判断提供量化依据', {
  x: 1.4, y: 4.3, w: 7.6, h: 0.25,
  fontSize: 14, color: colors.light, italic: true
});

// Save presentation
pres.writeFile({ fileName: 'painting_authentication_presentation.pptx' });
console.log('Presentation created: painting_authentication_presentation.pptx');
