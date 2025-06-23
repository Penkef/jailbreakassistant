// Jailbreak Assistant - Values Page Script
console.log('Jailbreak Assistant Values Page loaded successfully!');

// Fonction de recherche
function setupSearchFunctionality() {
    const searchInput = document.getElementById('searchInput');
    const itemCards = document.querySelectorAll('.values-item-card');

    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase().trim();

            itemCards.forEach(card => {
            const itemName = card.getAttribute('data-name').toLowerCase();
            const itemTitle = card.querySelector('h3').textContent.toLowerCase();

            // Vérifier si le terme de recherche est présent n'importe où dans le nom ou le titre
            const matches = searchTerm === '' || 
                           itemName.includes(searchTerm) || 
                           itemTitle.includes(searchTerm);

            if (matches) {
                // Afficher l'item avec animation
                card.classList.remove('hidden');
                card.style.opacity = '1';
                card.style.transform = 'scale(1)';
                card.style.display = 'block';
            } else {
                // Cacher l'item avec animation
                card.classList.add('hidden');
                card.style.opacity = '0';
                card.style.transform = 'scale(0.8)';
                setTimeout(() => {
                    if (card.classList.contains('hidden')) {
                        card.style.display = 'none';
                    }
                }, 300);
            }
        });

            // Log pour debug
            console.log(`Recherche: "${searchTerm}"`);
        });
    }

    // Animation d'entrée pour les cartes
    setTimeout(() => {
        itemCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'scale(1)';
            }, index * 100);
        });
    }, 300);
}

// Animation du titre VALUES
function setupTitleAnimation() {
    const title = document.querySelector('.values-title');
    if (title) {
        console.log('Animation du titre VALUES activée');
    }
}

// Gestionnaire de clics pour les cartes d'items
function setupItemCardHandlers() {
    const itemCards = document.querySelectorAll('.values-item-card');

    itemCards.forEach(card => {
        card.addEventListener('click', function() {
            const itemName = this.getAttribute('data-name');

            // Animation de clic
            this.style.transform = 'translateY(-8px) scale(1.05)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);

            console.log(`Item cliqué: ${itemName}`);
            // Ici on pourra ajouter plus de fonctionnalités plus tard
        });

        // Effet tactile pour mobile
        card.addEventListener('touchstart', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });

        card.addEventListener('touchend', function() {
            setTimeout(() => {
                this.style.transform = '';
            }, 100);
        });
    });
}

// Effet de parallaxe léger pour la bannière
function setupParallaxEffect() {
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const banner = document.querySelector('.banner');
        if (banner) {
            banner.style.transform = `translateY(${scrolled * 0.3}px)`;
        }
    });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - Jailbreak Assistant Values ready');

    setupSearchFunctionality();
    setupTitleAnimation();
    setupItemCardHandlers();
    setupParallaxEffect();

    // Message de bienvenue dans la console
    console.log('%c🔢 Welcome to Jailbreak Assistant Values! 🔢', 'color: #FFD700; font-size: 16px; font-weight: bold;');
});

// Gestion des erreurs d'images
window.addEventListener('error', function(e) {
    if (e.target.tagName === 'IMG') {
        console.log('Image loading failed, using text fallback');
        e.target.style.display = 'none';
    }
});