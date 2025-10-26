const form = document.getElementById('infographicForm');
const submitBtn = document.getElementById('submitBtn');
const resultsDiv = document.getElementById('results');
const validationMessage = document.getElementById('validationMessage');
const articleNameInput = document.getElementById('article_name');
const articleTextInput = document.getElementById('article_text');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const articleName = articleNameInput.value.trim();
    const articleText = articleTextInput.value.trim();
    
    validationMessage.innerHTML = '';
    
    // Validation checks
    if (!articleName && !articleText) {
        validationMessage.innerHTML = '<div class="validation-error">⚠️ Please fill in both Article Name and Article Content fields before generating.</div>';
        articleNameInput.focus();
        return;
    }
    
    if (!articleName) {
        validationMessage.innerHTML = '<div class="validation-error">⚠️ Please enter an Article Name (minimum 3 characters).</div>';
        articleNameInput.focus();
        return;
    }
    
    if (articleName.length < 3) {
        validationMessage.innerHTML = '<div class="validation-error">⚠️ Article Name must be at least 3 characters long.</div>';
        articleNameInput.focus();
        return;
    }
    
    if (!articleText) {
        validationMessage.innerHTML = '<div class="validation-error">⚠️ Please enter Article Content (minimum 50 characters).</div>';
        articleTextInput.focus();
        return;
    }
    
    if (articleText.length < 50) {
        validationMessage.innerHTML = `<div class="validation-error">⚠️ Article Content must be at least 50 characters long. Currently: ${articleText.length} characters.</div>`;
        articleTextInput.focus();
        return;
    }
    
    // Show loading state
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ Generating...';
    
    resultsDiv.innerHTML = `
        <div class="card loading">
            <div class="spinner"></div>
            <h3>Creating your infographic...</h3>
            <p>This may take 10-30 seconds</p>
        </div>
    `;

    const formData = new FormData(form);

    try {
        const response = await fetch('/run', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.files && Object.keys(result.files).length > 0) {
            // Success - build download links
            let html = `
                <div class="card">
                    <div class="success-message">
                        <h2>✅ Success!</h2>
                        <p>Your infographic has been generated successfully</p>
                    </div>
                    <div class="download-grid">
            `;

            const fileIcons = {
                html: '🌐',
                png: '📊',
                pdf: '📄'
            };

            const fileDescriptions = {
                html: 'Interactive web version',
                png: 'Chart image',
                pdf: 'Printable document'
            };

            for (const [fileType, filePath] of Object.entries(result.files)) {
                const fileName = filePath.replace('generated/', '');
                html += `
                    <a href="/download/${result.article_name}/${fileType}" 
                       class="download-card" 
                       target="_blank">
                        <div class="download-icon">${fileIcons[fileType]}</div>
                        <h3>${fileType.toUpperCase()}</h3>
                        <p>${fileDescriptions[fileType]}</p>
                        <small>${fileName}</small>
                    </a>
                `;
            }

            html += `
                    </div>
                </div>
            `;

            resultsDiv.innerHTML = html;
        } else if (result.error) {
            resultsDiv.innerHTML = `
                <div class="card">
                    <div class="error-message">
                        <h3>❌ Error</h3>
                        <p>${result.error}</p>
                    </div>
                </div>
            `;
        } else {
            resultsDiv.innerHTML = `
                <div class="card">
                    <div class="error-message">
                        <h3>⚠️ No files generated</h3>
                        <p>Please try again or check your input</p>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        resultsDiv.innerHTML = `
            <div class="card">
                <div class="error-message">
                    <h3>❌ Network Error</h3>
                    <p>${error.message}</p>
                </div>
            </div>
        `;
    } finally {
        // Re-enable button
        submitBtn.disabled = false;
        submitBtn.textContent = '✨ Generate Infographic';
    }
});

function clearForm() {
    // Reset the form fields
    form.reset();
    
    // Clear the results area
    resultsDiv.innerHTML = '';
    
    // Clear validation messages
    validationMessage.innerHTML = '';
    
    // Focus on the first input field
    articleNameInput.focus();
}
