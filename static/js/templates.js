(function (global) {
    const TemplateRegistry = {
        registry: new Map(),
        register(name, renderer) { this.registry.set(name, renderer); },
        get(name) { return this.registry.get(name); }
    };

    TemplateRegistry.register('list-inline', function renderListInline(items, section, contentDiv) {
        if (!items || items.length === 0) {
            const emptyDiv = document.createElement('div');
            emptyDiv.className = 'empty-state';
            emptyDiv.style.cssText = 'text-align: center; padding: 40px; color: #666; font-style: italic;';
            emptyDiv.textContent = 'No items available.';
            contentDiv.appendChild(emptyDiv);
            return;
        }

        items.forEach(item => {
            const div = document.createElement('div');
            div.style.cssText = 'display: flex; justify-content: flex-start; align-items: center; margin-bottom: 15px;';
            const date = item.date || '';
            const text = item.content || '';
            div.innerHTML = `<span style="font-weight: bold; margin-right: 50px;">${date}</span><span style="font-family: Georgia">${text}</span>`;
            contentDiv.appendChild(div);
        });
    });

    TemplateRegistry.register('paper-card', function renderPaperCard(items, section, contentDiv) {
        if (!items || items.length === 0) {
            const emptyDiv = document.createElement('div');
            emptyDiv.className = 'empty-state';
            emptyDiv.style.cssText = 'text-align: center; padding: 40px; color: #666; font-style: italic;';
            emptyDiv.textContent = 'No items available.';
            contentDiv.appendChild(emptyDiv);
            return;
        }

        items.forEach(entry => {
            const paperContainer = document.createElement('div');
            paperContainer.className = 'paper-container';
            const imageHtml = entry.image ? `<img src="${entry.image}" alt="Overview" class="paper-image">` : '<div class="paper-image" style="background: #f0f0f0; display: flex; align-items: center; justify-content: center; height: 150px;">No Image</div>';
            const linksHtml = Array.isArray(entry.links) ? entry.links.map(link => `<a href="${link.url}" target="_blank" class="paper-link">[${link.type}]</a>`).join(' ') : '';
            const rightTop = (entry.date ? `<span style="margin-left: auto; font-size: 16px;">${entry.date}</span>` : '');
            paperContainer.innerHTML = `
        ${imageHtml}
        <div class="paper-content">
          <h2 class="paper-title" style="display: flex; justify-content: space-between; align-items: center;">
            ${entry.title || ''}
            ${rightTop}
          </h2>
          ${entry.conference ? `<p class=\"paper-conf\">${entry.conference}</p>` : ''}
          ${entry.authors ? `<p class=\"paper-authors\">${entry.authors}</p>` : ''}
          ${entry.content ? `<p class=\"paper-description blog-description\">${entry.content}</p>` : `<p class=\"paper-description\">${entry.description || ''}</p>`}
          <p>${linksHtml}</p>
        </div>`;
            contentDiv.appendChild(paperContainer);
        });
    });

    TemplateRegistry.register('timeline', function renderTimeline(items, section, contentDiv) {
        if (!items || items.length === 0) {
            const emptyDiv = document.createElement('div');
            emptyDiv.className = 'empty-state';
            emptyDiv.style.cssText = 'text-align: center; padding: 40px; color: #666; font-style: italic;';
            emptyDiv.textContent = 'No items available.';
            contentDiv.appendChild(emptyDiv);
            return;
        }

        items.forEach(entry => {
            const div = document.createElement('div');
            div.className = 'timeline-item';
            div.style.cssText = 'margin: 12px 0;';
            const date = entry.date || '';
            const title = entry.title || '';
            const org = entry.org ? ` @ ${entry.org}` : '';
            const desc = entry.description || '';
            div.innerHTML = `<div style=\"font-weight: bold;\">${date} · ${title}${org}</div><div>${desc}</div>`;
            contentDiv.appendChild(div);
        });
    });

    global.TemplateRegistry = TemplateRegistry;
})(window);
