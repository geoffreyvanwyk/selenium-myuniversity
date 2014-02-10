from selenium import webdriver
from time import localtime
import csv

TARGET = 'http://myuniversity.gov.au/UndergraduateCourses'
ROOT_XPATH = "//div[@class='myuni-small-cell-block']"
LEAF_XPATH = './/span'

def parse_page():
	print 'Parsing web page ...'
	results = browser.find_elements_by_xpath(ROOT_XPATH)
	for result in results:
		values = result.find_elements_by_xpath(LEAF_XPATH)
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

def get_timestamp():
	current_time = localtime()
	return '-'.join(map(str, [
		current_time.tm_year,
		current_time.tm_mon,
		current_time.tm_mday,
		current_time.tm_hour,
		current_time.tm_min,
		current_time.tm_sec,
	]))

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

	file_name = 'courses-' + get_timestamp() + '.csv'
	print 'Writing results to ', file_name, ' ...'

	output_file = open(file_name, 'wb')
	dict_writer = csv.DictWriter(output_file, column_names)
	dict_writer.writer.writerow(column_names)
	dict_writer.writerows(courses)

print 'Opening web browser ...'
browser = webdriver.Firefox()
browser.get(TARGET)

courses = []

parse_page()
create_csv()

print 'Done.'