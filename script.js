
// JavaScript combiné pour le site statique
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔓 Site statique Jailbreak Assistant chargé!');
    
    // Mobile navigation toggle
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileNavMenu = document.getElementById('mobileNavMenu');
    
    if (mobileMenuToggle && mobileNavMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileNavMenu.classList.toggle('active');
        });
    }
    
    // Animation pour les titres vides (h1)
    const titleElement = document.querySelector('h1');
    if (titleElement && titleElement.textContent.trim() === '') {
        const currentPage = window.location.pathname;
        
        if (currentPage.includes('values.html')) {
            titleElement.textContent = 'VALUES';
            titleElement.classList.add('values-title');
            console.log('Animation du titre VALUES activée');
        } else {
            titleElement.textContent = 'JAILBREAK ASSISTANT';
            console.log('Animation du titre HOME activée');
        }
    }
    
    // Search functionality pour la page values
    const searchInput = document.getElementById('searchInput');
    const itemsGrid = document.getElementById('itemsGrid');
    
    if (searchInput && itemsGrid) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const items = itemsGrid.querySelectorAll('.values-item-card');
            
            items.forEach(item => {
                const itemName = item.getAttribute('data-name').toLowerCase();
                const itemTitle = item.querySelector('.item-name').textContent.toLowerCase();
                
                if (itemName.includes(searchTerm) || itemTitle.includes(searchTerm)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
        
        console.log('Fonction de recherche activée');
    }
    
    // Feature cards interaction
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('click', function() {
            const feature = this.getAttribute('data-feature');
            
            switch(feature) {
                case 'values':
                    window.location.href = 'values.html';
                    break;
                case 'dupe-finder':
                    console.log('Dupe Finder - Coming Soon!');
                    break;
                case 'community':
                    console.log('Community features - Coming Soon!');
                    break;
            }
        });
        
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Smooth scrolling pour les liens internes
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Sticky banner effect
    const banner = document.querySelector('.banner');
    if (banner) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            
            banner.style.transform = `translateY(${rate}px)`;
        });
        
        console.log('Bannière avec effet parallax activée');
    }
    
    console.log('✅ Toutes les fonctionnalités JavaScript chargées');
});

// Animation au chargement
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease-in-out';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});
