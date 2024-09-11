# Status Check App #SpyTribe

This project is a FastAPI application designed to record and view daily status checks, such as mental, emotional, and physical statuses throughout the day. It stores the data in a CSV file and provides an interface for retrieving and updating records. You can change this to any storage but to it easy I just used file for now.

I hope other #SpyTibe users find this useful.

## Features

- **Daily Status Logging**: Users can input their mental, emotional, and physical statuses during the day (Wake-up, Post-breakfast, Post-lunch, Post-dinner, Bedtime).
- **CSV Storage**: Data is stored in a CSV file for persistence.
- **Jinja2 Templating**: Frontend rendering using Jinja2 for serving HTML templates.
- **REST API**: Includes endpoints for getting and submitting status data for specific dates.

## Screen Shots

![](https://snipboard.io/eP8LRm.jpg)

------------

![](https://snipboard.io/VWZs2y.jpg)

------------

![](https://snipboard.io/CWU26a.jpg)

## Requirements

To run this project, the following dependencies need to be installed:

- Python 3.7+
- FastAPI
- Uvicorn
- Jinja2

You can install the required dependencies with the following command:

```bash
pip install fastapi uvicorn jinja2
