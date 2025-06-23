
// Jailbreak Assistant - Values Page Script
console.log('Jailbreak Assistant Values Page loaded successfully!');

// Variables globales pour la recherche
let currentSearchTerm = '';
let visibleCards = [];
let hiddenCards = [];

// Fonction de recherche avec repositionnement intelligent
function setupSearchFunctionality() {
    const searchInput = document.getElementById('searchInput');
    const itemCards = document.querySelectorAll('.values-item-card');
    const itemsGrid = document.getElementById('itemsGrid');

    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase().trim();
            
            // Créer une liste des éléments correspondants
            const matchingCards = [];
            const nonMatchingCards = [];

            itemCards.forEach(card => {
                const itemName = card.getAttribute('data-name').toLowerCase();
                const itemTitle = card.querySelector('h3').textContent.toLowerCase();
                
                const matches = searchTerm === '' || 
                               itemName.includes(searchTerm) || 
                               itemTitle.includes(searchTerm);

                if (matches) {
                    matchingCards.push(card);
                } else {
                    nonMatchingCards.push(card);
                }
            });

            // Réorganiser la grille
            reorganizeGrid(matchingCards, nonMatchingCards, itemsGrid);
            
            currentSearchTerm = searchTerm;
            console.log(`Recherche: "${searchTerm}"`);
        });
    }

    // Animation d'entrée pour les cartes
    setTimeout(() => {
        itemCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'scale(1)';
            }, index * 50);
        });
    }, 300);
}

function reorganizeGrid(matchingCards, nonMatchingCards, itemsGrid) {
    // Cacher les éléments non correspondants avec animation
    nonMatchingCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '0';
            card.style.transform = 'scale(0.8) translateY(-20px)';
            card.style.transition = 'all 0.4s ease';
            
            setTimeout(() => {
                card.style.display = 'none';
            }, 400);
        }, index * 30);
    });

    // Réorganiser et afficher les éléments correspondants
    setTimeout(() => {
        // Retirer tous les éléments de la grille
        Array.from(itemsGrid.children).forEach(card => {
            if (nonMatchingCards.includes(card)) {
                itemsGrid.removeChild(card);
            }
        });

        // Réinsérer les éléments correspondants dans l'ordre
        matchingCards.forEach((card, index) => {
            card.style.display = 'block';
            card.style.opacity = '0';
            card.style.transform = 'scale(0.8) translateY(20px)';
            
            if (!itemsGrid.contains(card)) {
                itemsGrid.appendChild(card);
            }
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'scale(1) translateY(0)';
                card.style.transition = 'all 0.4s ease';
            }, index * 50);
        });

        // Réinsérer les éléments cachés à la fin (mais cachés)
        nonMatchingCards.forEach(card => {
            if (!itemsGrid.contains(card)) {
                itemsGrid.appendChild(card);
                card.style.display = 'none';
            }
        });
    }, 200);
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

// Navigation mobile
function setupMobileNavigation() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileNavMenu = document.getElementById('mobileNavMenu');

    if (mobileMenuToggle && mobileNavMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileNavMenu.classList.toggle('open');
            this.textContent = mobileNavMenu.classList.contains('open') ? '✕' : '☰';
        });

        // Fermer le menu en cliquant sur un lien
        const mobileLinks = mobileNavMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileNavMenu.classList.remove('open');
                mobileMenuToggle.textContent = '☰';
            });
        });

        // Fermer le menu en cliquant à l'extérieur
        document.addEventListener('click', function(event) {
            if (!mobileNavMenu.contains(event.target) && !mobileMenuToggle.contains(event.target)) {
                mobileNavMenu.classList.remove('open');
                mobileMenuToggle.textContent = '☰';
            }
        });
    }
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
    setupMobileNavigation();
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
