/**
 * Product Lightbox - Interactive Image Gallery
 * Allows users to view product images in a fullscreen modal with navigation
 */

class ProductLightbox {
    constructor() {
        this.currentIndex = 0;
        this.products = [];
        this.lightbox = null;
        this.init();
    }

    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    setup() {
        // Create lightbox modal structure
        this.createLightboxHTML();
        
        // Get all product cards and extract data
        this.products = this.extractProductData();
        
        // Bind click events to product images
        this.bindImageClicks();
        
        // Bind keyboard events
        this.bindKeyboardEvents();
        
        // Bind navigation buttons
        this.bindNavigationButtons();
    }

    createLightboxHTML() {
        const lightboxHTML = `
            <div class="product-lightbox" id="productLightbox">
                <button class="lightbox-close" id="lightboxClose" aria-label="Cerrar">
                    &times;
                </button>
                
                <button class="lightbox-nav prev" id="lightboxPrev" aria-label="Anterior">
                    ‹
                </button>
                
                <button class="lightbox-nav next" id="lightboxNext" aria-label="Siguiente">
                    ›
                </button>
                
                <div class="lightbox-content">
                    <div class="lightbox-layout">
                        <div class="lightbox-image-section">
                            <div class="lightbox-image-wrapper">
                                <img src="" alt="" class="lightbox-image" id="lightboxImage">
                            </div>
                        </div>
                        
                        <div class="lightbox-details">
                            <h2 class="lightbox-product-name" id="lightboxName"></h2>
                            <p class="lightbox-product-description" id="lightboxDescription"></p>
                            <div class="lightbox-product-price" id="lightboxPrice"></div>
                            <div class="lightbox-actions">
                                <a href="#" class="lightbox-btn lightbox-btn-primary" id="lightboxQuoteBtn">
                                    <i class="bi bi-calculator"></i>
                                    <span>Cotizar Ahora</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', lightboxHTML);
        this.lightbox = document.getElementById('productLightbox');
        
        // Close on backdrop click
        this.lightbox.addEventListener('click', (e) => {
            if (e.target === this.lightbox) {
                this.close();
            }
        });
    }

    extractProductData() {
        const productCards = document.querySelectorAll('.product-card');
        const products = [];
        
        productCards.forEach((card, index) => {
            const image = card.querySelector('.product-image');
            const name = card.querySelector('.product-name');
            const description = card.querySelector('.product-description');
            const quoteBtn = card.querySelector('a[href*="cotizacion"]');
            
            if (image && name) {
                products.push({
                    index: index,
                    imageSrc: image.getAttribute('src'),
                    imageAlt: image.getAttribute('alt'),
                    name: name.textContent.trim(),
                    description: description ? description.textContent.trim() : '',
                    quoteUrl: quoteBtn ? quoteBtn.getAttribute('href') : '#'
                });
                
                // Store index on the image element
                image.dataset.productIndex = index;
            }
        });
        
        return products;
    }

    bindImageClicks() {
        const productImages = document.querySelectorAll('.product-image');
        
        productImages.forEach(image => {
            image.style.cursor = 'pointer';
            image.addEventListener('click', (e) => {
                e.preventDefault();
                const index = parseInt(image.dataset.productIndex);
                this.open(index);
            });
        });
    }

    bindKeyboardEvents() {
        document.addEventListener('keydown', (e) => {
            if (!this.lightbox.classList.contains('active')) return;
            
            switch(e.key) {
                case 'Escape':
                    this.close();
                    break;
                case 'ArrowLeft':
                    this.prev();
                    break;
                case 'ArrowRight':
                    this.next();
                    break;
            }
        });
    }

    bindNavigationButtons() {
        const closeBtn = document.getElementById('lightboxClose');
        const prevBtn = document.getElementById('lightboxPrev');
        const nextBtn = document.getElementById('lightboxNext');
        
        closeBtn.addEventListener('click', () => this.close());
        prevBtn.addEventListener('click', () => this.prev());
        nextBtn.addEventListener('click', () => this.next());
    }

    open(index) {
        this.currentIndex = index;
        this.updateContent();
        this.lightbox.classList.add('active');
        document.body.classList.add('lightbox-open');
        this.updateNavigationButtons();
    }

    close() {
        this.lightbox.classList.remove('active');
        document.body.classList.remove('lightbox-open');
    }

    prev() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.updateContent();
            this.updateNavigationButtons();
        }
    }

    next() {
        if (this.currentIndex < this.products.length - 1) {
            this.currentIndex++;
            this.updateContent();
            this.updateNavigationButtons();
        }
    }

    updateContent() {
        const product = this.products[this.currentIndex];
        
        if (!product) return;
        
        // Update image
        const lightboxImage = document.getElementById('lightboxImage');
        lightboxImage.src = product.imageSrc;
        lightboxImage.alt = product.imageAlt;
        
        // Update text content
        document.getElementById('lightboxName').textContent = product.name;
        document.getElementById('lightboxDescription').textContent = product.description;
        
        // Update quote button link
        const quoteBtn = document.getElementById('lightboxQuoteBtn');
        quoteBtn.href = product.quoteUrl;
        
        // Add animation
        lightboxImage.style.opacity = '0';
        setTimeout(() => {
            lightboxImage.style.transition = 'opacity 0.3s ease';
            lightboxImage.style.opacity = '1';
        }, 10);
    }

    updateNavigationButtons() {
        const prevBtn = document.getElementById('lightboxPrev');
        const nextBtn = document.getElementById('lightboxNext');
        
        // Disable/enable based on position
        prevBtn.disabled = (this.currentIndex === 0);
        nextBtn.disabled = (this.currentIndex === this.products.length - 1);
        
        // Hide buttons if only one product
        if (this.products.length <= 1) {
            prevBtn.style.display = 'none';
            nextBtn.style.display = 'none';
        } else {
            prevBtn.style.display = 'flex';
            nextBtn.style.display = 'flex';
        }
    }
}

// Initialize the lightbox when script loads
const productLightbox = new ProductLightbox();
