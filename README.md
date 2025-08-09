# Pollinations.ai Prompt Enhancer

A program with a secure and robust graphical user interface (GUI) to enhance text prompts using the Pollinations.ai API, featuring a dynamic user interface based on an external JSON file.

## Features

\*   **Dynamic UI:** The interface is dynamically generated from a `prompts.json` file, allowing for easy customization of prompt categories.
\*   **Secure API Client:** The application uses a secure API client that validates SSL certificates and loads the API token from a `.env` file.
\*   **Robust Error Handling:** The application has solid error handling to manage network issues, API errors, and other unexpected events.
\*   **Asynchronous API Calls:** The application uses a thread pool to make asynchronous API calls, ensuring the GUI remains responsive.
\*   **History and Conversation Management:** The application maintains a history of enhanced prompts and conversations for each category.
\*   **Export and Copy:** Allows exporting conversations and copying enhanced prompts to the clipboard.
\*   **Maximized on Startup:** The application window starts maximized for a better user experience.

## Author

\*   **Created by:** Diego Gonzalez
\*   **Contact:** diegoalgg88@gmail.com

## Installation and Configuration

Follow these steps to set up the application environment.

### 1\. Prerequisites

\*   Have Python 3 installed.

### 2\. Configure the API Token

Before running the setup, you must provide your Pollinations.ai API token.

1.  In the project's root directory, create a file named `.env`.
2.  Open the `.env` file and add your token as follows:

    `    API_TOKEN=your-api-token-here    `

### 3\. Run the Setup Script

I have created a script to automate the creation of the virtual environment and the installation of dependencies.

1.  Open a terminal in the project's root directory.
2.  Execute the following command:

    `    python setup.py    `

    This script will create a `.venv` folder with the virtual environment and install all necessary libraries found in `project/requirements.txt`.

## Usage

To run the application, simply double-click the `run.bat` file located in the project's root directory.

This script will handle:

1.  Requesting administrator permissions (necessary for proper execution).
2.  Activating the correct virtual environment.
3.  Starting the application.

## Project Structure

The project is organized into various directories and modules to keep the code clean and scalable.

\-   `setup.py`: Script in the project root that automates the creation of a virtual environment (`.venv`) and the installation of necessary dependencies.
\-   `run.bat`: Windows executable file in the root that starts the application with administrator privileges and using the correct virtual environment.
\-   `logs/`: Directory in the root that stores application execution logs.
\-   `project/`: Contains all the application's source code.
    -   `main.py`: The main entry point that starts the application.
    -   `requirements.txt`: A list of the necessary Python libraries.
    -   `config/`: Module responsible for configuration.
        -   `config.ini`: Defines API and application settings (URL, timeouts, window dimensions).
        -   `prompts.json`: The key file that allows dynamically defining the categories and enhancement prompts that appear in the interface.
    -   `core/`: Contains the main application logic.
        -   `gui.py`: Defines the entire structure, design, and behavior of the graphical user interface (GUI) with Tkinter.
        -   `api_client.py`: Manages secure communication with the Pollinations.ai API.
    -   `utils/`: Module for cross-cutting utilities.
        -   `logger.py`: Configures the logging system to record events and errors.
    -   `docs/`: Additional project documentation.

Below is a graphical representation of the structure:

```
Enhance_Prompt/
├── .env                # (Must be created by the user)
├── run.bat             # Execution script for Windows
├── setup.py            # Environment setup script
├── logs/               # Application logs
├── depreciated/        # Old code (not used)
└── project/
    ├── main.py         # Main application entry point
    ├── requirements.txt
    ├── config/
    │   ├── config.ini
    │   └── prompts.json
    ├── core/
    │   ├── api_client.py
    │   └── gui.py
    ├── utils/
    │   └── logger.py
    ├── docs/
    │   ├── CONTRIBUTING.md
    │   └── LICENSE
    └── tests/
```

## Contributions

Please read [CONTRIBUTING.md](https://www.google.com/search?q=docs/CONTRIBUTING.md) for more details on our code of conduct and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=docs/LICENSE) file for details.
