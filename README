# ITSC 3155 Final Project: NinerFit

Our application is a health tracking platform that allows users to input daily health data, including food intake, calorie consumption, caffeine intake, exercise, sleep, and more.

## Django

Out application uses the Django framework, which requires a Python virtual environment.

To start the project:
1. In a command terminal, create a virtual environment using the following command:
    ```
    virtualenv env
    ```
2. Install package dependencies from the `requirements.txt` file by running the following commands:
    ```
    cd NinerFit
    pip install -r requirements.txt
    ```
3. Once all dependencies have been downloaded, run the project using the following command:
    ```
    python manage.py runserver
    ```

When downloading this project, you may run into issues with the database that cause unexpected errors, such as failing to register or log in users or certain components not functioning properly. This can be fixed by resetting your Django database.

To reset your database:
1. Delete all `*.pycache` files from any `/__pycache__/` and `/migrations/` folders.
2. Within the `/NinerFit/` directory, run the following commands to recreate all migrations:
    ```
    python manage.py flush
    python manage.py makemigrations
    python manage.py migrate
    ```
    

## OpenAI implementation

NinerFit implements the GPT-4o-mini model using OpenAI's API, which requires an API key to work.

To make AI features accessible:
1. Make an account on `https://platform.openai.com/`
2. Follow the instructions on `https://platform.openai.com/docs/api-reference/authentication` to create a new secret key for your organization.

    > The OpenAI API uses API keys for authentication. Create, manage, and learn more about API keys in your _organization settings_.
    > Remember that your API key is a secret! Do not share it with others or expose it in any client-side code (browsers, apps). API keys should be securely loaded from an environment variable or key management service on the server.

3. Paste the API key you created within the files for `NinerFit/ChatBot/views.py` and `NinerFit/main/suggestion_generate.py`.
    ``` python
    #set open AI API
    your_api = '' #insert own api key here
    client = OpenAI(api_key=your_api)
    ```