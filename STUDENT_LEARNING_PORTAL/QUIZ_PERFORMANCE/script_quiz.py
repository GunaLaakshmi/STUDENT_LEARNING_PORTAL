document.getElementById("predictionForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Collect the form data
    const timeSpentModules = document.getElementById("time_spent_modules").value;
    const deviceType = document.getElementById("device_type").value;
    const engagementLevel = document.getElementById("engagement_level").value;
    const participationForums = document.getElementById("participation_forums").value;
    const assignmentSubmissions = document.getElementById("assignment_submissions").value;

    // Validate input data
    if (!timeSpentModules || !participationForums || !assignmentSubmissions) {
        document.getElementById("quizPerformanceAverage").innerText = "Please fill out all required fields.";
        return;
    }

    // Prepare the data for sending to the backend as JSON
    const data = {
        time_spent_modules: timeSpentModules,
        device_type: deviceType,
        engagement_level: engagementLevel,
        participation_forums: participationForums,
        assignment_submissions: assignmentSubmissions
    };

    console.log("Sending data:", data);  // Log the data to be sent to the backend for debugging

    // Make the POST request to the backend with JSON content
    fetch('http://localhost:8000', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Set the content type to application/json
        },
        body: JSON.stringify(data)  // Convert the data to JSON
    })
    .then(response => response.json())  // Handle JSON response from backend
    .then(data => {
        console.log("Response from server:", data);  // Log the response from the backend for debugging
        // Check if the backend returns the predicted quiz performance
        if (data.quiz_performance_average) {
            document.getElementById("quizPerformanceAverage").innerText = `Quiz Performance Average Score: ${data.quiz_performance_average}`;
            document.getElementById("predictionResult").style.display = 'block'; // Show the result section
        } else {
            document.getElementById("quizPerformanceAverage").innerText = "Prediction failed. Please check the input values.";
        }
    })
    .catch(error => {
        // Handle errors and display an error message
        document.getElementById("quizPerformanceAverage").innerText = "Error: " + error.message;
    });
});
