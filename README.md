# Status Check App for OpThink Course

This project is a FastAPI application designed to record and view daily status checks, such as mental, emotional, and physical statuses throughout the day. It stores the data in SQLite and provides an interface for retrieving and updating records. You can change this to any storage, but to keep it simple, I just used file storage for now.

I hope other **#SpyTribe** users find this useful.

**I've added Generative AI Reporting.** Type in "status report" to get a comprehensive report of all your entries automatically.

Links to Andy's website [here](https://everydayspy.com/about-andrew/ "here").

Note: I'm not an employee of EverydaySpy. Just someone doing the course and needed this tool for myself during the [OpThink Course](https://new.everydayspy.com/think2 "OpThink Course"). I needed something simple to use while on the go. Plus, I needed a way to summarize the unstructured content easily, so I integrated Generative AI.

## Features

- **Daily Status Logging**: Users can input their mental, emotional, and physical statuses during the day (Wake-up, Post-breakfast, Post-lunch, Post-dinner, Bedtime).
- **CSV Storage**: Data is stored in a local DB file for persistence.
- **Jinja2 Templating**: Frontend rendering using Jinja2 for serving HTML templates.
- **REST API**: Includes endpoints for getting and submitting status data for specific dates.
- **Generative AI**: Includes Generative AI allowing you to talk to all your data. Just put your OpenAI API key in the .env file.

## Screen Shots

![](https://snipboard.io/eP8LRm.jpg)

------------

![](https://snipboard.io/VWZs2y.jpg)

------------

![](https://snipboard.io/CWU26a.jpg)

------------

## Generative AI SpyTribe Status Check Helper
Your AI Guide will let you essentially talk to your notes you've added in automatically.
or you can type in "status report" and it will organise a report for you with the following:
- Identify key patterns, recurring themes, and significant fluctuations in the client's moods and behaviors.
- Note any correlations between activities, physical states, and emotional well-being.
- Comprehensive Summary and Insights:
- Personalized Recommendations

![](https://snipboard.io/LHEBS6.jpg)

------------

![](https://snipboard.io/JiavnN.jpg)

## Requirements

To run this project, the following dependencies need to be installed:

- Python 3.7+
- FastAPI
- Uvicorn
- Jinja2

You can install the required dependencies with the following command:

```bash
pip install fastapi uvicorn jinja2
