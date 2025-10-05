# Academic Template

A configuration-first academic homepage template with unified section rendering, multi-language data, and plugin extensions.
🌐 Live Demo: https://phospheneser.github.io/Phospheneser-awesome-academic-template/

[中文文档](README_ZH.md)

## ✨ Features
- 🎯 **Config Driven** – Navigation, sections, and content live in JSON; no HTML edits for day-to-day updates.
- 🧱 **Unified Layout** – All sections (except About) use the same paragraph-based renderer for consistent typography.
- 🔌 **Plugin Ready** – Search/sort plugins are bundled via `static/js/plugins.js`; register your own with a single call.
- 🌍 **Multi-language** – Per-language folders keep localized content while sharing the same metadata.
- 📱 **Responsive** – Bulma-based layout tuned for desktop, tablet, and mobile.
- 🎨 **Theming** – Configure backgrounds, hero avatar, socials, and theme colors in `data/meta.json`.

## 🚀 Quick Start
1. **Clone & enter the project**
   ```bash
   git clone <your-repo-url>
   cd academic-template
   ```
2. **Configure `data/meta.json`** – the global source of truth. Minimal sketch:
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
     "emptyStates": {"news": "No news available."}
   }
   ```
3. **Add per-language content** – each language uses `data/<lang>/`.
   - `web_content.json` holds homepage copy (title, subtitle, footer, etc.).
   - `<section>.json` mirrors the section `id`/`dataSource` in `meta.json`.
   - `blogs.json` localizes the blog list/detail chrome (`archive_label`, `page_labels`, `post_labels`).
   - Blog article bodies live under `blogs/posts/<slug>/<lang>.html` with automatic English fallback.

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

   Example `data/en/blogs.json`:
   ```json
   {
     "nav_label": "Blog",
     "title": "Research Log",
     "subtitle": "Stories, experiments, and longer reflections from ongoing projects.",
     "archive_label": "View all posts",
     "page_labels": {
       "back": "Back to site",
       "search": "Search posts...",
       "allTags": "All topics",
       "empty": "No posts published yet."
     },
     "post_labels": {
       "backBlog": "Back to blog",
       "bottomBackBlog": "Back to blog index",
       "darkToLight": "Switch to light mode"
     },
     "blogs": [
       {
         "slug": "launching-the-research-blog",
         "title": "Why This Blog Exists",
         "summary": "Setting the tone for longer-form updates.",
         "date": "2025-01-05",
         "post_time": "2025-01-05 09:00",
         "author": "Joshua Xu",
         "tags": ["Meta"]
       }
     ]
   }
   ```
4. **Serve statically**
   ```bash
   python3 -m http.server 8000
   # or
   npx serve .
   ```
   Open `http://localhost:8000` (single-page) or `http://localhost:8000/multipage_index.html` (multi-page).

## 🧩 Data & Rendering Model
### `data/meta.json`
- `availableLanguages` / `languageLabels` – configure language dropdown options.
- `backgrounds` – reusable light/dark backgrounds; sections reference them via `background`.
- Link icons are defined per link object via an `icon` (or `iconUrl`) property; icons render only when specified.
- `sections` – declarative section list with `id`, `dataSource`, `itemType`, backgrounds, and plugin usage.
- `itemTypes` – optional checklist of expected fields per item type; handy for content QA.
- `emptyStates` – per-section fallback text when a list has no items.
- `themes`, `socials`, `home` – tweak palette, social icons, and hero avatar.

### Language Folders (`data/<lang>/`)
Each section file must expose at least:
```json
{
  "nav_label": "...",
  "title": "...",
  "<dataSource>": [ ... items ... ]
}
```
where `<dataSource>` matches `sections[].dataSource`. Omit a language file to hide the section for that locale.

### Blog Content (`data/<lang>/blogs.json`)
- `archive_label` controls the homepage call-to-action that links to the blog archive.
- `page_labels` localizes the blog index chrome (back link, search placeholder, tag filter label, empty state, dark-mode tooltip).
- `post_labels` provides the article page UI strings (navigation buttons, dark-mode tooltip, missing-article copy).
- `blogs[]` stores metadata for each post (`slug`, `title`, `summary`, `date`, `post_time`, `author`, `tags`, optional `image`).
- Article bodies live in `blogs/posts/<slug>/<lang>.html`; when a translation is missing, the English file is used automatically.
- Configure card actions (e.g., "Read more") via `meta.json -> itemTypes.blog.templateOptions.actions`.

### Unified Section Renderer
`index.html` and `multipage_index.html` share the same text-first renderer:
- **news** – `date` + `content`.
- **publication** – `title`, `conference`, optional `date`, `authors`, `description`, `links`.
- **project** – `title`, `date`, `authors`, `description`, `links`.
- **blog** – `title`, `date`, `content`, `links`.
- **timeline** – `title`, `org`, `date`, `description`.

Missing fields are skipped automatically. When no items exist, the renderer displays the localized `emptyStates` message.
Fine-tune how each item type maps onto the card layout through `meta.json -> itemTypes[*].templateOptions` and add styling via `.meta-card--<itemType>` selectors in CSS.

### Background Tips
1. Add images under `media/` (or any static directory).
2. Register light/dark paths in `backgrounds`.
3. Reference the key from the section definition. Home falls back to `backgrounds.home` → `backgrounds.default`.

## 🔧 Extending the Template
### Add a Language
1. Append the language code to `availableLanguages` and add a label under `languageLabels`.
2. Create `data/<lang>/` with translated `web_content.json`, section files, and a localized `blogs.json` (plus article HTML under `blogs/posts/<slug>/<lang>.html`).
3. Provide localized media if needed.

### Add a Section
1. Describe the section in `meta.json.sections` (optionally add `emptyStates` text).
2. Create `<lang>/<dataSource>.json` in every language folder.
3. Map fields through `meta.json -> itemTypes` (or register a template in `static/js/templates.js`) and style with CSS classes such as `.meta-card--<itemType>`—no homepage HTML edits required.

For detailed changes, see the [Usage Example](https://github.com/Phospheneser/Phospheneser.github.io/commit/d562fbf003b006c1ef92675db1a8ce6184f5062d#diff-185fdcbe4e1d3cf7c9aa4e9e86e9cf6b1f49d7ecd733e9ec81220c2890673cb6).


### Customize Rendering or Plugins
- Section markup comes from `static/js/templates.js` and the helper functions in `index.html` / `multipage_index.html`; extend `TemplateRegistry` or tweak `itemTypes[*].templateOptions` for new layouts without touching page HTML.
- Register plugins in `static/js/plugins.js` via `PluginRegistry.register` and add the plugin name to `multiPage.plugins`.
- Tweak typography and spacing inside `static/css/index.css` (`.text-homepage-1`, `.section-text-block`, etc.).

## 🧪 Development Notes
- Use a static server with live reload for faster iteration.
- `itemTypes.requiredKeys` act as a checklist when preparing content PRs.
- Multi-page mode exercises plugin hooks (search/sort); test both modes after changes.
- If a language file is missing, the corresponding section hides automatically—useful during translation rollouts.
