// CONFIGURATION
const API_URL = 'http://127.0.0.1:8000/generate';

// DOM ELEMENTS
const generateBtn = document.getElementById('generateBtn');
const resetBtn = document.getElementById('resetBtn');
const downloadLink = document.getElementById('downloadLink');
const statusMsg = document.getElementById('statusMessage');

// EVENT LISTENERS (Better for maintainability)
document.addEventListener('DOMContentLoaded', () => {
    generateBtn.addEventListener('click', generateTestCases);
    resetBtn.addEventListener('click', resetPage);
    downloadLink.addEventListener('click', () => {
        showStatus("Test cases downloaded successfully!", "success");
        // We DO NOT reload the page here. Let the user keep their data.
    });
});

// UTILITY: Show User Feedback
function showStatus(message, type) {
    statusMsg.textContent = message;
    statusMsg.className = 'status-msg'; // Reset class
    if (type === 'error') statusMsg.classList.add('status-error');
    if (type === 'success') statusMsg.classList.add('status-success');
}

async function generateTestCases() {
    const storyID = document.getElementById('storyID').value.trim();
    const email = document.getElementById('userEmail').value.trim();
    const testType = document.getElementById('testType').value;
    const criteria = document.getElementById('acceptanceCriteria').value.trim();
    const loader = document.getElementById('loader');
    const downloadSection = document.getElementById('downloadSection');

    // CLEAR PREVIOUS STATUS
    statusMsg.className = 'status-msg';

    // VALIDATION
    if (!storyID) return showStatus("User Story ID is required.", "error");
    if (!/^[a-zA-Z0-9]{1,12}$/.test(storyID)) return showStatus("Invalid Story ID format.", "error");
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return showStatus("Invalid email address.", "error");
    if (!criteria) return showStatus("Acceptance Criteria is required.", "error");

    const finalTestType = testType || "Functional";

    // UI STATE: LOADING
    loader.classList.remove('hidden');
    downloadSection.classList.add('hidden');
    generateBtn.disabled = true; // Prevent double clicks
    generateBtn.style.opacity = "0.7";

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                story_id: storyID,
                email: email,
                test_type: finalTestType,
                criteria: criteria
            })
        });

        // Check if server actually responded nicely
        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }

        const data = await response.json();

        if (data.status === "success") {
            // Prepare CSV
            const blob = new Blob([data.csv_data], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);

            downloadLink.href = url;
            downloadLink.download = `${storyID}_TestCases.csv`;

            downloadSection.classList.remove('hidden');
            showStatus("Generation Complete! Ready to download.", "success");
        } else {
            showStatus("The agent encountered an issue generating tests.", "error");
        }
    } catch (error) {
        console.error("Error:", error);
        showStatus("Failed to connect to the AI Agent. Check backend.", "error");
    } finally {
        // UI STATE: RESET
        loader.classList.add('hidden');
        generateBtn.disabled = false;
        generateBtn.style.opacity = "1";
    }
}

function resetPage() {
    document.getElementById('storyID').value = '';
    document.getElementById('userEmail').value = '';
    document.getElementById('acceptanceCriteria').value = '';
    document.getElementById('testType').selectedIndex = 0;
    document.getElementById('downloadSection').classList.add('hidden');
    statusMsg.className = 'status-msg'; // Hide status
}