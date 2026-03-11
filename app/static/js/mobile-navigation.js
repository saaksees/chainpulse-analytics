// ChainPulse Mobile Navigation JavaScript

class MobileNavigation {
    constructor() {
        this.sidebar = null;
        this.overlay = null;
        this.menuBtn = null;
        this.isOpen = false;
        this.touchStartX = 0;
        this.touchStartY = 0;
        
        this.init();
    }
    
    init() {
        this.createMobileElements();
        this.bindEvents();
        this.handleResize();
        
        // Listen for window resize
        window.addEventListener('resize', () => this.handleResize());
        
        // Handle orientation change
        window.addEventListener('orientationchange', () => {
            setTimeout(() => this.handleResize(), 100);
        });
    }
    
    createMobileElements() {
        // Create mobile menu button
        this.createMenuButton();
        
        // Create mobile overlay
        this.createOverlay();
        
        // Create bottom navigation for mobile
        this.createBottomNavigation();
        
        // Get sidebar reference
        this.sidebar = document.querySelector('.cp-sidebar');
    }
    
    createMenuButton() {
        const topbar = document.querySelector('.cp-topbar');
        if (!topbar) {
            // Create topbar if it doesn't exist
            const main = document.querySelector('.cp-main');
            const newTopbar = document.createElement('div');
            newTopbar.className = 'cp-topbar';
            main.insertBefore(newTopbar, main.firstChild);
        }
        
        const targetTopbar = document.querySelector('.cp-topbar');
        
        // Check if menu button already exists
        if (targetTopbar.querySelector('.mobile-menu-btn')) {
            this.menuBtn = targetTopbar.querySelector('.mobile-menu-btn');
            return;
        }
        
        // Create menu button
        this.menuBtn = document.createElement('button');
        this.menuBtn.className = 'mobile-menu-btn';
        this.menuBtn.innerHTML = '☰';
        this.menuBtn.setAttribute('aria-label', 'Open navigation menu');
        
        // Create topbar content
        const topbarContent = document.createElement('div');
        topbarContent.style.display = 'flex';
        topbarContent.style.alignItems = 'center';
        topbarContent.style.gap = '12px';
        
        const logo = document.createElement('div');
        logo.style.fontWeight = '700';
        logo.style.color = 'var(--text-primary)';
        logo.textContent = 'ChainPulse';
        
        topbarContent.appendChild(this.menuBtn);
        topbarContent.appendChild(logo);
        
        // Add user info if available
        const userInfo = this.createUserInfo();
        if (userInfo) {
            topbarContent.appendChild(userInfo);
        }
        
        targetTopbar.appendChild(topbarContent);
    }
    
    createUserInfo() {
        // Try to get user info from existing elements
        const existingUserInfo = document.querySelector('.cp-user-info, .user-dropdown');
        if (existingUserInfo) {
            const mobileUserInfo = existingUserInfo.cloneNode(true);
            mobileUserInfo.style.marginLeft = 'auto';
            return mobileUserInfo;
        }
        
        // Create simple user indicator
        const userInfo = document.createElement('div');
        userInfo.style.marginLeft = 'auto';
        userInfo.style.padding = '8px 12px';
        userInfo.style.background = 'var(--bg-primary)';
        userInfo.style.borderRadius = '20px';
        userInfo.style.fontSize = '12px';
        userInfo.style.color = 'var(--text-secondary)';
        userInfo.textContent = 'User';
        
        return userInfo;
    }
    
    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'mobile-overlay';
        document.body.appendChild(this.overlay);
    }
    
    createBottomNavigation() {
        // Check if bottom nav already exists
        if (document.querySelector('.mobile-bottom-nav')) {
            return;
        }
        
        const bottomNav = document.createElement('div');
        bottomNav.className = 'mobile-bottom-nav';
        
        const navItems = [
            { href: '/', icon: '🏠', label: 'Home' },
            { href: '/eda', icon: '📊', label: 'EDA' },
            { href: '/risk', icon: '🚨', label: 'Risk' },
            { href: '/forecast', icon: '📈', label: 'Forecast' },
            { href: '/inventory', icon: '📦', label: 'Inventory' }
        ];
        
        navItems.forEach(item => {
            const navItem = document.createElement('a');
            navItem.href = item.href;
            navItem.className = 'mobile-nav-item';
            
            // Check if current page
            if (window.location.pathname === item.href || 
                (item.href !== '/' && window.location.pathname.includes(item.href))) {
                navItem.classList.add('active');
            }
            
            navItem.innerHTML = `
                <span class="mobile-nav-icon">${item.icon}</span>
                <span>${item.label}</span>
            `;
            
            bottomNav.appendChild(navItem);
        });
        
        document.body.appendChild(bottomNav);
    }
    
    bindEvents() {
        // Menu button click
        if (this.menuBtn) {
            this.menuBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleSidebar();
            });
        }
        
        // Overlay click
        if (this.overlay) {
            this.overlay.addEventListener('click', () => {
                this.closeSidebar();
            });
        }
        
        // Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.closeSidebar();
            }
        });
        
        // Touch gestures for swipe
        this.bindTouchEvents();
        
        // Close sidebar when clicking nav items on mobile
        if (this.sidebar) {
            const navItems = this.sidebar.querySelectorAll('.cp-nav-item');
            navItems.forEach(item => {
                item.addEventListener('click', () => {
                    if (window.innerWidth <= 768) {
                        this.closeSidebar();
                    }
                });
            });
        }
    }
    
    bindTouchEvents() {
        // Swipe to open/close sidebar
        document.addEventListener('touchstart', (e) => {
            this.touchStartX = e.touches[0].clientX;
            this.touchStartY = e.touches[0].clientY;
        }, { passive: true });
        
        document.addEventListener('touchend', (e) => {
            if (!e.changedTouches[0]) return;
            
            const touchEndX = e.changedTouches[0].clientX;
            const touchEndY = e.changedTouches[0].clientY;
            const deltaX = touchEndX - this.touchStartX;
            const deltaY = touchEndY - this.touchStartY;
            
            // Only handle horizontal swipes
            if (Math.abs(deltaY) > Math.abs(deltaX)) return;
            
            const minSwipeDistance = 50;
            
            // Swipe right to open (from left edge)
            if (deltaX > minSwipeDistance && this.touchStartX < 50 && !this.isOpen) {
                this.openSidebar();
            }
            
            // Swipe left to close
            if (deltaX < -minSwipeDistance && this.isOpen) {
                this.closeSidebar();
            }
        }, { passive: true });
    }
    
    toggleSidebar() {
        if (this.isOpen) {
            this.closeSidebar();
        } else {
            this.openSidebar();
        }
    }
    
    openSidebar() {
        if (!this.sidebar || window.innerWidth > 768) return;
        
        this.sidebar.classList.add('mobile-open');
        this.overlay.classList.add('active');
        this.isOpen = true;
        
        // Update menu button
        if (this.menuBtn) {
            this.menuBtn.innerHTML = '✕';
            this.menuBtn.setAttribute('aria-label', 'Close navigation menu');
        }
        
        // Prevent body scroll
        document.body.style.overflow = 'hidden';
        
        // Focus management
        this.sidebar.setAttribute('tabindex', '-1');
        this.sidebar.focus();
    }
    
    closeSidebar() {
        if (!this.sidebar) return;
        
        this.sidebar.classList.remove('mobile-open');
        this.overlay.classList.remove('active');
        this.isOpen = false;
        
        // Update menu button
        if (this.menuBtn) {
            this.menuBtn.innerHTML = '☰';
            this.menuBtn.setAttribute('aria-label', 'Open navigation menu');
        }
        
        // Restore body scroll
        document.body.style.overflow = '';
        
        // Return focus to menu button
        if (this.menuBtn) {
            this.menuBtn.focus();
        }
    }
    
    handleResize() {
        const isMobile = window.innerWidth <= 768;
        
        if (!isMobile && this.isOpen) {
            this.closeSidebar();
        }
        
        // Show/hide mobile elements
        const mobileElements = document.querySelectorAll('.mobile-bottom-nav, .cp-topbar');
        mobileElements.forEach(el => {
            if (el) {
                el.style.display = isMobile ? 'flex' : 'none';
            }
        });
        
        // Adjust main content
        const main = document.querySelector('.cp-main');
        if (main) {
            if (isMobile) {
                main.style.marginLeft = '0';
                main.style.paddingBottom = '80px';
            } else {
                main.style.marginLeft = '';
                main.style.paddingBottom = '';
            }
        }
    }
}

// Mobile-specific chart optimizations
class MobileChartOptimizer {
    constructor() {
        this.init();
    }
    
    init() {
        this.optimizeCharts();
        this.handleOrientationChange();
        
        // Re-optimize on window resize
        window.addEventListener('resize', () => {
            setTimeout(() => this.optimizeCharts(), 100);
        });
    }
    
    optimizeCharts() {
        if (window.innerWidth > 768) return;
        
        // Optimize Chart.js defaults for mobile
        if (typeof Chart !== 'undefined') {
            Chart.defaults.responsive = true;
            Chart.defaults.maintainAspectRatio = false;
            Chart.defaults.plugins.legend.position = 'bottom';
            Chart.defaults.plugins.legend.labels.boxWidth = 10;
            Chart.defaults.plugins.legend.labels.padding = 10;
            Chart.defaults.plugins.legend.labels.font = {
                size: 11
            };
            Chart.defaults.plugins.tooltip.titleFont = {
                size: 12
            };
            Chart.defaults.plugins.tooltip.bodyFont = {
                size: 11
            };
        }
        
        // Adjust chart containers
        const chartContainers = document.querySelectorAll('.chart-container');
        chartContainers.forEach(container => {
            container.style.height = '250px';
            container.style.padding = '12px';
        });
    }
    
    handleOrientationChange() {
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                // Trigger chart resize
                if (typeof Chart !== 'undefined') {
                    Chart.helpers.each(Chart.instances, (instance) => {
                        instance.resize();
                    });
                }
                
                this.optimizeCharts();
            }, 500);
        });
    }
}

// Mobile table converter
class MobileTableConverter {
    constructor() {
        this.init();
    }
    
    init() {
        this.convertTables();
        window.addEventListener('resize', () => this.convertTables());
    }
    
    convertTables() {
        if (window.innerWidth > 768) return;
        
        const tables = document.querySelectorAll('.comparison-table');
        tables.forEach(table => this.convertTableToCards(table));
    }
    
    convertTableToCards(table) {
        if (table.dataset.converted === 'true') return;
        
        const rows = table.querySelectorAll('tbody tr');
        const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent);
        
        const cardsContainer = document.createElement('div');
        cardsContainer.className = 'mobile-cards-container';
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            const card = document.createElement('div');
            card.className = 'mobile-data-card';
            
            const header = document.createElement('div');
            header.className = 'mobile-data-header';
            header.textContent = cells[0]?.textContent || 'Item';
            card.appendChild(header);
            
            cells.forEach((cell, index) => {
                if (index === 0) return; // Skip first cell (used as header)
                
                const dataRow = document.createElement('div');
                dataRow.className = 'mobile-data-row';
                
                const label = document.createElement('span');
                label.className = 'mobile-data-label';
                label.textContent = headers[index] || `Field ${index}`;
                
                const value = document.createElement('span');
                value.className = 'mobile-data-value';
                value.textContent = cell.textContent;
                
                dataRow.appendChild(label);
                dataRow.appendChild(value);
                card.appendChild(dataRow);
            });
            
            cardsContainer.appendChild(card);
        });
        
        // Replace table with cards on mobile
        table.style.display = 'none';
        table.parentNode.insertBefore(cardsContainer, table.nextSibling);
        table.dataset.converted = 'true';
    }
}

// Touch gesture handler
class TouchGestureHandler {
    constructor() {
        this.init();
    }
    
    init() {
        this.addTouchFeedback();
        this.optimizeScrolling();
    }
    
    addTouchFeedback() {
        // Add touch feedback to interactive elements
        const interactiveElements = document.querySelectorAll(
            '.cp-kpi-card, .cp-chart-card, .cp-nav-item, button, .action-btn'
        );
        
        interactiveElements.forEach(element => {
            element.addEventListener('touchstart', () => {
                element.style.transform = 'scale(0.98)';
                element.style.transition = 'transform 0.1s ease';
            }, { passive: true });
            
            element.addEventListener('touchend', () => {
                setTimeout(() => {
                    element.style.transform = '';
                    element.style.transition = '';
                }, 100);
            }, { passive: true });
        });
    }
    
    optimizeScrolling() {
        // Smooth scrolling for mobile
        document.documentElement.style.scrollBehavior = 'smooth';
        
        // Prevent overscroll on iOS
        document.body.style.overscrollBehavior = 'none';
    }
}

// Initialize mobile features when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on mobile devices
    const isMobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    const isMobileViewport = window.innerWidth <= 768;
    
    if (isMobileDevice || isMobileViewport) {
        new MobileNavigation();
        new MobileChartOptimizer();
        new MobileTableConverter();
        new TouchGestureHandler();
        
        console.log('📱 Mobile optimizations initialized');
    }
});

// Export for use in other modules
window.ChainPulseMobile = {
    MobileNavigation,
    MobileChartOptimizer,
    MobileTableConverter,
    TouchGestureHandler
};