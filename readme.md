
# Real Estate Assistant Application

This application is designed to facilitate real estate transactions and inquiries, leveraging a Flask-based web service to interact with users for property searches, viewings, and more.

https://www.loom.com/share/96699d257afd4cca91de38cf4f639a6f?sid=a09c40fc-0839-4ef8-946a-0b9658d04d43

## Getting Started

These instructions will guide you through setting up and running the application on your local machine.

### Prerequisites

Before you begin, ensure you have Python installed on your system. This application is tested with Python 3.8+.

### Setting up a Virtual Environment

A virtual environment is recommended to manage dependencies for your application. Here's how to set it up on various operating systems:

#### For Windows:

```bash
# Navigate to the project directory
cd path/to/your/project

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

#### For macOS and Linux:

```bash
# Navigate to the project directory
cd path/to/your/project

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### Installing Dependencies

With your virtual environment activated, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

### Environment Variables

Set the necessary environment variables. You can use a `.env` file or export them directly into your environment. These typically include:

- `OPENAI_API_KEY`
- `RAPID_API_KEY`
- `WEBHOOK_URL`
- `CUSTOM_API_KEY`

### Core Functions

The application includes several core functions:

- **Property Search Assistance**: Facilitates searching for real estate listings based on user input.
- **Scheduling Property Viewings**: Allows users to schedule property viewings and handles the necessary arrangements.
- **Lead Capture and Management**: Captures and manages potential client information for follow-up and marketing purposes.

### Running the Application

To run the application, use the following command:

```bash
flask run
```

This will start a local server, typically accessible at `http://127.0.0.1:8080`.

### API Endpoints

The application provides several API endpoints, such as:

- `/start`: Initiates a conversation with the user.
- `/chat`: Handles user input and provides appropriate responses.


## Built With

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Requests](https://docs.python-requests.org/) - Used for handling HTTP requests


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

