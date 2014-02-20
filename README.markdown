# MyUniversity Scraper (Selenium)

Uses the Selenium framework to scrape undergraduate and postgraduate course information from the website
www.myuniversity.gov.au. The data is collected in a CSV file with the following headings:

* Course Name
* Cut-off ATAR
* Duration
* Award Type
* Field of Education
* Provider
* Campus
* Level

## Requirements

* Python 2.7
* Selenium 2.39.0

## Usage

Issue the following command in root of the project folder:

	$ python myuniversity-courses.py

The script will have output similar to this:

![Screenshot of Terminal Output](screenshot-of-terminal-output.png "Terminal Output")

## Performance

This scraper collected 15564 records from 1557 pages containing 10 courses each, in 2 hours 54 minutes.