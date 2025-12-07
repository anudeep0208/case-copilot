async function generateTestCases() {
    const storyID = document.getElementById('storyID').value;
    const email = document.getElementById('userEmail').value;
    const testType = document.getElementById('testType').value;
    const criteria = document.getElementById('acceptanceCriteria').value;
    const loader = document.getElementById('loader');
    const downloadSection = document.getElementById('downloadSection');

    // Basic Validation
    // Validation: User Story ID (Required, 12 Alphanumeric)
    if (!storyID) {
        alert("User Story ID is required.");
        return;
    }
    const storyIdRegex = /^[a-zA-Z0-9]{1,12}$/;
    if (!storyIdRegex.test(storyID)) {
        alert("User Story ID should be alphanumeric characters.");
        return;
    }

    // Validation: User Email (Optional, Format)
    if (email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert("Please enter a valid email address.");
            return;
        }
    }

    // Validation: Acceptance Criteria (Required)
    if (!criteria) {
        alert("Acceptance Criteria is required.");
        return;
    }

    // Default Test Type to "Functional" if empty
    const finalTestType = testType || "Functional";

    // Show Loader
    loader.classList.remove('hidden');
    downloadSection.classList.add('hidden');

    try {
        // Call Python Backend
        const response = await fetch('[http://127.0.0.1:8000/generate](http://127.0.0.1:8000/generate)', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                story_id: storyID,
                email: email,
                test_type: finalTestType,
                criteria: criteria
            })
        });

        const data = await response.json();

        if (data.status === "success") {
            // Prepare CSV for download
            const blob = new Blob([data.csv_data], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const downloadLink = document.getElementById('downloadLink');

            downloadLink.href = url;
            downloadLink.download = `${storyID}_TestCases.csv`;

            // Show Download Section
            downloadSection.classList.remove('hidden');
        } else {
            alert("Error generating tests.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to connect to the backend.");
    } finally {
        loader.classList.add('hidden');
    }
}

function handleDownload() {
    // Wait a brief moment to ensure download starts, then reset
    setTimeout(() => {
        alert("Success! Your test cases have been downloaded.");
        // Reset the page
        location.reload();
    }, 1000);
}

function resetPage() {
    // Clear inputs
    document.getElementById('storyID').value = '';
    document.getElementById('userEmail').value = '';
    document.getElementById('acceptanceCriteria').value = '';

    // Reset dropdown to first option
    document.getElementById('testType').selectedIndex = 0;

    // Hide download section and loader
    document.getElementById('downloadSection').classList.add('hidden');
    document.getElementById('loader').classList.add('hidden');
}
