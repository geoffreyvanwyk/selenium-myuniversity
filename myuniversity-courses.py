from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException

from datetime import datetime
from sys import stdout
import csv

#-------------------------------------------------------------------------------
# CONSTANTS
#-------------------------------------------------------------------------------

TARGETS = [
	'http://myuniversity.gov.au/UndergraduateCourses',
	'http://myuniversity.gov.au/PostgraduateCourses',
]

COLUMNS = [
	'Course Name',
	'Cut-off ATAR',
	'Duration',
	'Award Type',
	'Field of Education',
	'Provider',
	'Campus',
	'Level',
]

XPATHS = {
	'course_elements': "//div[@class='myuni-small-cell-block']",
    'course_attribute_elements': './/span',
    'next_button': "//div[@class='myuni-alignright-whenbig'][../p[@id='navigationDescriptor']]/a[last()]",
    'number_of_pages': "//div[@class='myuni-alignright-whenbig'][../p[@id='navigationDescriptor']]/label/span[last()]",
}

#-------------------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------------------

def create_csv(courses, status):
	timestamp = datetime.today().strftime("%Y-%m-%dT%H-%M-%S")
	file_name = 'myuniversity-courses-' + status + '-' + timestamp  + '.csv'
	print "\nWriting " + status + " results to ", file_name, ' ...'
	output_file = open(file_name, 'wb')

	dict_writer = csv.DictWriter(output_file, COLUMNS)
	dict_writer.writer.writerow(COLUMNS)
	dict_writer.writerows(courses)

def finish(courses, status):
	create_csv(courses, status)
	if status == 'partial':
		print
		print 'WARNING: Timed-out.'
		print 'Retrying ...'
		print 'Parsing page:     ', # The comma allows for the page number to appear on the same line.
	elif status == 'complete':
		print 'Finish time: ', datetime.today().strftime("%H:%M:%S %b %d, %Y")
		print 'Done.'

def get_next_page(driver):
	driver.find_element_by_xpath(XPATHS['next_button']).click()

def parse_page(driver, courses):
	course_elements = driver.find_elements_by_xpath(XPATHS['course_elements'])
	for course_element in course_elements:
		course_attribute_elements = course_element.find_elements_by_xpath(XPATHS['course_attribute_elements'])
		course = {
			COLUMNS[0]: course_attribute_elements[0].text,
			COLUMNS[1]: course_attribute_elements[2].text,
			COLUMNS[2]: course_attribute_elements[4].text,
			COLUMNS[3]: course_attribute_elements[5].text,
			COLUMNS[4]: course_attribute_elements[6].text,
			COLUMNS[5]: course_attribute_elements[7].text,
			COLUMNS[6]: course_attribute_elements[8].text,
			COLUMNS[7]: driver.current_url.split('/')[-1].replace('Courses', '')
		}
		courses.append(course)

def get_backspaces(page_number):
	n = page_number
	b = "\b"
	while n / 10 > 0:
		b += "\b"
		n /= 10
	return b

def print_page_number(page_number):
	stdout.write(get_backspaces(page_number) + "%d" % page_number)
	stdout.flush()

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
	number_of_pages = 5 #get_number_of_pages(driver)

	print 'Number of pages: ', number_of_pages
	print 'Parsing page:     ', # The comma allows for the page number to appear on the same line.

	while number_of_pages >= current_page_number:
		try:
			WebDriverWait(driver, 10).until(has_page_loaded)
			print_page_number(current_page_number)
			parse_page(driver, courses)
			current_page_number += 1
			get_next_page(driver)
		except TimeoutException:
			finish(courses, 'partial')

def start(url):
	print 'Start time: ', datetime.today().strftime("%H:%M:%S %b %d, %Y")
	print 'Opening web browser ...'
	browser = webdriver.Firefox()
	print 'Visiting: ', url
	browser.get(url)
	parse_all(browser)

#-------------------------------------------------------------------------------
# EXECUTION
#-------------------------------------------------------------------------------

for TARGET in TARGETS:
	start(TARGET)

finish(courses, 'complete')