(function (global) {
    const PluginRegistry = {
        registry: new Map(),
        register(name, plugin) {
            this.registry.set(name, plugin);
        },
        get(name) {
            return this.registry.get(name);
        },
        applyPlugins(section, container, data, webContent) {
            if (!section.plugins || !Array.isArray(section.plugins)) return;

            section.plugins.forEach(pluginName => {
                const plugin = this.get(pluginName);
                if (plugin && typeof plugin.apply === 'function') {
                    plugin.apply(section, container, data, webContent);
                }
            });
        }
    };

    function getControlsAndContent(section, container) {
        const controls = container.querySelector(`#${section.id}-controls`) || container.querySelector('.mp-controls') || container;
        const content = container.querySelector(`#${section.id}-content`) || container.querySelector('.mp-list');
        return { controls, content };
    }

    function normalizeText(text) {
        return (text || '').replace(/\s+/g, ' ').trim().toLowerCase();
    }

    // Search plugin
    PluginRegistry.register('search', {
        apply(section, container, data, webContent) {
            const { controls, content } = getControlsAndContent(section, container);
            if (!controls || !content) return;

            if (controls.querySelector('.meta-search')) return;

            const wrapper = document.createElement('div');
            wrapper.className = 'mp-control mp-control-search';

            const searchInput = document.createElement('input');
            searchInput.className = 'input meta-search';
            searchInput.type = 'search';
            const placeholder = webContent && webContent.search_placeholder ? webContent.search_placeholder : 'Search...';
            searchInput.placeholder = placeholder;

            wrapper.appendChild(searchInput);
            controls.appendChild(wrapper);

            searchInput.addEventListener('input', (e) => {
                const keyword = normalizeText(e.target.value);
                const items = Array.from(content.children);
                items.forEach(el => {
                    const text = normalizeText(el.textContent);
                    el.style.display = keyword ? (text.includes(keyword) ? '' : 'none') : '';
                });
            });
        }
    });

    // Sort plugin
    PluginRegistry.register('sort', {
        apply(section, container, data, webContent) {
            const { controls, content } = getControlsAndContent(section, container);
            if (!controls || !content) return;

            if (controls.querySelector('.meta-sort')) return;

            const wrapper = document.createElement('div');
            wrapper.className = 'mp-control mp-control-sort select';

            const sortSelect = document.createElement('select');
            sortSelect.className = 'meta-sort';
            const sortLabels = (webContent && webContent.sort_labels) || {};
            sortSelect.innerHTML = `
        <option value="">${sortLabels.default || 'Sort by...'}</option>
        <option value="date-desc">${sortLabels.date_desc || 'Date (Newest)'}</option>
        <option value="date-asc">${sortLabels.date_asc || 'Date (Oldest)'}</option>
        <option value="title-asc">${sortLabels.title_asc || 'Title (A-Z)'}</option>
        <option value="title-desc">${sortLabels.title_desc || 'Title (Z-A)'}</option>
      `;

            wrapper.appendChild(sortSelect);
            controls.appendChild(wrapper);

            sortSelect.addEventListener('change', (e) => {
                const sortValue = e.target.value;
                const items = Array.from(content.children);
                if (!sortValue || items.length === 0) return;

                const getDateValue = (element) => {
                    if (element.dataset && element.dataset.sortDate) {
                        return element.dataset.sortDate;
                    }
                    const dateEl = element.querySelector('[data-sort-date]') || element.querySelector('.paper-title span, time, .paper-conf, .paper-date');
                    return dateEl ? dateEl.getAttribute('data-sort-date') || dateEl.textContent || '' : '';
                };

                const getTitleValue = (element) => {
                    if (element.dataset && element.dataset.sortTitle) {
                        return element.dataset.sortTitle;
                    }
                    const titleEl = element.querySelector('[data-sort-title], .paper-title, h2, h3, .timeline-item > div:first-child');
                    if (titleEl) {
                        return titleEl.getAttribute('data-sort-title') || titleEl.textContent || '';
                    }
                    return '';
                };

                const compareStrings = (a, b, direction = 1) => {
                    return direction * a.localeCompare(b, undefined, { sensitivity: 'base' });
                };

                items.sort((a, b) => {
                    switch (sortValue) {
                        case 'date-desc':
                            return compareStrings(getDateValue(b), getDateValue(a));
                        case 'date-asc':
                            return compareStrings(getDateValue(a), getDateValue(b));
                        case 'title-asc':
                            return compareStrings(getTitleValue(a), getTitleValue(b));
                        case 'title-desc':
                            return compareStrings(getTitleValue(b), getTitleValue(a));
                        default:
                            return 0;
                    }
                });

                items.forEach(item => content.appendChild(item));
            });
        }
    });

    global.PluginRegistry = PluginRegistry;
})(window);

