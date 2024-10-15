# HBnB Project - Project Setup

## Overview

This project is part of the **HBnB** series, focused on building a web application using Python, Flask, and RESTful API principles. This document outlines the project structure, the purpose of each directory, and instructions for setting up and running the application.

## Project Structure

The project follows a modular architecture to ensure scalability and maintainability. Below is a description of the key directories and files:

### Directories

- **`api/`**: Contains the Flask API logic, including routes and views to manage client requests.
- **`models/`**: Contains the core business logic and models, such as `User`, `Place`, `Review`, and `Amenity`.
- **`tests/`**: Holds unit tests to validate API endpoints and business logic.
- **`utils/`**: Contains utility functions used throughout the project, such as error handling and response formatting.
- **`static/`**: Includes static files for the front-end (CSS, JavaScript, images).
- **`templates/`**: Stores HTML templates for dynamic content rendering (if needed).

### Files

- **`app.py`**: The main file that initializes the Flask app and configures the routes.
- **`requirements.txt`**: A list of dependencies required for the project.
- **`README.md`**: Documentation and instructions for setting up and running the project.
- **`config.py`**: Handles configuration settings for different environments (development, production, etc.).

## Installation and Setup

### Prerequisites

- Ensure that Python 3.8 or above is installed on your system.
- Make sure you have a package manager to install Python dependencies (e.g., pip).

### Steps to Install and Run

1. **Clone the repository** to your local machine.

   ```bash
   git clone https://github.com/<your-username>/holbertonschool-hbnb.git
   cd holbertonschool-hbnb
   ```

2. **Set up a virtual environment** (recommended but optional) to manage dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install all dependencies** listed in the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application** locally to launch the Flask server.

   ```bash
   python3 app.py
   ```
   The application will be available at http://127.0.0.1:5000/ in your browser.

### Testing

The project includes a test suite in the `tests/` directory, which you can use to ensure that the API endpoints and business logic are working as expected.

## Conclusion

This setup provides a structured approach for building the HBnB application, enabling modular development and easy maintenance. Follow the setup steps to run the application and begin contributing to the project.

## Autors

Nadège Luthier (https://github.com/NadegeL)
Enes Gemici (https://github.com/ZykeLaDebrouille)
Jérôme Romand (https://github.com/jeje-digifab/)
