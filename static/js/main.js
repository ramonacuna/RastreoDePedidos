document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('tracking-form');
    const input = document.getElementById('tracking-input');
    const spinner = document.getElementById('loading-spinner');
    const errorMsg = document.getElementById('error-message');
    const validationMsg = document.getElementById('validation-message');
    const resultsSection = document.getElementById('results-section');
    
    // UI Elements for Data
    const pkgId = document.getElementById('pkg-id');
    const pkgStatus = document.getElementById('pkg-status');
    const pkgOrigin = document.getElementById('pkg-origin');
    const pkgDestination = document.getElementById('pkg-destination');
    const pkgEstimate = document.getElementById('pkg-estimate');
    const pkgEvents = document.getElementById('pkg-events');
    const pkgProgress = document.getElementById('pkg-progress');
    const truckIcon = document.querySelector('.truck-icon');
    const searchBtn = document.getElementById('search-btn');
    const clearBtn = document.getElementById('clear-btn');
    const copyBtn = document.getElementById('copy-btn');
    const recentSearches = document.getElementById('recent-searches');
    const recentList = document.getElementById('recent-list');

    // Initialize Recent Searches
    renderRecentSearches();

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const trackingNumber = input.value.trim();
        
        if (!trackingNumber) {
            validationMsg.classList.remove('hidden');
            input.classList.add('validation-error');
            setTimeout(() => input.classList.remove('validation-error'), 500);
            return;
        }

        // Reset UI
        errorMsg.classList.add('hidden');
        resultsSection.classList.add('hidden');
        spinner.classList.remove('hidden');
        searchBtn.disabled = true;
        searchBtn.querySelector('span').textContent = 'Buscando...';

        try {
            // Artificial delay for smooth UX transition
            await new Promise(resolve => setTimeout(resolve, 800));

            const response = await fetch(`/api/track/${trackingNumber}`);
            const data = await response.json();

            if (data.success) {
                renderPackageData(trackingNumber, data.data);
                resultsSection.classList.remove('hidden');
            } else {
                showError(data.message);
            }
        } catch (error) {
            showError("Hubo un error al conectar con el servidor. Intenta nuevamente.");
        } finally {
            spinner.classList.add('hidden');
            searchBtn.disabled = false;
            searchBtn.querySelector('span').textContent = 'Buscar';
        }
    });

    // Clear input functionality and hide validation
    input.addEventListener('input', () => {
        validationMsg.classList.add('hidden');
        input.classList.remove('validation-error');
        
        if (input.value.length > 0) {
            clearBtn.classList.remove('hidden');
        } else {
            clearBtn.classList.add('hidden');
        }
    });

    clearBtn.addEventListener('click', () => {
        input.value = '';
        clearBtn.classList.add('hidden');
        input.focus();
    });

    // Copy to clipboard
    copyBtn.addEventListener('click', async () => {
        const textToCopy = pkgId.textContent;
        try {
            await navigator.clipboard.writeText(textToCopy);
            copyBtn.classList.add('copied');
            const originalTitle = copyBtn.getAttribute('title');
            copyBtn.setAttribute('title', '¡Copiado!');
            
            setTimeout(() => {
                copyBtn.classList.remove('copied');
                copyBtn.setAttribute('title', originalTitle);
            }, 2000);
        } catch (err) {
            console.error('Error al copiar: ', err);
        }
    });

    function saveRecentSearch(id) {
        let recents = JSON.parse(localStorage.getItem('recentTracking')) || [];
        // Remove if already exists and add to front
        recents = recents.filter(item => item !== id);
        recents.unshift(id);
        // Keep last 3
        recents = recents.slice(0, 3);
        localStorage.setItem('recentTracking', JSON.stringify(recents));
        renderRecentSearches();
    }

    function renderRecentSearches() {
        const recents = JSON.parse(localStorage.getItem('recentTracking')) || [];
        if (recents.length === 0) {
            recentSearches.classList.add('hidden');
            return;
        }

        recentSearches.classList.remove('hidden');
        recentList.innerHTML = '';
        recents.forEach(id => {
            const pill = document.createElement('div');
            pill.className = 'recent-pill';
            pill.textContent = id;
            pill.onclick = () => {
                input.value = id;
                clearBtn.classList.remove('hidden');
                form.dispatchEvent(new Event('submit'));
            };
            recentList.appendChild(pill);
        });
    }

    function showError(message) {
        errorMsg.textContent = message;
        errorMsg.classList.remove('hidden');
    }

    function renderPackageData(trackingNumber, data) {
        pkgId.textContent = trackingNumber;
        pkgOrigin.textContent = data.origin;
        pkgDestination.textContent = data.destination;
        
        // Update document title
        document.title = `${trackingNumber} - Rastreo de Envío`;
        
        // Save to recent searches
        saveRecentSearch(trackingNumber);
        
        // Format date slightly
        const dateObj = new Date(data.estimatedDelivery + "T00:00:00");
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        pkgEstimate.textContent = dateObj.toLocaleDateString('es-ES', options).replace(/^\w/, c => c.toUpperCase());

        // Status styling
        const statusNormalized = data.status.toLowerCase().replace(/\s+/g, '-');
        pkgStatus.textContent = data.status;
        pkgStatus.className = `status-badge status-${statusNormalized}`;
        
        // Delayed Delivery Indicator
        const delayContainer = document.getElementById('delay-badge-container');
        const today = new Date();
        today.setHours(0,0,0,0);
        if (dateObj < today && statusNormalized !== 'entregado') {
            delayContainer.innerHTML = '<span class="delay-badge">⚠️ Entrega retrasada</span>';
        } else {
            delayContainer.innerHTML = '';
        }

        // Progress bar logic based on status
        let progress = 0;
        if (statusNormalized === 'entregado') progress = 100;
        else if (statusNormalized === 'en-reparto') progress = 66;
        else if (statusNormalized === 'en-tránsito') progress = 33;
        else progress = 10;

        // Handle responsive logic for progress
        if (window.innerWidth <= 640) {
            // Vertical bar
            pkgProgress.style.width = '100%';
            pkgProgress.style.height = '0%';
            truckIcon.style.left = '-12px';
            truckIcon.style.top = '0%';
            
            setTimeout(() => {
                pkgProgress.style.height = `${progress}%`;
                truckIcon.style.top = `calc(${progress}% - 12px)`;
            }, 100);
        } else {
            // Horizontal bar
            pkgProgress.style.height = '100%';
            pkgProgress.style.width = '0%';
            truckIcon.style.top = '-12px';
            truckIcon.style.left = '0%';

            setTimeout(() => {
                pkgProgress.style.width = `${progress}%`;
                truckIcon.style.left = `calc(${progress}% - 12px)`;
            }, 100);
        }

        // Render Events History
        pkgEvents.innerHTML = '';
        data.events.forEach((event, index) => {
            const li = document.createElement('li');
            li.className = 'timeline-item';
            li.style.animationDelay = `${index * 0.1}s`;
            
            if (index >= 5) {
                li.classList.add('hidden-event');
            }

            const dateDiv = document.createElement('div');
            dateDiv.className = 'timeline-date';
            dateDiv.textContent = event.date;

            const contentDiv = document.createElement('div');
            contentDiv.className = 'timeline-content';

            const locationDiv = document.createElement('div');
            locationDiv.className = 'timeline-location';
            locationDiv.textContent = `📍 ${event.location}`;

            const descDiv = document.createElement('div');
            descDiv.className = 'timeline-desc';
            descDiv.textContent = event.description;

            contentDiv.appendChild(locationDiv);
            contentDiv.appendChild(descDiv);
            li.appendChild(dateDiv);
            li.appendChild(contentDiv);
            pkgEvents.appendChild(li);
        });
        
        // Pagination logic
        if (data.events.length > 5) {
            const btnContainer = document.createElement('div');
            btnContainer.className = 'show-all-container';
            const btn = document.createElement('button');
            btn.className = 'show-all-btn';
            btn.textContent = `Ver todos (${data.events.length})`;
            btn.onclick = () => {
                const hiddenEvents = pkgEvents.querySelectorAll('.hidden-event');
                hiddenEvents.forEach(el => el.classList.remove('hidden-event'));
                btnContainer.remove();
            };
            btnContainer.appendChild(btn);
            pkgEvents.appendChild(btnContainer);
        }
    }

    // Handle resize for progress bar correctness
    window.addEventListener('resize', () => {
        if (!resultsSection.classList.contains('hidden')) {
            const trackingNumber = input.value.trim();
            if(trackingNumber) {
                // Re-trigger progress animation on resize
                 form.dispatchEvent(new Event('submit'));
            }
        }
    });
});
