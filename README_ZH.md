# 学术模板 (Academic Template)

一个以配置为核心的学术主页模板，支持多语言内容、统一段落式排版以及插件扩展。

[English Documentation](README.md)

## ✨ 主要特性
- 🎯 **配置驱动**：导航、区块、内容全部写在 JSON 中，日常更新无需改动 HTML。
- 🧱 **统一排版**：除「关于我」外，其余 Section 均使用同一套段落渲染，视觉风格统一。
- 🔌 **插件机制**：默认集成搜索/排序插件，可在 `static/js/plugins.js` 中注册自定义插件。
- 🌍 **多语言**：为每种语言单独维护 `data/<lang>/` 目录，元信息复用。
- 📱 **响应式**：基于 Bulma，针对桌面/平板/手机做了细致适配。
- 🎨 **主题配置**：在 `data/meta.json` 中管理背景、主题色、头像和社交链接。

## 🚀 快速上手
1. **克隆项目并进入目录**
   ```bash
   git clone <your-repo-url>
   cd academic-template
   ```
2. **配置 `data/meta.json`**（全局控制中心），示例：
   ```json
   {
     "defaultLanguage": "en",
     "availableLanguages": ["en", "zh"],
     "languageLabels": {"en": "English", "zh": "中文"},
     "navbar": {"showLanguageDropdown": true},
     "home": {"showHero": true, "avatar": "./media/personal.jpg"},
     "backgrounds": {
       "default": {"light": "./media/occupacy.jpg"}
     },
     "itemTypes": {
       "news": {"requiredKeys": ["date", "content"]},
       "publication": {"requiredKeys": ["title", "conference", "authors", "description", "links"]}
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
     "socials": [{"icon": "fab fa-github", "url": "https://github.com/your-name"}],
     "emptyStates": {"news": "暂无新闻。"}
   }
   ```
3. **准备多语言内容** – 每种语言使用 `data/<lang>/`。 
   - `web_content.json`：仅保存首页文案（标题、副标题、页脚等）。
   - `<section>.json`：名称与 `dataSource` 对应，内含导航标签、标题以及数据数组。

   示例 `data/zh/news.json`：
   ```json
   {
     "nav_label": "新闻",
     "title": "🔥 新闻",
     "news": [
       {"date": "2025.01.01", "content": "这里是新闻占位内容。"}
     ]
   }
   ```

   示例 `data/zh/about.json`：
   ```json
   {
     "nav_label": "关于我",
     "title": "🎄 关于我",
     "texts": [
       "<strong>关于我占位符：</strong>在这里介绍自己、学校/机构以及研究方向。",
       "可以再加一段话，写兴趣、目标或联系信息。"
     ]
   }
   ```
4. **启动静态服务器**
   ```bash
   python3 -m http.server 8000
   # 或
   npx serve .
   ```
   打开 `http://localhost:8000`（单页模式）或 `http://localhost:8000/multipage_index.html`（多页模式）。

## 🧩 数据与渲染模型
### `data/meta.json`
- `availableLanguages` / `languageLabels`：语言下拉菜单及其显示名称。
- `backgrounds`：注册可复用的浅色/深色背景，Section 通过 `background` 引用。
- `sections`：声明所有 Section 的 `id`、数据源、类型、背景以及插件。
- `itemTypes`：可选字段，用于提示内容编辑需要填写的关键字段。
- `emptyStates`：Section 数据为空时显示的占位文案。
- `themes`、`socials`、`home`：主题色、社交链接、首页头像/卡片等设置。

### 语言目录 (`data/<lang>/`)
每个 Section 文件至少包含：
```json
{
  "nav_label": "...",
  "title": "...",
  "<dataSource>": [ ... items ... ]
}
```
其中 `<dataSource>` 必须与 `meta.json.sections[*].dataSource` 对应。若缺少某语言的文件，该 Section 会在该语言下自动隐藏。

### 统一段落渲染
`index.html` 与 `multipage_index.html` 共享同一套渲染函数，依赖常见字段生成段落：
- **news**：`date` + `content`。
- **publication**：`title`、`conference`、可选 `date`、`authors`、`description`、`links`。
- **project**：`title`、`date`、`authors`、`description`、`links`。
- **blog**：`title`、`date`、`content`、`links`。
- **timeline**：`title`、`org`、`date`、`description`。

缺失字段会被自动忽略；若数组为空，则展示 `emptyStates` 中配置的提示语。

### 背景图小技巧
1. 将图片放入 `media/`（或任意静态资源目录）。
2. 在 `backgrounds` 中登记 `light`/`dark` 路径。
3. 在 Section 中引用该 key。若未指定，首页会按 `backgrounds.home` → `backgrounds.default` 的顺序回退。

## 🔧 扩展指南
### 新增语言
1. 在 `availableLanguages` 中加入语言码，并在 `languageLabels` 增加显示名称。
2. 新建 `data/<lang>/` 目录，准备该语言的 `web_content.json` 与各 Section 数据。
3. 如有需要，提供对应的本地化媒体资源。

### 新增 Section
1. 在 `meta.json.sections` 中描述新 Section，并在 `emptyStates` 中写好空状态文案（可选）。
2. 在各语言目录创建对应的 `<dataSource>.json` 文件。
3. 如需新增字段或特殊展示，请修改 `index.html` / `multipage_index.html` 中的 `renderEntryIntoBlock`。

### 自定义排版与插件
- Section 的 HTML 结构集中在 `renderEntryIntoBlock` 及其辅助函数，可直接调整。
- 插件通过 `static/js/plugins.js` 的 `PluginRegistry.register` 注册，再在 `multiPage.plugins` 中引用。
- 样式统一位于 `static/css/index.css`，段落使用 `.text-homepage-1` 与 `.section-text-block`。

## 🧪 开发提示
- 使用带热更新的静态服务器能显著提升调试效率。
- `itemTypes.requiredKeys` 可作为内容提交前的自检清单。
- 多页模式会触发搜索/排序等插件，改动后建议同时验证单页和多页。
- 若某语言暂未提供对应 Section 数据，页面会自动隐藏该 Section，便于分批上架翻译。

