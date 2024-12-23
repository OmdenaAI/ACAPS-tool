# Streamlit App: Crisis Forecasting Tool

This project is part of ACAPS initiative to build a custom workflow leveraging AI-powered tools for real-time crisis forecasting.

## Table of Contents
1. [Features](#features)
2. [Setup and Installation](#setup-and-installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Additional Notes](#additional-notes)

---

## Features

- AI-driven sentiment analysis using Twitter, Google Trends, and news data.
- Supports over 20 languages with voice responses.
- Integration with ACLED data for enhanced analysis.
- Data visualization and insights for decision-making.

---

## Setup and Installation

Follow the steps below to set up the application:

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo-name/your-project-name.git
cd your-project-name
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### Windows:
```bash
venv\Scripts\activate
```

#### macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `secrets.toml` file in the `.streamlit` folder with the following content:

```toml
APIFY_TOKEN = "apify_api_???"
MODEL_KEY = "hf_???"
OPENAI_API_KEY = "sk-proj-???"
SERPER_API_KEY = "???"
HUGGING_FACE_API_KEY = "hf_???"
GROQ_API_KEY = "gsk_???"
APIFY_TWITTER_TOKEN = "apify_api_???"
ELEVEN_API_KEY = ""
ACLED_API_KEY = "???"
ACLED_EMAIL = "???@???.???"

[acaps]
username = "???@???.???"
password = "???@???.???"
```

Replace the placeholders (`???`) with your actual API keys and credentials.

---

## Usage

1. **Run the Application**

```bash
streamlit run app.py
```

2. **Access the Application**

Open your browser and navigate to the URL provided by Streamlit (e.g., `http://localhost:8501`).

---

## Additional Notes

- Ensure all dependencies are installed and API keys are correctly configured.
- Use the provided CLI commands to set up the environment quickly.
- For troubleshooting, refer to the Streamlit documentation or raise an issue in the repository.

