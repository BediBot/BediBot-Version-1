# BediBot
Python Discord Bot designed for UWaterloo Discord Servers. Currently, it is in active use with 3000+ users in both official and unofficial contexts.

Key Features
========
- $verify: Will verify if the user has an email under a specified domain and give roles accordingly. Cross-server verification is supported.
- $addduedate: Adds due dates for assigments, tests, and reminders to a set channel
- $setbirthday: Stores the birthday in a mongoDB that is checked daily to announce birthdays to promote team bonding
- $addQuotes: Adds in a particular quote from a user
- $lockdown: Prevents users from speaking in a text channel temporarily (in case of assessments)

DEV INFORMATION
========
- Prod Branch is linked to Heroku
- Python 3.8 is required
- requirments.txt stores the packages required
- API keys are stored in a .ENV file that will only be given to developers

Workflow
========
Do NOT commit to master under any circumstances.
- Open a PR against master and request reviews if desired.
- Squash and merge is the preferred method
- Resolve merge conflicts on local before PR'ing

Contributers
========
Made by: Aadi, Carson, Sahil, & Zayd © 2020
- Please contact if you'd like to use any part of this code in your own repo :)
