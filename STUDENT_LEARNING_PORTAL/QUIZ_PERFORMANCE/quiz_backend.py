import http.server
import socketserver
import cgi
import joblib
import numpy as np
import json

# Load the trained model
model = joblib.load('recommendation_model.pkl')

# Map categorical values to numerical values (for the model to work)
device_type_mapping = {'Mobile': 0, 'Laptop': 1, 'Tablet': 2}
engagement_level_mapping = {'Active': 0, 'Inactive': 1}

class RecommendationHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        # Handle preflight OPTIONS request for CORS
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        content_type, pdict = cgi.parse_header(self.headers['Content-Type'])

        if content_type == 'application/json':
            try:
                length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(length)
                data = json.loads(post_data.decode())  # Read the JSON data

                # Extract feature values and convert them to float
                try:
                    time_spent_modules = float(data['time_spent_modules'])
                    device_type = data['device_type']
                    engagement_level = data['engagement_level']
                    participation_forums = float(data['participation_forums'])
                    assignment_submissions = float(data['assignment_submissions'])

                    # Convert device_type and engagement_level to numerical values
                    if device_type not in device_type_mapping:
                        raise ValueError("Invalid device_type")
                    if engagement_level not in engagement_level_mapping:
                        raise ValueError("Invalid engagement_level")

                    device_type_encoded = device_type_mapping[device_type]
                    engagement_level_encoded = engagement_level_mapping[engagement_level]

                except (ValueError, KeyError) as e:
                    error_msg = f"Invalid input data: {str(e)}"
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': error_msg}).encode())
                    return

                # Prepare feature array for prediction
                features = np.array([[time_spent_modules, device_type_encoded, engagement_level_encoded,
                                      participation_forums, assignment_submissions]])

                # Model prediction
                try:
                    prediction = model.predict(features)
                    quiz_performance = prediction[0]  # This will be the predicted quiz performance average

                    # Return prediction result (Quiz_Performance_Average)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()

                    # Send the prediction in JSON format
                    response = {
                        "quiz_performance_average": quiz_performance
                    }
                    self.wfile.write(json.dumps(response).encode())

                except Exception as e:
                    error_msg = f"Prediction failed: {str(e)}"
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': error_msg}).encode())
                    return

            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': error_msg}).encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Unsupported Content-Type'}).encode())

# Start the server
PORT = 8000
Handler = RecommendationHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server running on port {PORT}")
    httpd.serve_forever()
