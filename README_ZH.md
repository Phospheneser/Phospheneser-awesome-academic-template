# 学术模板

一个高度可扩展的学术个人主页模板，支持通过配置驱动页面生成，具备模板注册表、插件系统、多语言支持等特性。

[English Documentation](README.md) | [中文文档](README_ZH.md)

## ✨ 特性

- 🎯 **配置驱动**: 通过 `data/meta.json` 控制页面结构、导航、内容类型
- 🧩 **模板系统**: 支持注册自定义渲染模板（list-inline、paper-card、timeline）
- 🔌 **插件系统**: 内置搜索、排序插件，支持扩展
- 🌍 **多语言**: 支持英文、中文、日文切换
- 📱 **响应式**: 基于 Bulma CSS 框架，适配各种设备
- 🎨 **主题支持**: 可配置主题色彩与样式

## 🚀 快速开始

### 1. 克隆模板
```bash
git clone <your-repo-url>
cd academic-template
```

### 2. 配置个人信息
编辑 `data/meta.json` 配置基本信息：
```json
{
  "defaultLanguage": "en",
  "availableLanguages": ["en", "zh", "jp"],
  "home": {
    "avatar": "./media/your-photo.jpg"
  },
  "socials": [
    {"icon": "fab fa-github", "url": "https://github.com/yourusername"},
    {"icon": "fas fa-envelope", "url": "mailto:your@email.com"}
  ]
}
```

### 3. 配置页面内容
在 `data/{lang}/` 目录下编辑各语言的内容文件：
- `web_content.json`: 页面文案
- `news.json`: 新闻动态
- `publications.json`: 学术论文
- `projects.json`: 项目经历
- `blogs.json`: 博客文章

### 4. 启动服务
```bash
# 使用 Python 简单服务器
python -m http.server 8000

# 或使用 Node.js
npx serve .

# 或使用任何静态文件服务器
```

访问 `http://localhost:8000` 查看效果。

## 📖 详细配置

### Meta 配置结构

```json
{
  "defaultLanguage": "en",
  "availableLanguages": ["en", "zh", "jp"],
  "navbar": {
    "showLanguageDropdown": true
  },
  "home": {
    "showHero": true,
    "showWordCloud": true,
    "avatar": "./media/avatar.jpg"
  },
  "itemTypes": {
    "news": {
      "requiredKeys": ["date", "content"],
      "template": "list-inline"
    },
    "publication": {
      "requiredKeys": ["title", "conference", "authors", "description", "links", "image"],
      "template": "paper-card"
    }
  },
  "sections": [
    {
      "id": "news",
      "enabled": true,
      "navLabelKey": "navbar_news",
      "titleKey": "news_title",
      "itemType": "news",
      "plugins": ["search"],
      "dataSource": "news",
      "layout": "list",
      "options": {
        "columns": 1,
        "gap": "normal"
      }
    }
  ],
  "socials": [...],
  "emptyStates": {...},
  "themes": {...}
}
```

### 内容类型定义

#### News (新闻)
```json
{
  "news": [
    {
      "date": "2025.01.01",
      "content": "Your news content here"
    }
  ]
}
```

#### Publications (论文)
```json
{
  "publications": [
    {
      "title": "Paper Title",
      "conference": "Conference Name",
      "authors": "Author A, Author B",
      "description": "Paper description",
      "links": [
        {"type": "Paper", "url": "https://example.com/paper"},
        {"type": "Code", "url": "https://github.com/repo"}
      ],
      "image": "./media/paper-image.jpg"
    }
  ]
}
```

#### Projects (项目)
```json
{
  "projects": [
    {
      "title": "Project Name",
      "date": "2025.01",
      "authors": "Contributor A, Contributor B",
      "description": "Project description",
      "links": [
        {"type": "Demo", "url": "https://example.com/demo"},
        {"type": "Code", "url": "https://github.com/project"}
      ],
      "image": "./media/project-image.jpg"
    }
  ]
}
```

## 🔧 扩展开发

### 添加新的内容类型

1. **定义 ItemType**:
```json
{
  "itemTypes": {
    "education": {
      "requiredKeys": ["date", "title", "org", "description"],
      "template": "timeline"
    }
  }
}
```

2. **添加 Section**:
```json
{
  "sections": [
    {
      "id": "education",
      "enabled": true,
      "navLabelKey": "navbar_education",
      "titleKey": "education_title",
      "itemType": "education",
      "plugins": ["search"],
      "dataSource": "education"
    }
  ]
}
```

3. **创建数据文件**:
```json
// data/en/education.json
{
  "education": [
    {
      "date": "2020-2024",
      "title": "Bachelor of Science",
      "org": "University Name",
      "description": "Major in Computer Science"
    }
  ]
}
```

### 注册自定义模板

```javascript
// static/js/templates.js
TemplateRegistry.register('custom-grid', function(items, section, contentDiv) {
  items.forEach(item => {
    const card = document.createElement('div');
    card.className = 'custom-card';
    card.innerHTML = `
      <h3>${item.title}</h3>
      <p>${item.description}</p>
    `;
    contentDiv.appendChild(card);
  });
});
```

### 开发插件

```javascript
// static/js/plugins.js
PluginRegistry.register('pagination', {
  apply(section, container, data, webContent) {
    // 分页插件逻辑
    const pagination = document.createElement('div');
    pagination.className = 'pagination';
    // ... 实现分页功能
    container.appendChild(pagination);
  }
});
```

## 🎨 样式定制

### 主题色彩
在 `data/meta.json` 中配置：
```json
{
  "themes": {
    "primary": "#3273dc",
    "secondary": "#23d160",
    "accent": "#ff3860"
  }
}
```

### CSS 变量
模板支持 CSS 变量，可在 `static/css/index.css` 中覆盖：
```css
:root {
  --primary-color: #3273dc;
  --secondary-color: #23d160;
  --accent-color: #ff3860;
}
```

## 📁 项目结构

```
academic-template/
├── data/
│   ├── meta.json              # 主配置文件
│   ├── en/                    # 英文内容
│   ├── zh/                    # 中文内容
│   └── jp/                    # 日文内容
├── static/
│   ├── css/
│   │   └── index.css          # 主样式文件
│   └── js/
│       ├── templates.js       # 模板注册表
│       ├── plugins.js         # 插件系统
│       └── index.js           # 核心逻辑
├── media/                     # 媒体文件
├── index.html                 # 单页模式
├── multipage_index.html       # 多页模式
├── README.md                  # 英文文档
└── README_ZH.md              # 中文文档
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [Bulma CSS Framework](https://bulma.io/)
- [Font Awesome](https://fontawesome.com/)
- [WordCloud2.js](https://github.com/timdream/wordcloud2.js)
