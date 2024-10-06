# Status Check App #SpyTribe

This project is a FastAPI application designed to record and view daily status checks, such as mental, emotional, and physical statuses throughout the day. It stores the data in a SQLLite and provides an interface for retrieving and updating records. You can change this to any storage but to it easy I just used file for now.

I hope other **#SpyTribe** users find this useful.

**I've added Generative AI Reporting.** Type in "status report" to get a comprehensive report of all your entires automatically.

Links to Andys webiste [here](https://everydayspy.com/about-andrew/ "here")

Note: I'm not an emmployee of EerydaySpy. Just someone doing the course and needed this tool for myself during the [OpThink Course](https://new.everydayspy.com/think2 "OpThink Course"). I needed something simple to use whilst on the go. Plus I needed a way to summarise the unstrcutred content easliy so I integrated Generative AI.

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
