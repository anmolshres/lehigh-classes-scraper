from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
import logging
import pprint
from time import sleep
import sys

CHROMEDRIVER_PATH = './chromedriver.exe'
options = Options()
options.headless = False
chunkLength = 5000
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
master_json_list = []


def gotoPage(page_number):
    page_input = driver.find_element_by_class_name('page-number.enabled')
    page_input.clear()
    page_input.send_keys(page_number)
    page_input.send_keys(Keys.ENTER)
    sleep(2)


def extractInfoFromSingleClass(one_class):
    one_class.click()
    # wait until the class details visible
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'courseReferenceNumber')))
    except expression as identifier:
        logging.exception(
            f'Error while waiting for class details to load for {one_class.text}')
        raise Exception('Stop')

    crn_number = driver.find_element_by_id('courseReferenceNumber').text
    section_number = driver.find_element_by_id('sectionNumber').text
    subject = driver.find_element_by_id('subject').text
    course_number = driver.find_element_by_id('courseNumber').text
    course_title = driver.find_element_by_id('courseTitle').text
    json_to_dump = {
        "CRN": crn_number,
        "section": section_number,
        "subject": subject,
        "course_number": course_number,
        "title": course_title
    }
    master_json_list.append(json_to_dump)
    close_button = driver.find_element_by_css_selector(
        'body > div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.course-details-dialog.ui-draggable.ui-resizable > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button > span')
    close_button.click()
    # wait until the class details page is gone
    try:
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element((By.ID, 'courseReferenceNumber')))
    except expression as identifier:
        logging.exception(
            f'Error while waiting for class details to close for {one_class.text}')
        raise Exception('Stop')


def getClassesInfo(max_page, start_page):
    if(start_page != 1):
        gotoPage(start_page)
    for page in range(start_page, max_page + 1):
        print(f'Currently in page number {page}')
        classes_elements = driver.find_elements_by_css_selector(
            '.section-details-link')
        for single_class in classes_elements:
            extractInfoFromSingleClass(single_class)
        if page != max_page:
            next_page_button = driver.find_element_by_css_selector(
                '#searchResultsTable > div.bottom.ui-widget-header > div > button.paging-control.next.ltr.enabled')
            next_page_button.click()
            # wait until the website has gone to next page
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'loading')))
                WebDriverWait(driver, 20).until(
                    EC.invisibility_of_element((By.CLASS_NAME, 'loading')))
            except expression as identifier:
                logging.exception(
                    f'Error while going to next page at page number {page}')


def main():
    driver.get(
        'https://reg-prod.ec.lehigh.edu/StudentRegistrationSsb/ssb/classSearch/classSearch')
    first_link = driver.find_element_by_id('classSearchLink')
    first_link.click()
    dropdown = driver.find_element_by_css_selector(
        '#s2id_txt_term > a > span.select2-arrow > b')
    dropdown.click()
    try:
        fall2020_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.ID, '202040')))
        fall2020_element.click()
    except expression as identifier:
        logging.exception('Error while waiting for dropdown')
        raise Exception('Stop')
    continue_button = driver.find_element_by_id('term-go')
    continue_button.click()
    try:
        search_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'search-go')))
        search_button.click()
        # Wait till search results are available
        maxpage_number_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.paging-text.total-pages')))
        max_page = int(maxpage_number_element.text)
    except expression as identifier:
        logging.exception(
            'Error while waiting for the search button or data loaded after search')
        raise Exception('Stop')
    start_page = 1 if len(sys.argv) == 1 else int(sys.argv[1])
    getClassesInfo(max_page, start_page)
    with open('class_data.json', 'w', encoding='utf-8') as out_file:
        json.dump(master_json_list, out_file)
    print(f'{len(master_json_list)} pages were crawled!')
    driver.quit()


if __name__ == "__main__":
    try:
        main()
    except:
        with open('class_data.json', 'w', encoding='utf-8') as out_file:
            json.dump(master_json_list, out_file)
            logging.exception('Error occured!')
