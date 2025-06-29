// Main JavaScript functionality for Tourism Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Search functionality
    initializeSearch();
    
    // Form validation
    initializeFormValidation();
    
    // Image lazy loading
    initializeLazyLoading();
    
    // Favorite functionality
    initializeFavorites();
    
    // Rating display
    initializeRatings();
    
    // Date validation for booking forms
    initializeDateValidation();
});

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchForm = document.getElementById('searchForm');
    
    if (searchInput && searchForm) {
        // Remove auto-submit on input, submit only on button click or Enter
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                searchForm.submit();
            }
        });
    }
    
    // Filter functionality
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            if (searchForm) {
                searchForm.submit();
            }
        });
    });
}

// Form validation
function initializeFormValidation() {
    // Bootstrap form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Custom validation for specific fields
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', validateEmail);
    });
    
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('blur', validatePhone);
    });
}

// Email validation
function validateEmail(event) {
    const email = event.target.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email && !emailRegex.test(email)) {
        event.target.setCustomValidity('Please enter a valid email address');
    } else {
        event.target.setCustomValidity('');
    }
}

// Phone validation
function validatePhone(event) {
    const phone = event.target.value;
    const phoneRegex = /^\+?[1-9]\d{1,14}$/;
    
    if (phone && !phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''))) {
        event.target.setCustomValidity('Please enter a valid phone number');
    } else {
        event.target.setCustomValidity('');
    }
}

// Image lazy loading
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

// Favorite functionality
function initializeFavorites() {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    
    favoriteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const destinationId = this.dataset.destinationId;
            const isFavorited = this.classList.contains('favorited');
            
            // Add loading state
            this.classList.add('loading');
            this.disabled = true;
            
            // Make request to toggle favorite
            fetch(`/destinations/${destinationId}/favorite`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.classList.toggle('favorited');
                    const icon = this.querySelector('i');
                    if (this.classList.contains('favorited')) {
                        icon.classList.remove('far');
                        icon.classList.add('fas');
                        this.title = 'Remove from favorites';
                    } else {
                        icon.classList.remove('fas');
                        icon.classList.add('far');
                        this.title = 'Add to favorites';
                    }
                }
            })
            .catch(error => {
                console.error('Error toggling favorite:', error);
                showAlert(error);
            })
            .finally(() => {
                this.classList.remove('loading');
                this.disabled = false;
            });
        });
    });
}

// Rating display
function initializeRatings() {
    const ratingContainers = document.querySelectorAll('.rating');
    
    ratingContainers.forEach(container => {
        const rating = parseFloat(container.dataset.rating);
        const stars = container.querySelectorAll('.star');
        
        stars.forEach((star, index) => {
            if (index < Math.floor(rating)) {
                star.classList.add('fas');
                star.classList.remove('far');
            } else if (index < rating) {
                star.classList.add('fas');
                star.classList.remove('far');
                star.style.clipPath = `inset(0 ${100 - (rating - index) * 100}% 0 0)`;
            } else {
                star.classList.add('far');
                star.classList.remove('fas');
            }
        });
    });
}

// Date validation for booking forms
function initializeDateValidation() {
    const checkInInputs = document.querySelectorAll('input[name="checkInDate"]');
    const checkOutInputs = document.querySelectorAll('input[name="checkOutDate"]');
    const reservationDateInputs = document.querySelectorAll('input[name="reservationDate"]');
    
    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    
    checkInInputs.forEach(input => {
        input.min = today;
        input.addEventListener('change', validateBookingDates);
    });
    
    checkOutInputs.forEach(input => {
        input.min = today;
        input.addEventListener('change', validateBookingDates);
    });
    
    reservationDateInputs.forEach(input => {
        input.min = today;
    });
}

// Validate booking dates
function validateBookingDates() {
    const checkInInput = document.querySelector('input[name="checkInDate"]');
    const checkOutInput = document.querySelector('input[name="checkOutDate"]');
    
    if (checkInInput && checkOutInput && checkInInput.value && checkOutInput.value) {
        const checkInDate = new Date(checkInInput.value);
        const checkOutDate = new Date(checkOutInput.value);
        
        if (checkOutDate <= checkInDate) {
            checkOutInput.setCustomValidity('Check-out date must be after check-in date');
            checkOutInput.reportValidity();
        } else {
            checkOutInput.setCustomValidity('');
        }
        
        // Update minimum checkout date
        const minCheckOut = new Date(checkInDate);
        minCheckOut.setDate(minCheckOut.getDate() + 1);
        checkOutInput.min = minCheckOut.toISOString().split('T')[0];
    }
}

// Utility functions
function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
}

function showAlert(message, type = 'danger') {
    const alertContainer = document.getElementById('alert-container') || document.body;
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Loading button state
function setButtonLoading(button, loading = true) {
    if (loading) {
        button.disabled = true;
        button.classList.add('loading');
        const originalText = button.textContent;
        button.dataset.originalText = originalText;
        button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    } else {
        button.disabled = false;
        button.classList.remove('loading');
        button.textContent = button.dataset.originalText || button.textContent;
    }
}

// Smooth scrolling for anchor links
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

// Back to top button
function initializeBackToTop() {
    const backToTopBtn = document.getElementById('backToTop');
    
    if (backToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopBtn.style.display = 'block';
            } else {
                backToTopBtn.style.display = 'none';
            }
        });
        
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// Initialize back to top functionality
initializeBackToTop();

// Handle responsive navigation
function initializeResponsiveNav() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking on nav links
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                        toggle: false
                    });
                    bsCollapse.hide();
                }
            });
        });
    }
}

// Initialize responsive navigation
initializeResponsiveNav();

// Print functionality for bookings/reservations
function printDocument() {
    window.print();
}

// Export data functionality
function exportData(data, filename, type = 'json') {
    let content, mimeType;
    
    if (type === 'json') {
        content = JSON.stringify(data, null, 2);
        mimeType = 'application/json';
    } else if (type === 'csv') {
        content = convertToCSV(data);
        mimeType = 'text/csv';
    }
    
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
}

// Convert JSON to CSV
function convertToCSV(data) {
    if (!data.length) return '';
    
    const headers = Object.keys(data[0]);
    const csv = [
        headers.join(','),
        ...data.map(row => headers.map(header => 
            JSON.stringify(row[header] || '')
        ).join(','))
    ].join('\n');
    
    return csv;
}
