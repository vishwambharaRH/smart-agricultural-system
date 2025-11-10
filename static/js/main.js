// Main JavaScript for dashboard functionality

let updateInterval;
const UPDATE_RATE = 2000; // 2 seconds

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard initialized');
    updateConnectionStatus(false);
    startDataUpdates();
    loadStatistics();
    loadHistory();
});

// Start periodic data updates
function startDataUpdates() {
    updateData(); // Initial update
    updateInterval = setInterval(updateData, UPDATE_RATE);
}

// Fetch and update current sensor data
async function updateData() {
    try {
        const response = await fetch('/api/data');
        
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        
        const data = await response.json();
        
        // Update sensor displays
        updateSensorDisplay('temp', data.temp, '°C');
        updateSensorDisplay('hum', data.hum, '%');
        updateSensorDisplay('soil', data.soil, '');
        updateSensorDisplay('light', data.light, '');
        
        // Update pump status
        await updatePumpStatus();
        
        // Update connection status
        updateConnectionStatus(true);
        
    } catch (error) {
        console.error('Error updating data:', error);
        updateConnectionStatus(false);
    }
}

// Update individual sensor display
function updateSensorDisplay(sensor, value, unit) {
    const element = document.getElementById(`${sensor}-value`);
    if (element && value !== null && value !== undefined) {
        element.textContent = typeof value === 'number' ? value.toFixed(1) : value;
    } else if (element) {
        element.textContent = '--';
    }
}

// Update pump status indicator
async function updatePumpStatus() {
    try {
        const response = await fetch('/api/pump/status');
        const data = await response.json();
        
        const indicator = document.getElementById('pump-indicator');
        const statusText = document.getElementById('pump-status-text');
        
        if (data.is_on) {
            indicator.classList.add('on');
            statusText.textContent = 'ON';
            statusText.style.color = '#10b981';
        } else {
            indicator.classList.remove('on');
            statusText.textContent = 'OFF';
            statusText.style.color = '#6b7280';
        }
        
    } catch (error) {
        console.error('Error updating pump status:', error);
    }
}

// Control pump
async function pumpControl(action, duration = null) {
    try {
        const endpoint = action === 'on' ? '/api/pump/on' : '/api/pump/off';
        const body = duration ? { duration: duration } : {};
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });
        
        if (!response.ok) {
            throw new Error('Pump control failed');
        }
        
        const result = await response.json();
        console.log('Pump control:', result);
        
        // Show notification
        showNotification(result.message, 'success');
        
        // Immediate update
        await updatePumpStatus();
        
    } catch (error) {
        console.error('Error controlling pump:', error);
        showNotification('Failed to control pump', 'error');
    }
}

// Load and display statistics
async function loadStatistics() {
    try {
        const response = await fetch('/api/stats');
        const result = await response.json();
        
        if (result.success && result.data) {
            displayStatistics(result.data);
        }
        
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Display statistics
function displayStatistics(stats) {
    const statsContent = document.getElementById('stats-content');
    
    statsContent.innerHTML = `
        <div class="stat-item">
            <div class="stat-label">Total Records</div>
            <div class="stat-value">${stats.total_records || 0}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Avg Temperature</div>
            <div class="stat-value">${(stats.avg_temperature || 0).toFixed(1)}°C</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Avg Soil Moisture</div>
            <div class="stat-value">${(stats.avg_soil_moisture || 0).toFixed(0)}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Min Temp</div>
            <div class="stat-value">${(stats.min_temperature || 0).toFixed(1)}°C</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Max Temp</div>
            <div class="stat-value">${(stats.max_temperature || 0).toFixed(1)}°C</div>
        </div>
    `;
}

// Update connection status badge
function updateConnectionStatus(connected) {
    const badge = document.getElementById('connection-status');
    if (connected) {
        badge.textContent = 'Connected';
        badge.classList.remove('disconnected');
        badge.classList.add('connected');
    } else {
        badge.textContent = 'Disconnected';
        badge.classList.remove('connected');
        badge.classList.add('disconnected');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Simple console log for now - you can implement a toast notification
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // Optional: Add visual notification
    alert(message);
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (updateInterval) {
        clearInterval(updateInterval);
    }
});