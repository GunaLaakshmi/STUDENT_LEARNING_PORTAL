// Select the form and result elements
const form = document.getElementById('predictionForm');
const resultElement = document.getElementById('engagementLevel');

// Handle form submission
form.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from reloading the page

    // Collect form data
    const data = {
        login_frequency: parseFloat(document.getElementById('login_frequency').value),
        time_spent_modules: parseFloat(document.getElementById('time_spent_modules').value),
        participation_forums: parseFloat(document.getElementById('participation_forums').value),
        quiz_performance_average: parseFloat(document.getElementById('quiz_performance_average').value),
        assignment_submissions: parseFloat(document.getElementById('assignment_submissions').value),
    };

    // Validate form data before sending
    if (
        isNaN(data.login_frequency) ||
        isNaN(data.time_spent_modules) ||
        isNaN(data.participation_forums) ||
        isNaN(data.quiz_performance_average) ||
        isNaN(data.assignment_submissions)
    ) {
        resultElement.innerText = 'Error: Please fill in all fields with valid values';
        return;
    }
    console.log('Response body:', result);

    // Log the data being sent to the backend (debugging)
    console.log('Sending data to backend:', data);

    // Send the data to the backend
    fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            // Log the response status for debugging
            console.log('Response status:', response.status);

            if (!response.ok) {
                throw new Error(`Network response was not ok. Status: ${response.status}`);
            }
            return response.json();
        })
        .then((result) => {
            // Log the received result (debugging)
            console.log('Received result from backend:', result);

            // Update the result section with the prediction
            if (result && result.predicted_engagement_level) {
                resultElement.innerText = `Predicted Engagement Level: ${result.predicted_engagement_level}`;
            } else {
                resultElement.innerText = 'Error: Unexpected response format';
                console.error('Unexpected response format:', result);
            }
        })
        .catch((error) => {
            // Log the error (debugging)
            console.error('Error occurred:', error);

            // Update the result element with an error message
            resultElement.innerText = 'Error: Unable to get prediction. Please try again later.';
        });
});
