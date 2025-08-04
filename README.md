# JobJourney Tracker

## Overview

Job Tracker is a tool designed to help manage and classify job application emails. It uses Cohere's text classification API to categorize emails into different classes such as "Application Received", "Rejected", "Interview" and "Not applicable" for unrelated emails.

## Features

- **Email Retrieval**: Uses the Gmail API to search and retrieve job application emails from you email.
- **Text Classification**: Classifies emails using Cohere's classification API.

## Setup

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- Google Cloud account for Gmail API
- Cohere API account
- Git

### Installation

1. **Clone the Repository**

    ```sh
    git clone https://github.com/norachams/JobTracker.git
    cd JobTracker
    ```

2. **Set Up Virtual Environment**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**

    Create a `.env` file in the root directory and add your API keys:

    ```plaintext
    COHERE_API_KEY=your-cohere-api-key
    GMAIL_CLIENT_ID=your-gmail-client-id
    GMAIL_CLIENT_SECRET=your-gmail-client-secret
    ```

5. **Set Up Gmail API**

    Follow the [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python) to enable the API and obtain `credentials.json`. Place this file in the root directory.

### Usage

1. **Run Email Retrieval and Classification**

    ```sh
    python get_messages.py
    python Classify_cohere.py
    ```

2. **Check the Cleaned Classifications**

    After running the classification script, check the `cleaned_classifications.json` file for results.

## Currently Working on

1. **Enhance Classification Model**: Improve the accuracy of the classification by fine-tuning the model with more labeled examples.
2. **Add More Email Providers**: Extend support to other email providers like Outlook and Yahoo Mail.
3. **Automated Updates**: Implement a cron job to automatically retrieve and classify new emails on a regular basis.
4. **Data Visualization**: Add features to visualize the classification data for better insights.
