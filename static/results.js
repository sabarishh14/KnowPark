document.addEventListener('DOMContentLoaded', () => {
    const resultsContainer = document.getElementById('resultsContainer');

    
    let results = JSON.parse(localStorage.getItem('analysisResults')) || {};

    if (Object.keys(results).length === 0) {
        resultsContainer.textContent = 'No results to display.';
        return;
    }

    Object.keys(results).forEach(key => {
        const value = results[key];
        const element = document.createElement('p');
        element.textContent = `${key}: ${value.toFixed(2)}`;
        resultsContainer.appendChild(element);
    });

    const evaluateButton = document.getElementById('evaluateButton');
    evaluateButton.addEventListener('click', () => {
        fetch('http://127.0.0.1:5000/predict-parkinsons', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(results)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            window.location.href = `/prediction`;
        })
        .catch(error => {
            console.error('Error:', error);
            resultsContainer.textContent = `Error: ${error.message}`;
        });
    
    });
    
});
