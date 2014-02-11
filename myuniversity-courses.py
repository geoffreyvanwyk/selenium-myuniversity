from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

from datetime import datetime
from sys import stdout
from time import localtime
import csv

#-------------------------------------------------------------------------------
# CONSTANTS
#-------------------------------------------------------------------------------

TARGET = 'http://myuniversity.gov.au/UndergraduateCourses'

COLUMNS = [
	'Course Name',
	'Cut-off ATAR',
	'Duration',
	'Award Type',
	'Field of Education',
	'Provider',
	'Campus',
]

XPATHS = {
	'results_root': "//div[@class='myuni-small-cell-block']",
    'results_leaf': './/span',
    'next_button': "//div[@class='myuni-alignright-whenbig'][../p[@id='navigationDescriptor']]/a[last()]",
    'number_of_pages': "//div[@class='myuni-alignright-whenbig'][../p[@id='navigationDescriptor']]/label/span[last()]",
}

#-------------------------------------------------------------------------------
# FUNCTION DEFINITIONS
#-------------------------------------------------------------------------------

def create_csv(courses):
	file_name = 'courses-' + datetime.today().strftime("%Y-%m-%dT%H-%M-%S") + '.csv'
	print "\nWriting results to ", file_name, ' ...'
	output_file = open(file_name, 'wb')

	dict_writer = csv.DictWriter(output_file, COLUMNS)
	dict_writer.writer.writerow(COLUMNS)
	dict_writer.writerows(courses)

def finish(courses):
	create_csv(courses)
	print 'Finish time: ', datetime.today().strftime("%H:%M:%S %b %d, %Y")
	print 'Done.'

def get_next_page(driver):
	driver.find_element_by_xpath(XPATHS['next_button']).click()

def parse_page(driver, courses):
	results = driver.find_elements_by_xpath(XPATHS['results_root'])
	for result in results:
		values = result.find_elements_by_xpath(XPATHS['results_leaf'])
		course = {
			COLUMNS[0]: values[0].text,
			COLUMNS[1]: values[2].text,
			COLUMNS[2]: values[4].text,
			COLUMNS[3]: values[5].text,
			COLUMNS[4]: values[6].text,
			COLUMNS[5]: values[7].text,
			COLUMNS[6]: values[8].text,
		}
		courses.append(course)

def has_page_loaded(driver):
	try:
		return 0 == driver.execute_script('return jQuery.active')
	except WebDriverException:
		pass

def get_number_of_pages(driver):
	return int(driver.find_element_by_xpath(XPATHS['number_of_pages']).text.replace('of', ''))

def parse_all(driver):
	courses = []
	current_page_number = 1
	number_of_pages = 5

	print 'Number of pages: ', number_of_pages
	print 'Parsing page:  ',

	while number_of_pages >= current_page_number:
		WebDriverWait(driver, 10).until(
			has_page_loaded,
			lambda courses: finish(courses)
		)
		stdout.write("\b%d" %  current_page_number)
		stdout.flush()

		parse_page(driver, courses)
		current_page_number += 1
		get_next_page(driver)

	finish(courses)

def start():
	print 'Start time: ', datetime.today().strftime("%H:%M:%S %b %d, %Y")
	print 'Opening web browser ...'
	browser = webdriver.Firefox()
	print 'Visiting: ', TARGET
	browser.get(TARGET)
	parse_all(browser)

#-------------------------------------------------------------------------------
# BEGIN EXECUTION
#-------------------------------------------------------------------------------

start()