let gaugeChart = null;

document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form values
    const formData = {
        latitude: document.getElementById('latitude').value,
        longitude: document.getElementById('longitude').value,
        depth: document.getElementById('depth').value,
        mag: document.getElementById('mag').value,
        nst: document.getElementById('nst').value,
        gap: document.getElementById('gap').value,
        dmin: document.getElementById('dmin').value,
        rms: document.getElementById('rms').value,
        horizontalError: document.getElementById('horizontalError').value,
        depthError: document.getElementById('depthError').value,
        magError: document.getElementById('magError').value
    };

    try {
        // Hide error container
        document.getElementById('errorContainer').classList.add('hidden');

        // Make prediction request
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Prediction failed');
        }

        const result = await response.json();

        // Update results
        document.getElementById('magnitude').textContent = result.magnitude;
        document.getElementById('strength').textContent = result.strength;
        document.getElementById('probability').textContent = result.probability;
        document.getElementById('summary').textContent = result.summary;

        // Update strength card color
        const strengthCard = document.getElementById('strengthCard');
        const colorMap = {
            'green': '#51cf66',
            'yellow': '#ffd43b',
            'orange': '#ff922b',
            'red': '#ff6b6b'
        };
        strengthCard.style.borderLeftColor = colorMap[result.color];

        // Update gauge chart
        updateGauge(result.magnitude, result.color);

        // Show results
        document.getElementById('resultsContainer').classList.remove('hidden');

    } catch (error) {
        console.error('Error:', error);
        document.getElementById('errorMessage').textContent = `Error: ${error.message}`;
        document.getElementById('errorContainer').classList.remove('hidden');
    }
});

// Reset form
document.querySelector('.btn-clear').addEventListener('click', function() {
    document.getElementById('resultsContainer').classList.add('hidden');
    document.getElementById('errorContainer').classList.add('hidden');
});

function updateGauge(magnitude, color) {
    const ctx = document.getElementById('gaugeChart').getContext('2d');
    
    // Destroy old chart if exists
    if (gaugeChart) {
        gaugeChart.destroy();
    }

    const colorMap = {
        'green': '#51cf66',
        'yellow': '#ffd43b',
        'orange': '#ff922b',
        'red': '#ff6b6b'
    };

    // Create gauge chart
    gaugeChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Magnitude', 'Remaining'],
            datasets: [{
                data: [magnitude, 10 - magnitude],
                backgroundColor: [colorMap[color], '#e0e0e0'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            if (context.dataIndex === 0) {
                                return 'Magnitude: ' + magnitude.toFixed(2);
                            }
                        }
                    }
                },
                centerText: {
                    display: true
                }
            }
        },
        plugins: [{
            id: 'centerText',
            beforeDatasetsDraw(chart) {
                const {ctx, chartArea: {left, top, width, height}} = chart;
                ctx.save();

                const x = left + width / 2;
                const y = top + height / 2;
                
                // Draw text
                ctx.font = '30px Arial';
                ctx.fontWeight = 'bold';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillStyle = '#333';
                ctx.fillText(magnitude.toFixed(2), x, y);
                
                ctx.font = '14px Arial';
                ctx.fillStyle = '#999';
                ctx.fillText('Magnitude', x, y + 25);
                ctx.restore();
            }
        }]
    });
}
