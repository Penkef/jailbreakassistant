
// Jailbreak Assistant - Main Script
console.log('Jailbreak Assistant loaded successfully!');

// Function to display loading animation
function showLoading() {
    const container = document.querySelector('.container');
    const loadingDiv = document.createElement('div');
    loadingDiv.innerHTML = '<p>Chargement en cours...</p>';
    loadingDiv.style.marginTop = '20px';
    container.appendChild(loadingDiv);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - Jailbreak Assistant ready');
    
    // Add interactive element
    const title = document.querySelector('h1');
    if (title) {
        title.addEventListener('click', function() {
            title.style.color = '#FFD700';
            setTimeout(() => {
                title.style.color = 'white';
            }, 1000);
        });
    }
});