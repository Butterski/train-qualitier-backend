# Train Qualitier Backend
Train Qualitier is a cutting-edge application aimed at enhancing passengers' travel experiences by monitoring and assessing the quality of train rides through real-time data collection from various sensors.

## Backend Overview
The backend is powered by Python, utilizing Flask as its web framework to ensure swift and efficient handling of the application logic and data flow. It facilitates sensor communication and data processing, storing the collected data in a lightweight SQLite3 database.

## Getting Started
To get the backend running on your local machine, follow these steps:

### Prerequisites
- Python 3.6+
- pip

### Installation
1. Clone the repository to your local machine:

`git clone https://your-repository-url.git`

2. Navigate to the backend directory:

`cd path/to/backend`

3. Install the required Python packages:

`pip install -r requirements.txt`

4. Initialize the database and venv:

`python setup.py`

### Running the Application
Start the Flask application:

`python app.py`

This script initializes the backend server on `http://localhost:5000`, ready to receive data from the sensors and serve the frontend application.

### Deployment
For production environments:

- Set up an isolated virtual environment.
- Utilize Nginx as a reverse proxy for enhanced security and communication between the frontend and backend.
- Ensure the application is running in a secure and scalable environment.

#### Technology Stack
- Python & Flask: Ensures efficient processing and simplicity in implementing complex application logic.
- SQLite3: Provides a fast, simple, and reliable database solution for small to medium-sized applications.
- Nginx: Acts as a robust reverse proxy to enhance security and facilitate communication between frontend and backend components.

For more information on the complete system architecture and frontend setup, refer to the main project documentation.

This project focuses on simplicity, efficiency, and providing a seamless experience for monitoring train ride quality. Your contributions and feedback are welcome to improve the application further.