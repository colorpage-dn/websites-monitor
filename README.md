# Website Layout Change Monitoring

This repository monitors multiple WordPress websites for layout changes. The monitoring checks each site every hour, compares the layout to the previous version, and sends an email alert if any changes are detected.

## How it Works
- The script checks the websites for layout changes.
- It compares the current layout with the previously captured version.
- If any differences are found, an email alert is sent.

## Requirements
- Python 3.9+
- Required Python packages: `requests`, `smtplib`, `email`.

## Setup
- Clone this repository and add your email configuration to the GitHub Actions secrets.
- Set up the repository to run the monitoring script on a schedule.
