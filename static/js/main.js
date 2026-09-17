const header = document.getElementById('header');
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');

// Header scroll effect
window.addEventListener('scroll', function() {
    if (!header) return;

    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Mobile menu toggle
if (hamburger && navLinks) {
    const setMenuState = (isOpen) => {
        hamburger.classList.toggle('active', isOpen);
        navLinks.classList.toggle('active', isOpen);
        hamburger.setAttribute('aria-expanded', String(isOpen));
        hamburger.setAttribute('aria-label', isOpen ? 'Fermer le menu' : 'Ouvrir le menu');
    };

    hamburger.addEventListener('click', function() {
        setMenuState(!navLinks.classList.contains('active'));
    });

    // Close mobile menu when clicking a link
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function() {
            setMenuState(false);
        });
    });

    // Ferme le panneau lorsqu'un clic est effectué en dehors de l'en-tête.
    document.addEventListener('click', function(event) {
        if (!header.contains(event.target)) {
            setMenuState(false);
        }
    });

    // Évite de conserver un état mobile si la fenêtre repasse en desktop.
    window.addEventListener('resize', function() {
        if (window.innerWidth > 820) {
            setMenuState(false);
        }
    });
}
