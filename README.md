# Bounus Example - Jarvis Chatbot - Powered by OpenAI

This is a Python-based chatbot application called **Jarvis** that uses the OpenAI API to respond to user inputs. The application can handle a variety of questions and provides meaningful responses based on OpenAI's GPT models. The chatbot runs in a terminal/command line interface and can answer questions in a conversational style.

## Features

- Simple chatbot interface.
- Integration with OpenAI's GPT-3.5 or GPT-4 models.
- Flexible conversation based on user input.
- Easy setup and use on Ubuntu or any system with Python.

## Requirements

- Python 3.x
- OpenAI API key

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Create a Virtual Environment

It's recommended to create a virtual environment to isolate your project's dependencies.

```bash

python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

All required Python packages are listed in the requirements.txt file. You can install them with the following command:

```bash

pip install -r requirements.txt
```

### 4. Set Up Environment Variables

This project uses a .env file to store sensitive environment variables such as the OpenAI API key.

    Create a .env file in the root of the project:

```bash

touch .env
```

    Add your OpenAI API key to the .env file:

```plaintext

OPENAI_API_KEY=your-openai-api-key
```

### 5. Run the Chatbot

After setting up the environment and installing the dependencies, you can start the chatbot by running the following command:

```bash

python chat.py
```
