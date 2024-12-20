IS218Final Project

Overview

This project is a Python-based web application that performs various operations, including mathematical calculations and interaction with an external API (GroqAPI). The application is built using FastAPI and supports both a web interface and programmatic interaction through RESTful APIs. The project also includes comprehensive test coverage to ensure reliability.

Features

Core Functionalities:

Mathematical Operations:

Addition, subtraction, multiplication, and division.

Results are saved in a connected PostgreSQL database.

GroqAPI Integration:

Enables interaction with external APIs for advanced computations.

Allows sending natural language queries to the GroqAPI.

Web Interface:

A simple web calculator interface with JavaScript-based real-time clock support.

Database Integration:

Uses SQLAlchemy to manage database connections and handle models.

Testing:

Comprehensive tests for API endpoints, GroqAPI calls, and mathematical operations.

Dockerized Deployment:

Supports containerized deployment using Docker and Docker Compose.

Project Structure

Root Directory

Dockerfile: Builds the Docker image for the application.

docker-compose.yml: Manages multi-container setup for the app and database.

requirements.txt: Specifies the Python dependencies.

pytest.ini: Configuration for running tests with Pytest.

.gitignore: Files and directories to ignore in Git.

README.md: Documentation for the project.

Application Code (app/)

__init__.py: Initializes the application package.

base.py: Defines base classes and configurations.

config.py: Stores API keys and endpoint configurations (loaded via .env).

database.py: Manages database connection and ORM models.

groq_api.py: Handles interactions with the GroqAPI.

main.py: The main application entry point, defines routes and app lifecycle events.

operations/__init__.py: Implements core mathematical functions.

Static Files (static/)

index.html: HTML file for the web interface.

clock.js: JavaScript for rendering a real-time clock.

Tests (tests/)

test_base.py: Tests for base configurations.

test_groq_api.py: Tests for GroqAPI integration.

test_main.py: Tests for application routes and functionality.

test_operations.py: Tests for mathematical operations.


Highlights

Scalable Design: Modular structure for easy enhancements.

Real-Time Clock: Enhances user experience with a JavaScript-based clock.

GroqAPI Integration: Extends functionality with external API calls.

Comprehensive Testing: Ensures reliability through high test coverage.

Docker Support: Simplifies deployment and environment consistency.

tails.

Video Link: https://youtu.be/01LIlCU4WGg

By: Andres Tovio Pabon