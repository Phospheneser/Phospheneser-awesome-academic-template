# Academic Template

A configuration-first academic homepage template with dynamic sections, template registry, and plugin support.

[中文文档](README_ZH.md)

## ✨ Features

- 🎯 **Configuration-Driven** – Manage navigation, sections, and content types via JSON files.
- 🧩 **Template Registry** – Extend rendering logic with custom templates (`static/js/templates.js`).
- 🔌 **Plugin System** – Ship search/sort plugins or register your own (`static/js/plugins.js`).
- 🌍 **Multi-language** – Per-language data folders with shared metadata for language labels.
- 📱 **Responsive** – Built on Bulma; optimized for desktop, tablet, and mobile.
- 🎨 **Theme Friendly** – Global theme settings in `data/meta.json`.

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd academic-template
```

### 2. Configure Meta Information
`data/meta.json` is the source of truth for global settings. Minimal example:
```json
{
  "defaultLanguage": "en",
  "availableLanguages": ["en", "zh", "jp"],
  "languageLabels": {
    "en": "English",
    "zh": "中文",
    "jp": "日本語"
  },
  "navbar": {
    "showLanguageDropdown": true
  },
"home": {
  "showHero": true,
  "avatar": "./media/personal.jpg"
},
"backgrounds": {
  "default": {
    "light": "./media/occupacy.jpg",
    "dark": "./media/occupacy_dark.jpg"
  },
  "news": {
    "light": "./media/news_bg.jpg",
    "dark": "./media/news_bg_dark.jpg"
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
      "background": "news",
      "singlePage": {"enabled": true},
      "multiPage": {"enabled": true, "plugins": ["search"]}
    }
  ],
  "socials": [{"icon": "fab fa-github", "url": "https://github.com/your-name"}]
}
```

### 3. Provide Content per Language
Each language has its own folder under `data/<lang>/`.

- `web_content.json` – homepage copy only (title, subtitle, footer, etc.).
- `<section>.json` – each section keeps its navigation label, title, and payload.

Example `data/en/news.json`:
```json
{
  "nav_label": "News",
  "title": "🔥 News",
  "news": [
    {"date": "2025.01.01", "content": "Placeholder news item."}
  ]
}
```

Example `data/en/about.json`:
```json
{
  "nav_label": "About Me",
  "title": "🎄 About Me",
  "texts": [
    "<strong>About me placeholder:</strong> introduce yourself.",
    "Add another paragraph with your interests or call-to-action."
  ]
}
```

Other section files (`publications.json`, `projects.json`, `blogs.json`, `academic_service.json`) follow the same pattern: `nav_label`, `title`, and the section-specific array (`publications`, `projects`, `blogs`, `academic_service`, etc.).

### 4. Run a Static Server
```bash
python3 -m http.server 8000
# or
npx serve .
```
Visit `http://localhost:8000` or `http://localhost:8000/multipage_index.html`.

## 📖 Configuration Details

### `data/meta.json`
- **defaultLanguage / availableLanguages** – control the initial language and the language options.
- **languageLabels** – shared human-readable names for language codes. UI always pulls labels from here.
- **backgrounds** – declare reusable background sets (`light`/`dark`); sections reference them via `background` key.
- *Tip*: the home page uses `backgrounds.home` when present, otherwise falls back to `backgrounds.default`.
- **sections** – define enabled sections, their data sources, item types, backgrounds, and plugin usage.
- **itemTypes** – map item types to template IDs (`static/js/templates.js`) and list required keys.
- **themes / socials / home** – tweak theme colors, hero avatar, and social icons.

### Section Data Contracts
Each section file must expose at least:
```json
{
  "nav_label": "...",
  "title": "...",
  "<dataSource>": [ ... items ... ]
}
```
where `<dataSource>` matches `sections[].dataSource` in `meta.json`. For timeline-style sections you can use `items` instead.

To assign a custom background to a page/section:

1. Add an entry under `backgrounds` in `data/meta.json` and provide `light`/`dark` image paths.
2. Reference the background key in the section definition, e.g. `"background": "news"`.
3. If omitted, the section (and home) fall back to the `default` background (`occupacy` images).

### Homepage Copy (`web_content.json`)
```json
{
  "navbar_title": "Academic Template",
  "navbar_home": "Home",
  "language": "Language",
  "title": "Add your homepage headline here.",
  "subtitle": "Use this subtitle to share a short mission statement or tagline.",
  "footer": "Powered by Academic Template"
}
```

Only home-specific strings remain here; everything else lives in per-section files.

## 🔧 Extending the Template

### 1. Add a New Language
1. Update `data/meta.json`:
   - Append the language code to `availableLanguages`.
   - Provide a label in `languageLabels` (e.g., `"de": "Deutsch"`).
2. Create `data/<lang>/` folder with:
   - `web_content.json` (homepage copy for the new language).
   - `<section>.json` for each enabled section (copy an existing language file as a template).
3. Add translated media if necessary.

### 2. Add a New Section
1. Register section in `data/meta.json`:
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
2. Define an item type if you need a new template:
```json
"itemTypes": {
  "timeline": {
    "requiredKeys": ["date", "title", "org", "description"],
    "template": "timeline"
  }
}
```
3. For each language create `data/<lang>/education.json`:
```json
{
  "nav_label": "Education",
  "title": "🎓 Education",
  "education": [
    {"date": "2020–2024", "title": "BSc", "org": "University", "description": "Details"}
  ]
}
```
4. (Optional) Add a background preset in `data/meta.json.backgrounds` (e.g. `"education": {"light": "...", "dark": "..."}`).
5. (Optional) Supply custom empty-state text in `meta.json.emptyStates` with the section id.

### 3. Customize Section Templates
- Templates live in `static/js/templates.js`. Register a new template name and implement rendering.
- Reference the template in `itemTypes[].template`.
- Need extra behavior (filtering, sorting)? Register a plugin in `static/js/plugins.js` and list it under `sections[].multiPage.plugins`.

### 4. Tailor Styles
- Global styles: `static/css/index.css`.
- Section-specific tweaks: add classes within section templates and target them in CSS.
- Light/dark adjustments: see the bottom of `static/css/index.css` for dark-mode overrides.

## 🧪 Development Tips
- **Live Reload**: Pair with a local static server that supports livereload for rapid iteration.
- **Data Validation**: Item types declare `requiredKeys`; use them as a checklist when authoring content.
- **Fallbacks**: If a section file is missing in the current language, the UI will hide that section until data is provided.
- **Testing Plugins**: Check search/sort on multipage sections after any data schema change.

## 📁 Project Structure Overview
```
├── data/
│   ├── meta.json              # global config (languages, sections, themes)
│   ├── en/
│   │   ├── web_content.json   # homepage copy (EN)
│   │   ├── about.json         # section metadata + content
│   │   ├── news.json
│   │   └── ...
│   ├── zh/
│   └── jp/
├── static/
│   ├── css/index.css          # global styling
│   ├── js/templates.js        # template registry
│   ├── js/plugins.js          # plugin registry
│   └── js/index.js            # shared UI helpers
├── index.html                 # single-page mode entry
└── multipage_index.html       # multi-page mode entry
```

## 📝 License
MIT License. Feel free to use, remix, and share.
