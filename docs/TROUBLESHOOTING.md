# Troubleshooting

This guide provides solutions to common issues that you may encounter while using the Pollinations.ai Prompt Enhancer.

## Common Issues

### 1. `python-dotenv` library not found

*   **Error Message:** `Error: The 'python-dotenv' library is required.`
*   **Solution:** Install the `python-dotenv` library by running the following command:

    ```
    pip install python-dotenv
    ```

### 2. API_TOKEN not found

*   **Error Message:** `API_TOKEN not found.`
*   **Solution:** Create a `.env` file in the root directory of the project and add your Pollinations.ai API token:

    ```
    API_TOKEN=your-api-token
    ```

### 3. `prompts.json` not found

*   **Error Message:** `The file 'prompts.json' was not found.`
*   **Solution:** Make sure that the `prompts.json` file is in the same directory as the `main.py` script.

### 4. Authentication failed

*   **Error Message:** `Authentication failed. Check your API_TOKEN.`
*   **Solution:** Make sure that your API token is correct and that you have sufficient credits in your Pollinations.ai account.

### 5. API request failed

*   **Error Message:** `API request failed (Status: ...)`
*   **Solution:** This error may be caused by a temporary issue with the Pollinations.ai API. Please try again later.

### 6. Connection failed

*   **Error Message:** `Connection failed: ...`
*   **Solution:** This error may be caused by a network issue. Please check your internet connection and try again.
