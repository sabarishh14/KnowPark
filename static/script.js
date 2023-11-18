document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('uploadArea');
    const uploadBtn = document.getElementById('uploadBtn');
    const fileInput = document.getElementById('fileInput');
    const filesList = document.getElementById('filesList');
    

    // Click the hidden file input when the 'Browse' link is clicked
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // Handle file input change
    fileInput.addEventListener('change', (event) => {
        const files = event.target.files;
        displayFiles(files);
    });

    // Display the selected files
    function displayFiles(files) {
        filesList.innerHTML = ''; // Clear the list

        Array.from(files).forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.textContent = file.name; // Add other file details as needed
            filesList.appendChild(fileItem);
        });
    }

    // Handle the file upload button
    uploadBtn.addEventListener('click', () => {
        // Here you would normally handle the actual file upload.
        alert('Files ready for upload!');
    });
});
