from selenium import webdriver
import csv

print 'Opening web browser ...'

browser = webdriver.Firefox()
browser.get('http://myuniversity.gov.au/UndergraduateCourses')

print 'Parsing web page ...'

results = browser.find_elements_by_xpath("//div[@class='myuni-small-cell-block']")
courses = []
for result in results:
	values = result.find_elements_by_xpath('.//span')
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

print 'Writing results to courses.csv file ...'

column_names = ['Course Name', 'Cut-off ATAR', 'Duration', 'Award Type', 'Field of Education', 'Provider', 'Campus']
output_file = open('courses.csv', 'wb')
dict_writer = csv.DictWriter(output_file, column_names)
dict_writer.writer.writerow(column_names)
dict_writer.writerows(courses)

print 'Done.'