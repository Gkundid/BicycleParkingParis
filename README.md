# Bicycle Parking in Paris 

## Configuring the Development Environment

This project requires Python. Here's how to configure your development environment.

1. Make sure you have Python installed on your machine. This project uses Python 3.8+.

2. Create a virtual environment.
    ```bash
    python -m venv .venv
    ```

3. Activate the virtual environment :
    - On Windows :
        ```bash
        .\.venv\Scripts\activate
        ```
    - On macOS and Linux :
        ```bash
        source .venv/bin/activate
        ```

4. Install the necessary dependencies :
    ```bash
    pip install -r requirements.txt
    ```


## Run 

1. Go in frontend/  
    ```bash
    http-server 
    ```

2. Go in backend/
    ```bash
    python server.py
    ```

3. Test on http://localhost:8080