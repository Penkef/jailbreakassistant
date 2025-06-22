
// Jailbreak Assistant - Home Page Script
console.log('Jailbreak Assistant Home Page loaded successfully!');

// Animation pour les cartes de fonctionnalités
function animateFeatureCards() {
    const cards = document.querySelectorAll('.feature-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 200);
    });
}

// Effect de clic sur le titre
function setupTitleInteraction() {
    const title = document.querySelector('h1');
    if (title) {
        title.addEventListener('click', function() {
            title.style.animation = 'none';
            title.style.color = '#FFD700';
            title.style.transform = 'scale(1.1)';
            
            setTimeout(() => {
                title.style.color = 'white';
                title.style.transform = 'scale(1)';
                title.style.animation = 'glow 2s ease-in-out infinite alternate';
            }, 1000);
        });
    }
}

// Effet de parallaxe léger pour la bannière
function setupParallaxEffect() {
    window.addEventListener('scroll', () => {
        const banner = document.querySelector('.banner');
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        
        if (banner) {
            banner.style.transform = `translateY(${rate}px)`;
        }
    });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - Jailbreak Assistant Home ready');
    
    // Démarrer les animations
    setTimeout(animateFeatureCards, 500);
    setupTitleInteraction();
    setupParallaxEffect();
    
    // Message de bienvenue dans la console
    console.log('%c🔓 Welcome to Jailbreak Assistant! 🔓', 'color: #FFD700; font-size: 16px; font-weight: bold;');
});

// Gestion des erreurs d'images
window.addEventListener('error', function(e) {
    if (e.target.tagName === 'IMG') {
        console.log('Image loading failed, using text fallback');
        e.target.style.display = 'none';
    }
});
