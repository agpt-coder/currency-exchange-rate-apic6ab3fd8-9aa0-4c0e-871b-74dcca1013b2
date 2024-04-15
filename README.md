---
date: 2024-04-15T13:17:50.197346
author: AutoGPT <info@agpt.co>
---

# Currency Exchange Rate API

To create an endpoint that handles real-time exchange rate data effectively, the application will utilize Python as the programming language, with FastAPI for the API framework due to its performance and ease of asynchronous programming, which is beneficial for real-time data processing. The database of choice will be PostgreSQL, managed through Prisma as the ORM for efficient and straightforward database operations.

The endpoint will be designed to accept both a base currency and one or multiple target currencies as parameters. Utilizing the preferred real-time exchange rate data source, the 'Forex Open Exchange Rates' API, the application will retrieve the latest exchange rates efficiently. Implementing best practices for secure external API calls, such as using HTTPS for encrypted data transmission, managing sensitive information like API keys securely, and validating the SSL certificates, will ensure data integrity and security.

The endpoint will calculate the exchange rate between the specified base and target currencies by fetching the latest rates from the Forex API. To accommodate the requirement for multiple target currencies, the logic will include processing multiple rates in a single request when possible, leveraging the Forex API’s ability to handle multiple currencies. The results will include the calculated exchange rates along with a timestamp of the data retrieval, ensuring users have access to the timeliness of the information.

Care will be taken to implement caching strategies to minimize direct API calls, thus optimizing performance and managing API rate limits effectively. Fallback mechanisms will also be in place to handle potential API failures, ensuring continuous functionality of the endpoint.

In summary, the endpoint will provide a robust, secure, and efficient way to retrieve and calculate real-time exchange rates for given base and target currencies, incorporating user feedback and technical best practices for a high-quality user experience.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Currency Exchange Rate API'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
