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
    // Animation de sortie par la droite pour les éléments non correspondants
    nonMatchingCards.forEach((card, index) => {
        if (card.style.display !== 'none') {
            setTimeout(() => {
                card.style.opacity = '0';
                card.style.transform = 'translateX(150%) rotateY(90deg) scale(0.8)';
                card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';

                setTimeout(() => {
                    card.style.display = 'none';
                    // Repositionner pour l'entrée par la gauche
                    card.style.transform = 'translateX(-150%) rotateY(-90deg) scale(0.8)';
                }, 600);
            }, index * 50);
        }
    });

    // Animation d'entrée par la gauche pour les éléments correspondants
    setTimeout(() => {
        // Réorganiser la grille
        const allCards = Array.from(itemsGrid.children);
        const sortedCards = [...matchingCards, ...nonMatchingCards];

        // Réorganiser dans l'ordre voulu
        sortedCards.forEach(card => {
            itemsGrid.appendChild(card);
        });

        // Animer l'entrée des éléments correspondants
        matchingCards.forEach((card, index) => {
            if (card.style.display === 'none') {
                card.style.display = 'block';
                card.style.opacity = '0';
                card.style.transform = 'translateX(-150%) rotateY(-90deg) scale(0.8)';
            }

            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateX(0) rotateY(0deg) scale(1)';
                card.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
            }, index * 80 + 300);
        });

        // Réinitialiser les éléments cachés
        nonMatchingCards.forEach(card => {
            card.style.display = 'none';
            card.style.opacity = '0';
            card.style.transform = 'translateX(-150%) rotateY(-90deg) scale(0.8)';
        });
    }, 400);
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

// Navigation mobile avec animation
function setupMobileNavigation() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileNavMenu = document.getElementById('mobileNavMenu');

    if (mobileMenuToggle && mobileNavMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            if (mobileNavMenu.classList.contains('open')) {
                // Fermer le menu
                mobileNavMenu.classList.remove('open');
                this.textContent = '☰';
            } else {
                // Ouvrir le menu
                mobileNavMenu.style.display = 'block';
                // Forcer un reflow pour que la transition fonctionne
                mobileNavMenu.offsetHeight;
                mobileNavMenu.classList.add('open');
                this.textContent = '✕';
            }
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
                if (mobileNavMenu.classList.contains('open')) {
                    mobileNavMenu.classList.remove('open');
                    mobileMenuToggle.textContent = '☰';
                }
            }
        });

        // Cacher le menu après la transition de fermeture
        mobileNavMenu.addEventListener('transitionend', function() {
            if (!this.classList.contains('open')) {
                this.style.display = 'none';
            }
        });
    }
}

// Effet de parallaxe léger pour la bannière - DÉSACTIVÉ pour éviter les problèmes de scaling
function setupParallaxEffect() {
    // Parallax désactivé pour éviter les conflits avec le scaling des cartes
    console.log('Parallax effect disabled to prevent scaling conflicts');
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