# lehigh-classes-scraper

A python script that uses selenium to scrape classes and class meta-data of Lehigh classes.

This script uses [selenium](https://selenium-python.readthedocs.io/) to scrape information about classes offered in [Lehigh University](https://www1.lehigh.edu/home) from this registration [link](https://reg-prod.ec.lehigh.edu/StudentRegistrationSsb/ssb/registration/registration).

The data is stored in a file named `class_data.json` in the root directory in the following `JSON` list format:

```
{
    "CRN": crn_number,
    "section": section_number,
    "subject": subject,
    "course_number": course_number,
    "title": course_title
}
```

## Steps before running script:

- Create a virtualenv and run it. (This is slightly different for [Windows](https://programwithus.com/learn-to-code/Pip-and-virtualenv-on-Windows/) vs [Linux/Mac](https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv))
- In order for selenium to work, you need to download [`chromewebdriver`](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it into the directory containing the shell scripts. Choose the version that matches the web browser you have. Note: You can always opt to use a different browser like Firefox. Just make sure to change the code accordingly in `new_zealand_links,py` to reflect that. Also, if you don't have a windows machine, you need to change this part in `new_zealand_links.py` to reflect that:

```
CHROMEDRIVER_PATH = './chromedriver.exe'
```

- Run `pip install -r requirements.txt` from the inside the directory containing `requirements.txt` file while virtualenv is running to install all the dependencies
  The dependencies are as follows (automatically installed when above command is run):

```
autopep8==1.5.3
pycodestyle==2.6.0
selenium==3.141.0
toml==0.10.1
urllib3==1.25.10
```

## Running the script:

- Run command `python main.py` from root directory if you want to start from `page 1`
- Run command `python main.py <page_number>` if you want to start from `<page_number>` page.

## Accessing the data:

- Your data will be in `class_data.json` 😎
