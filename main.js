// 1. Mobile Menu Toggle
function toggleMenu() {
    const menu = document.getElementById('mobileMenu');
    menu.classList.toggle('active');
}

// 2. Google Translate Init
function googleTranslateElementInit() {
    new google.translate.TranslateElement({
        pageLanguage: 'en',
        // English, Spanish, Arabic, Vietnamese, Urdu, Farsi (Common in NOVA area)
        includedLanguages: 'en,es,ar,vi,ur,fa',
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
        autoDisplay: false
    }, 'google_translate_element');
}

// Sticky Header Scroll Logic
window.addEventListener('scroll', () => {
    const nav = document.getElementById('navbar');
    if (window.scrollY > 10) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});

// 3. Testimonials Slider Code
document.addEventListener('DOMContentLoaded', () => {
    const track = document.getElementById('newReviewsTrack');
    if (!track) return;

    const slides = Array.from(track.children);
    const nextButton = document.querySelector('.next-slide');
    const prevButton = document.querySelector('.prev-slide');
    const dotsNav = document.getElementById('reviewDots');

    let currentIndex = 0;
    let autoPlayInterval;

    slides.forEach((_, index) => {
        const dot = document.createElement('div');
        dot.classList.add('modern-dot');
        if (index === 0) dot.classList.add('active');
        dot.addEventListener('click', () => {
            goToSlide(index);
            resetAutoPlay();
        });
        dotsNav.appendChild(dot);
    });

    const dots = Array.from(dotsNav.children);

    function updateDots(index) {
        dots.forEach(d => d.classList.remove('active'));
        dots[index].classList.add('active');
    }

    function goToSlide(index) {
        if (index < 0) {
            index = slides.length - 1;
        } else if (index >= slides.length) {
            index = 0;
        }

        currentIndex = index;
        const gap = 30;
        const slideWidth = slides[0].getBoundingClientRect().width;
        const moveAmount = (slideWidth + gap) * currentIndex;
        track.style.transform = `translateX(-${moveAmount}px)`;
        updateDots(currentIndex);
    }

    nextButton.addEventListener('click', () => {
        goToSlide(currentIndex + 1);
        resetAutoPlay();
    });

    prevButton.addEventListener('click', () => {
        goToSlide(currentIndex - 1);
        resetAutoPlay();
    });

    function startAutoPlay() {
        autoPlayInterval = setInterval(() => {
            goToSlide(currentIndex + 1);
        }, 6000);
    }

    function resetAutoPlay() {
        clearInterval(autoPlayInterval);
        startAutoPlay();
    }

    let touchStartX = 0;
    let touchEndX = 0;

    track.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    });

    track.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        if (touchEndX < touchStartX - 50) {
            goToSlide(currentIndex + 1);
            resetAutoPlay();
        }
        if (touchEndX > touchStartX + 50) {
            goToSlide(currentIndex - 1);
            resetAutoPlay();
        }
    }

    window.addEventListener('resize', () => {
        goToSlide(currentIndex);
    });

    startAutoPlay();
});

// 4. Scroll Animations
const observerOptions = {
    threshold: 0.15,
    rootMargin: "0px 0px -50px 0px"
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.fade-in-up').forEach(el => {
    observer.observe(el);
});

// 5. Copyright Year
const yearSpan = document.getElementById('year');
if(yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
}

// 6. Modern Chat Widget Logic
function toggleChat() {
    const widget = document.querySelector('.modern-chat-widget');
    widget.classList.toggle('active');
}

setTimeout(() => {
    const tooltip = document.getElementById('chatTooltip');
    if(tooltip && !document.querySelector('.modern-chat-widget.active')) {
        tooltip.classList.add('visible');
        setTimeout(() => {
            tooltip.classList.remove('visible');
        }, 8000);
    }
}, 3000);

// 7. Form Validation
function validateForm(event) {
    event.preventDefault();
    const radios = document.getElementsByName('humancheck');
    let selectedValue = null;
    for (let i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            selectedValue = radios[i].value;
            break;
        }
    }
    if (selectedValue === 'house') {
        alert('Thank you! Your appointment request has been sent. We will contact you shortly.');
        document.getElementById('bookingForm').reset();
    } else {
        alert('Please prove you are human by selecting the HOUSE icon.');
    }
    return false;
}

// 8. Accessibility Widget Logic (Grayscale Removed)
function toggleAccessibility() {
    const widget = document.getElementById('accessWidget');
    widget.classList.toggle('active');
}

let currentFontSize = 100;

function changeFontSize(direction) {
    if (direction === 1 && currentFontSize < 150) {
        currentFontSize += 10;
    } else if (direction === -1 && currentFontSize > 70) {
        currentFontSize -= 10;
    }
    document.documentElement.style.fontSize = currentFontSize + '%';
}

function toggleHighContrast() {
    document.body.classList.toggle('high-contrast');
}

function toggleLinks() {
    document.body.classList.toggle('highlight-links');
}

function resetAccessibility() {
    currentFontSize = 100;
    document.documentElement.style.fontSize = '';
    document.body.classList.remove('high-contrast', 'highlight-links');
}

// 9. FAQ Toggle Logic
function toggleFAQ(element) {
    const item = element.parentElement;
    item.classList.toggle('active');
}