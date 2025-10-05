// Platform Mermaid diagram text to be white in dark mode
(function() {
    function applyDarkModeFix() {
        const isDarkMode = document.querySelector('body[data-md-color-scheme="slate"]');
        
        console.log('[Dark Mode Fix] Checking mode:', isDarkMode ? 'DARK' : 'LIGHT');
        
        if (isDarkMode) {
            // Multiple attempts to catch Mermaid rendering
            const attempts = [100, 500, 1000, 2000];
            
            attempts.forEach(function(delay) {
                setTimeout(function() {
                    // Find all text elements
                    const mermaidTexts = document.querySelectorAll(
                        '.mermaid text, .mermaid tspan, .mermaid .nodeLabel, .mermaid foreignObject div'
                    );
                    
                    console.log('[Dark Mode Fix] Found', mermaidTexts.length, 'text elements');
                    
                    mermaidTexts.forEach(function(text) {
                        text.style.fill = '#ffffff';
                        text.style.color = '#ffffff';
                        text.style.fontWeight = '600';
                    });
                    
                    // Darken colored boxes
                    const mermaidRects = document.querySelectorAll('.mermaid rect');
                    console.log('[Dark Mode Fix] Found', mermaidRects.length, 'rectangles');
                    
                    mermaidRects.forEach(function(rect) {
                        const currentFill = rect.style.fill || rect.getAttribute('fill');
                        if (currentFill && currentFill !== 'none' && !currentFill.includes('rgb(0')) {
                            rect.style.filter = 'brightness(0.4) saturate(1.5)';
                        }
                    });
                }, delay);
            });
        }
    }
    
    // Apply on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyDarkModeFix);
    } else {
        applyDarkModeFix();
    }
    
    // Apply on theme change
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'data-md-color-scheme') {
                console.log('[Dark Mode Fix] Theme changed!');
                applyDarkModeFix();
            }
        });
    });
    
    if (document.body) {
        observer.observe(document.body, {
            attributes: true,
            attributeFilter: ['data-md-color-scheme']
        });
    }
})();

