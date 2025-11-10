// Chart.js configuration and data loading

let tempChart = null;
let soilChart = null;

// Load historical data and render charts
async function loadHistory() {
    const limit = document.getElementById('data-range').value;
    
    try {
        const response = await fetch(`/api/history?limit=${limit}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch history');
        }
        
        const data = await response.json();
        
        if (data.length === 0) {
            console.log('No historical data available');
            return;
        }
        
        // Extract data for charts
        const labels = data.map(d => formatTimestamp(d.timestamp));
        const temperatures = data.map(d => parseFloat(d.temp) || 0);
        const humidity = data.map(d => parseFloat(d.humidity) || 0);
        const soilMoisture = data.map(d => parseInt(d.soil_moisture) || 0);
        const lightLevels = data.map(d => parseInt(d.light_level) || 0);
        
        // Render charts
        renderTemperatureChart(labels, temperatures, humidity);
        renderSoilChart(labels, soilMoisture, lightLevels);
        
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Format timestamp for chart labels
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Render temperature and humidity chart
function renderTemperatureChart(labels, temperatures, humidity) {
    const ctx = document.getElementById('tempChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (tempChart) {
        tempChart.destroy();
    }
    
    tempChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: temperatures,
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Humidity (%)',
                    data: humidity,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Temperature & Humidity Over Time',
                    font: {
                        size: 16,
                        weight: 'bold'
                    },
                    color: '#667eea'
                },
                legend: {
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
    
    // Set chart container height
    document.getElementById('tempChart').parentElement.style.height = '400px';
}

// Render soil moisture and light level chart
function renderSoilChart(labels, soilMoisture, lightLevels) {
    const ctx = document.getElementById('soilChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (soilChart) {
        soilChart.destroy();
    }
    
    soilChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Soil Moisture',
                    data: soilMoisture,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    yAxisID: 'y'
                },
                {
                    label: 'Light Level',
                    data: lightLevels,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Soil Moisture & Light Level Over Time',
                    font: {
                        size: 16,
                        weight: 'bold'
                    },
                    color: '#667eea'
                },
                legend: {
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Soil Moisture'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Light Level'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
    
    // Set chart container height
    document.getElementById('soilChart').parentElement.style.height = '400px';
}

// Auto-refresh charts every 5 minutes
setInterval(() => {
    loadHistory();
}, 300000);