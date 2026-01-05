# Anki Theme - 极简 UI 皮肤

一款干净、现代的 Anki 主题插件，将默认界面变成精致的极简设计，同时支持浅色和深色模式。

![Anki](https://img.shields.io/badge/Anki-2.1+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ 功能特点

- **现代极简设计** — 扁平化 UI，配合细腻的阴影和流畅的过渡效果
- **浅色 & 深色模式** — 自动适配 Anki 原生主题设置
- **牌组浏览器重设计** — 卡片式牌组行，带有彩色计数标签（新卡/学习中/待复习）
- **统一风格** — 牌组浏览器、复习界面和概览页面保持一致的视觉效果
- **原生 Qt 菜单样式** — 右键菜单（齿轮图标）与整体主题匹配
- **紧凑布局** — 优化间距，提高信息密度

## 📸 截图预览

![浅色模式截图](pic_light.webp)
![深色模式截图](pic_dark.webp)

## 🚀 安装方法

### 手动安装

### 从 AnkiWeb 安装

*即将上线*

## 🎨 设计系统

### 配色选项

颜色分别为 `light`（浅色）和 `dark`（深色）模式定义，使用十六进制颜色代码：

```json
{
    "light": {
        "background": "#f6f6f7",
        "surface": "#ffffff",
        "accent": "#4f6ef7",
        "new": "#3b82f6",
        "learn": "#f59e0b",
        "due": "#10b981"
    },
    "dark": {
        "background": "#1c1c1f",
        "surface": "#242427",
        "accent": "#7aa2ff",
        "new": "#7aa2ff",
        "learn": "#ffcc66",
        "due": "#57d39a"
    }
}
```

详细配置请参阅 [`config.md`](config.md)。

> **提示：** 修改配置后，需要重启 Anki 才能生效。

## 🛠️ 技术细节

### 样式化组件

- **牌组浏览器** — 表格布局、牌组行、计数标签、齿轮图标
- **Qt 菜单** — 原生弹出菜单（齿轮图标右键菜单）

### 工作原理

1. 通过 `webview_will_set_content` 钩子向 Anki 的 webview 注入 CSS
2. 应用 Qt 样式表 (QSS) 来美化原生 UI 元素
3. 监听主题变化，动态切换浅色/深色模式

### 兼容性

- Anki 2.1+（已在 2.1.60+ 上测试）
- 与大多数其他插件兼容
- 可与 Review Heatmap 等插件共存

## 📄 开源许可

MIT 许可证 — 可自由修改和分发。

## 🙏 致谢

- 灵感来源于现代 UI 设计原则
- 为 Anki 社区而构建

---

**享受更清爽的 Anki 体验！** ⚡
