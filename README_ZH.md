# 学术模板 (Academic Template)

一个以配置驱动的学术主页模板，提供动态 Section、模板注册表、插件系统和多语言支持。

[English Documentation](README.md)

## ✨ 特性概览
- 🎯 **配置优先**：通过 JSON 即可维护导航、Section 以及内容类型。
- 🧩 **模板注册表**：在 `static/js/templates.js` 中扩展自定义渲染逻辑。
- 🔌 **插件系统**：默认提供搜索/排序插件，可灵活扩展 (`static/js/plugins.js`)。
- 🌍 **多语言**：不同语言的数据放在各自目录，语言标签统一由 `meta.json` 管理。
- 📱 **响应式**：基于 Bulma 框架，对桌面、平板、手机均做了优化。
- 🎨 **主题/背景**：支持全局主题色与按页面配置的背景图（含暗色模式）。

## 🚀 快速上手

### 1. 克隆仓库
```bash
git clone <your-repo-url>
cd academic-template
```

### 2. 配置全局信息 (`data/meta.json`)
核心设置都集中在 `meta.json`，示例：
```json
{
  "defaultLanguage": "en",
  "availableLanguages": ["en", "zh", "jp"],
  "languageLabels": {
    "en": "English",
    "zh": "中文",
    "jp": "日本語"
  },
  "navbar": {"showLanguageDropdown": true},
  "home": {
    "showHero": true,
    "avatar": "./media/personal.jpg"
  },
  "backgrounds": {
    "default": {
      "light": "./media/occupacy.jpg",
      "dark": "./media/occupacy_dark.jpg"
    }
  },
  "itemTypes": {
    "news": {
      "requiredKeys": ["date", "content"],
      "template": "list-inline"
    },
    "publication": {
      "requiredKeys": ["title", "conference", "authors", "description", "links"],
      "template": "paper-card"
    }
  },
  "sections": [
    {
      "id": "news",
      "enabled": true,
      "itemType": "news",
      "dataSource": "news",
      "background": "default",
      "singlePage": {"enabled": true},
      "multiPage": {"enabled": true, "plugins": ["search"]}
    }
  ],
  "socials": [{"icon": "fab fa-github", "url": "https://github.com/your-name"}]
}
```
要点：
- `backgrounds` 中定义背景图（light/dark）。Section 的 `background` 字段引用该 key，未配置时自动使用 `default`。
- 小贴士：主页会优先使用 `backgrounds.home`，若未配置则回退到 `backgrounds.default`。
- `itemTypes` 声明字段约束及模板，避免内容缺字段。

### 3. 准备多语言数据
每种语言一个目录，例如 `data/zh/`，包含：

- `web_content.json`：仅保留首页文案（标题、副标题、页脚等）。
- `<section>.json`：Section 自己维护导航名、标题以及数据数组。

示例 `data/zh/news.json`：
```json
{
  "nav_label": "新闻",
  "title": "🔥 新闻",
  "news": [
    {"date": "2025.01.01", "content": "这是新闻占位内容。"}
  ]
}
```

示例 `data/zh/about.json`：
```json
{
  "nav_label": "关于我",
  "title": "🎄 关于我",
  "texts": [
    "<strong>关于我占位符：</strong>这里介绍你自己、学校/机构以及研究方向。",
    "可以追加一段话，写兴趣、目标或联系方式。"
  ]
}
```

所有 Section 文件均遵循：`nav_label`、`title`、以及与 `dataSource` 同名的数组（或 `items`）。

### 4. 启动本地静态服务器
```bash
python3 -m http.server 8000
# 或者
npx serve .
```
访问 `http://localhost:8000`（单页模式）或 `http://localhost:8000/multipage_index.html`（多页模式）。

## 📖 配置详情

### `meta.json` 关键字段
- `availableLanguages` / `languageLabels`：决定可切换语言及按钮文字。
- `backgrounds`：定义全局背景资源，支持明暗两套图；Section 引用对应 key。
- `sections`：开关 Section、指定数据源、布局、插件和背景。
- `itemTypes`：指定模板与必填字段；模板在 `static/js/templates.js` 中维护。
- `themes`、`socials`、`home`：控制主题色、社交图标、首页头像/功能。

### Section 数据结构
```json
{
  "nav_label": "导航按钮文本",
  "title": "Section 标题",
  "projects": [ ... ]
}
```
其中 `projects` 与 `meta.sections[*].dataSource` 对应。若某 Section 未提供语言文件，则该 Section 自动隐藏。

### 首页文案 (`web_content.json`)
```json
{
  "navbar_title": "Academic Template",
  "navbar_home": "Home",
  "language": "Language",
  "title": "请在此填写你的主页标题。",
  "subtitle": "这里可以写一句简短介绍或口号。",
  "footer": "Powered by Academic Template"
}
```

## 🔧 扩展指南

### 1. 扩展语言
1. 在 `meta.json` 的 `availableLanguages` 中添加新语言码，并在 `languageLabels` 中填入显示名称。
2. 新建 `data/<lang>/` 目录，拷贝现有语言的 Section JSON 并翻译内容。
3. `web_content.json` 里填写该语言的首页文案。

### 2. 扩展 Section
1. 在 `meta.json.sections` 中添加新的 Section：
```json
{
  "id": "education",
  "enabled": true,
  "itemType": "timeline",
  "dataSource": "education",
  "background": "education",
  "singlePage": {"enabled": true},
  "multiPage": {"enabled": true, "plugins": ["search"]}
}
```
2. 若需要新模板或字段，先在 `itemTypes` 中定义：
```json
"timeline": {
  "requiredKeys": ["date", "title", "org", "description"],
  "template": "timeline"
}
```
3. 在每个语言目录下新增 `education.json`：
```json
{
  "nav_label": "教育经历",
  "title": "🎓 教育",
  "education": [
    {"date": "2020–2024", "title": "本科", "org": "某大学", "description": "你的描述"}
  ]
}
```
4. 需要自定义背景时，在 `data/meta.json.backgrounds` 中增加 `education` 条目（提供 light/dark 图片），并在 section 中引用。
5. 可选：在 `meta.json.emptyStates` 中添加对应 id 的空状态文案。

### 3. 自定义模板 / 插件
- 模板：`static/js/templates.js`，通过 `TemplateRegistry.register(name, renderer)` 注册。
- 插件：`static/js/plugins.js`，使用 `PluginRegistry.register` 注册后，在 `sections[*].multiPage.plugins` 中引用。
- CSS：统一在 `static/css/index.css` 中调整，可根据模板添加自定义 class 进行定制。

## 🧪 开发提示
- 使用支持热刷新或自动重载的静态服务器，提升调试效率。
- `itemTypes` 的 `requiredKeys` 可作为撰写内容的检查清单。
- 如果某语言缺少 Section 数据文件，页面会自动隐藏该 Section，不会报错。
- 修改插件或模板后，记得在多页模式下测试搜索/排序等功能。

## 📁 项目结构
```
├── data/
│   ├── meta.json
│   ├── en/
│   │   ├── web_content.json
│   │   ├── about.json
│   │   ├── news.json
│   │   └── ...
│   ├── zh/
│   └── jp/
├── static/
│   ├── css/index.css
│   ├── js/index.js
│   ├── js/templates.js
│   └── js/plugins.js
├── index.html               # 单页模式入口
└── multipage_index.html     # 多页模式入口
```

## 📝 License
MIT License，自由使用与修改。
