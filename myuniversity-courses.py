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

XPATHS = {
	'results_root': "//div[@class='myuni-small-cell-block']",
    'results_leaf': './/span',
    'next_button': "//div[@class='myuni-alignright-whenbig'][../p[@id='navigationDescriptor']]/a[last()]",
    'number_of_pages': "//div[@class='myuni-alignright-whenbig'][../p[@id='navigationDescriptor']]/label/span[last()]",
}

#-------------------------------------------------------------------------------
# FUNCTION DEFINITIONS
#-------------------------------------------------------------------------------

def ajax_complete(driver):
	try:
		return 0 == driver.execute_script('return jQuery.active')
	except WebDriverException:
		pass

def get_number_of_pages():
	return int(browser.find_element_by_xpath(XPATHS['number_of_pages']).text.replace('of', ''))

def parse_page():
	results = browser.find_elements_by_xpath(XPATHS['results_root'])
	for result in results:
		values = result.find_elements_by_xpath(XPATHS['results_leaf'])
		course = {
			'Course Name': values[0].text,
			'Cut-off ATAR': values[2].text,
			'Duration': values[4].text,
			'Award Type': values[5].text,
			'Field of Education': values[6].text,
			'Provider': values[7].text,
			'Campus': values[8].text,
		}
		courses.append(course)

def create_csv():
	column_names = [
		'Course Name',
		'Cut-off ATAR',
		'Duration',
		'Award Type',
		'Field of Education',
		'Provider',
		'Campus',
	]

	file_name = 'courses-' + datetime.today().strftime("%Y-%m-%dT%H-%M-%S") + '.csv'
	print "\nWriting results to ", file_name, ' ...'

	output_file = open(file_name, 'wb')
	dict_writer = csv.DictWriter(output_file, column_names)
	dict_writer.writer.writerow(column_names)
	dict_writer.writerows(courses)

#-------------------------------------------------------------------------------
# BEGIN EXECUTION
#-------------------------------------------------------------------------------

print 'Start time: ', datetime.today().strftime("%H:%M:%S %b %d, %Y")
print 'Opening web browser ...'

browser = webdriver.Firefox()
browser.get(TARGET)

courses = []
current_page_number = 1
number_of_pages = 5

print 'Number of pages: ', number_of_pages
print 'Parsing page:  ',

while number_of_pages >= current_page_number:
	WebDriverWait(browser, 10).until(
		ajax_complete,
		create_csv
	)
	stdout.write("\b%d" %  current_page_number)
	stdout.flush()
	parse_page()
	current_page_number += 1
	browser.find_element_by_xpath(XPATHS['next_button']).click()

create_csv()
print 'Stop time: ', datetime.today().strftime("%H:%M:%S %b %d, %Y")
print 'Done.'