<h1 align="center">Big Query Anonymization Test Tool</h1>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

---

<p align="center"> Testing solution for BQ GDPR anonymization use case.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Running the tests](#tests)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

This projects implements a testing solution using python-behave framework to test, whether ID fields in BQ datasets' tables were anonymized successfully.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them.

- Python 3.6+ with these external packages:
  - behave
  - allure-behave
  - pandas
  - openpyxl
  - tqdm
  - pyhamcrest
  - google
  - google-cloud-biqquery
  - protobuf
- linux (Ubuntu)/Win10 OS
- allure reporting tool
  - on Win10 install using scoop
  - on Ubuntu/linux install using linuxbrew
- access to tested BQ data project
- access to BQ API, have it set up and have proper roles
- access to this repository

### Get familiar with used external tools' documentation to really understand, what is going on

- <a href="https://behave.readthedocs.io/en/latest/index.html">behave framework</a>
- <a href="http://allure.qatools.ru/">allure reporting tool</a>
- <a href="https://github.com/hamcrest/PyHamcrest">pyhamcrest</a>
- <a href="https://github.com/tqdm/tqdm">tqdm</a>
- <a href="https://pandas.pydata.org/pandas-docs/stable/index.html">pandas</a>
- <a href="https://openpyxl.readthedocs.io/en/stable/">openpyxl</a>
- <a href="https://pypi.org/project/google-cloud-bigquery/">google-cloud-bigquery</a>

Google and protobuf packages had to be placed in setup.py file to ensure proper functionality of BQ API library package.

### Installing

1. Install Python (refer to documentation, how to do that on your OS)
2. fire up your command line tool of choice and get to the directory, where you will want to clone the project from github
3. clone this repo
4. run "python3 setup.py install" if on ubuntu, or "py setup.py install" if on win10. On Win10, package "pandas" will not be installed, you will have to do it manually. See comment in the setup.py file for link. Download the package, and run command _pip install [path to package]/packagefile_

## 🔧 Running the tests <a name = "tests"></a>

1. In the console, be in the root folder of the project
2. run command _"behave -f allure_behave.formatter:AllureFormatter -f pretty -o allure-results .\test\features\"_ if on ubuntu, or _"behave -f allure_behave.formatter:AllureFormatter -f pretty -o allure-results ./test/features"_ if on Win10
3. wait, until tests are finished
4. failed test have BQ data saved in XLSX file with timestamped name in the _./reports_ folder.
5. you can also display interactive HTML report. To do this, run _"allure serve"_ command in your console and the report will open in your default browser. It should be Firefox or Chrome.

### Pseudo-random feature file test running

All datasets are divided into 5 feature files, with few exceptions. It is possible to run them either as it is specified above, or, if needed, it is possible to apply pseudo-random selection of the feature file.

To do that, run _"python3 (or py on windows) manage.py -r"_ command in the console.

This will pick one of the tags stored in the list in the _"functions.py"_ file and then run behave test framework, as usual, but only the feature file tagged by this tag will be actually run.

This process can be repeated as many times, as there are some tags, that were not picked, or "exhausted". When that happens, ValueError exception is caught, and you have to manually clear the "config.json" file.

To do that, use the utility _"py manage.py -c"_.

You can also run the utility with both parameters at once, so next time the pseudorandom function will be able to choose from full set of tags again. In this case, run command like this _"py manage.py -r -c"_.

### Manage.py utility

To provide easier and faster work with behave coupled with allure reporting tool - since that console command can be quite long, you can use manage.py utility to cover these scenarios:

- _py manage.py -r_ will run one randomly picked feature file from all tagged feature files. This feature file will not be ran again, until config.json is cleared.
- _py manage.py -c_ will clear config.json file, which stores tags of feature files, which were already randomly run.
- _py manage.py -b_ will run all feature files like this command _"behave -f allure_behave.formatter:AllureFormatter -f pretty -o allure-results .\test\features\"_ would do.
- _py manage.py -t "@tag1" -t "@tag2" etc..._ wil run all feature files or just some of their scenarios tagged by provided tags. Take care to enter the tags wrapped in " " !.
- _py manage.py -h_ is always available by default and will display all available command with short descriptions.

## ✍️ Authors <a name = "authors"></a>

- [@bednaJedna](https://github.com/bednaJedna) - Idea & work
