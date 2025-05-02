# Project Setup with UV

This project uses `uv` for managing Python environments and dependencies.

## Setup

1.  **Install `uv`:**
    If you haven't already, install `uv`:
    ```bash
    # Using curl (check uv documentation for other methods)
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Or using Homebrew on macOS/Linux
    brew install uv
    ```

2.  **Create a Virtual Environment:**
    Navigate to the project directory and create a virtual environment using `uv`:
    ```bash
    uv venv
    ```
    This will create a `.venv` directory.

3.  **Activate the Environment:**
    Activate the environment:
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows (Command Prompt):**
        ```bash
        .venv\Scripts\activate.bat
        ```
    *   **Windows (PowerShell):**
        ```bash
        .venv\Scripts\Activate.ps1
        ```

4.  **Install Dependencies:**
    Install the required packages using `uv`:
    ```bash
    uv pip install -r requirements.txt
    ```
    *(Assuming your dependencies are listed in `requirements.txt`)*

## Running the Application

*(Add instructions here on how to run your specific application, e.g., using `uvicorn` if it's a FastAPI app)*

```bash
# Example for a FastAPI app
uvicorn main:app --reload
```

## Deactivating the Environment

When you're done working, deactivate the environment:
```bash
deactivate
``` 