// Make sure to include this script in your index.html file
document.getElementById('uploadButton').addEventListener('click', function() {
    var audioFile = document.getElementById('audioUpload').files[0];
    var formData = new FormData();
    formData.append('file', audioFile);

    fetch('http://127.0.0.1:5000/analyze-audio', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Received data:', data);  // Log data to console
        localStorage.setItem('analysisResults', JSON.stringify(data));
        window.location.href = '/results'; // Redirect to the results page
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
