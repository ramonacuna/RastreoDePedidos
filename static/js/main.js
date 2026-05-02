document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('tracking-form');
    const input = document.getElementById('tracking-input');
    const spinner = document.getElementById('loading-spinner');
    const errorMsg = document.getElementById('error-message');
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

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const trackingNumber = input.value.trim();
        
        if (!trackingNumber) return;

        // Reset UI
        errorMsg.classList.add('hidden');
        resultsSection.classList.add('hidden');
        spinner.classList.remove('hidden');

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
        }
    });

    function showError(message) {
        errorMsg.textContent = message;
        errorMsg.classList.remove('hidden');
    }

    function renderPackageData(trackingNumber, data) {
        pkgId.textContent = trackingNumber;
        pkgOrigin.textContent = data.origin;
        pkgDestination.textContent = data.destination;
        
        // Format date slightly
        const dateObj = new Date(data.estimatedDelivery + "T00:00:00");
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        pkgEstimate.textContent = dateObj.toLocaleDateString('es-ES', options).replace(/^\w/, c => c.toUpperCase());

        // Status styling
        const statusNormalized = data.status.toLowerCase().replace(/\s+/g, '-');
        pkgStatus.textContent = data.status;
        pkgStatus.className = `status-badge status-${statusNormalized}`;

        // Progress bar logic based on status
        let progress = 0;
        if (statusNormalized === 'entregado') progress = 100;
        else if (statusNormalized === 'en-reparto') progress = 80;
        else if (statusNormalized === 'en-tránsito') progress = 50;
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
            li.style.animationDelay = `${index * 0.15}s`;

            li.innerHTML = `
                <div class="timeline-date">${event.date}</div>
                <div class="timeline-content">
                    <div class="timeline-location">📍 ${event.location}</div>
                    <div class="timeline-desc">${event.description}</div>
                </div>
            `;
            pkgEvents.appendChild(li);
        });
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
