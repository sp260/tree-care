# tree-care

Google App Engine Application.

## prerequisites

- Create a Free Trial Account on GCP, Google offers a free trial which gives you $300 credit you can use over 12 months
- Create a new Project
- Enable the Google Drive API
- Install Google Cloud SDK from [here](https://cloud.google.com/sdk/)

## Installation

Clone the repository, then use this command to install the necessary libraries:

```bash
pip install -t lib -r requirements.txt
```

## Running locally

Use this command to run in local environment:

```python
python main.py
```

## Deploying the app

Use this command to deploy the application:

```python
python app deploy
python app deploy cron.yaml
```