(function (global) {
    const _registry = new Map();

    const TemplateRegistry = {
        register(name, rendererFn) {
            console.log(`[TemplateRegistry] Registered template: ${name}`);
            _registry.set(name, rendererFn);
        },
        get(name) {
            if (!_registry.has(name)) {
                console.warn(`[TemplateRegistry] No template found for: ${name}`);
                return null;
            }
            const renderer = _registry.get(name);
            console.log(`[TemplateRegistry][GET] template: ${name}`, renderer);
            return renderer;
        }
    };



    global.TemplateRegistry = TemplateRegistry;
    console.log("[templates.js] global.TemplateRegistry assigned");
})(window);
