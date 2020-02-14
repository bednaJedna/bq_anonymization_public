import argparse
import json
from datetime import datetime as dt
from datetime import timedelta
from os import getcwd, path
from os.path import isfile, join
from random import randrange

from allure import attach, attachment_type
from behave.__main__ import main as bmain

from google.cloud.bigquery import Client

from pandas import ExcelWriter

FILEPATH_SQL_ANON = path.join(getcwd(), "sql", "anon.sql")
FILEPATH_SQL_NOTANON = path.join(getcwd(), "sql", "notanon.sql")
FILEPATH_BQ_DATA = path.join(
    getcwd(), "reports", "".join([dt.now().strftime("%Y%m%d_%H%M"), ".xlsx"])
)
TAGS = ["@set1", "@set2", "@set3", "@set4", "@set5"]
PATH_CONFIG = join(getcwd(), "config.json")


def load_file(filepath: str):
    """
    loads file as string
        :param filepath:str: 
        :returns str:
    """
    with open(filepath, mode="r", encoding="utf-8") as f:
        content = f.read()
    return content


def insert_dataset_id(script: str, dataset_id: str):
    """
    replaces {dataset} placeholder in the SQL query string
    template script
        :param script:str: 
        :param dataset_id:str: 
        :returns script:str
    """
    return script.replace("{dataset}", dataset_id)


def insert_date(script: str, timedelta_: str):
    """
    replaces {date_} placeholder in the SQL query string
    template script
        :param script:str: 
        :param timedelta_:str: 
        :returns script:str
    """
    return script.replace("{date_}", get_past_date(timedelta_))


def get_past_date(timedelta_: str, present=dt.now):
    """
    return previous date computed as present - timedelta,
    formatted as "%Y%m%d" str
        :param timedelta_:str: 
        :param present=dt.now:object:
        :returns date:str 
    """
    past = present() - timedelta(days=int(timedelta_))
    return past.strftime("%Y%m%d")


def convert_to_dataframe(bq_data: object):
    """
    downloads BQ data and returns them as pandas dataframe object
        :param bq_data:object: 
        :returns bq_data:object
    """
    return bq_data.to_dataframe(progress_bar_type="tqdm")


def save_data_to_excel(
    filepath: str, dataframe: object, dataset: str, timedelta_: str, scenario: str
):
    """
    saves data of FAILED test cases into XLSX file.
    data of each failed test case are appended as new sheet.
        :param filepath:str: 
        :param dataframe:object: 
        :param dataset:str: 
        :param timedelta_:str: 
        :param scenario:str: 
    """
    sheetname = f"{scenario}_{dataset}_t-{timedelta_}"

    if not isfile(filepath):
        with ExcelWriter(filepath, mode="w") as writer:
            dataframe.to_excel(writer, sheet_name=sheetname)

    else:
        with ExcelWriter(filepath, engine="openpyxl", mode="a") as writer:
            dataframe.to_excel(writer, sheet_name=sheetname)


def add_file_link_attachment(filepath: str, name: str):
    """
    adds link to XLSX file of failed test cases' data 
    into Allure report as attachment of given test case.
        :param filepath:str: 
        :param name:str: 
    """
    link_code = f'<head></head><body><a href="file:///{filepath}" target="_blank" rel="noopener">{filepath}</a></body>'
    attach(link_code, name, attachment_type.HTML)


def add_html_attachment(html_content: str, name: str):
    """
    adds HTML content into Allure report 
    as attachment of given test case.
        :param html_content:str: 
        :param name:str: 
    """
    attach(html_content, name, attachment_type.HTML)


def render_df_html_snapshot(dataframe: object, maxrows=10):
    """
    returns first <maxrows> no. of rows of dataframe
    as HTML code.
        :param dataframe:object: 
        :param maxrows=10: 
        :returns html:str:
    """
    if dataframe.shape[0] <= maxrows:
        return dataframe.to_html()
    else:
        df = dataframe.iloc[:maxrows, :]
        return df.to_html()


def run_bq_job(filepath: str, dataset_id: str, timedelta_: str):
    """
    returns RowIterator object of requested BigQuery data via 
    API Client. 
        :param filepath:str: 
        :param dataset_id:str: 
        :param timedelta_:str: 
        :returns result:object:

    RowIterator docs:
    https://googleapis.dev/python/bigquery/1.23.1/generated/google.cloud.bigquery.table.RowIterator.html#google.cloud.bigquery.table.RowIterator
    """
    client = Client()
    query = insert_date(insert_dataset_id(load_file(filepath), dataset_id), timedelta_)
    query_job = client.query(query)
    result = query_job.result()
    return result


def load_json(filepath: str):
    """
    loads .json file and returns it as object
        :param filepath:str: 
        :returns json content:object
    """
    with open(filepath, mode="r", encoding="utf-8") as f:
        content = json.load(f)
    return content


def save_json(filepath: str, blown_tags: list):
    """
    saves <blown_tags> data into json file
        :param filepath:str: 
        :param blown_tags:list: 
    """
    with open(filepath, mode="w", encoding="utf-8") as f:
        json.dump({"done": blown_tags}, f, ensure_ascii=False, indent=2)


def get_blown_tags(json_content: object):
    """
    returns list of already used tags.
        :param json_content:object:
        :returns tags:list 
    """
    return json_content["done"]


def get_random_tag(tags: list, blown_tags: list):
    """
    Randomly selects one tag from the list.
    If tag was already used, then this tag is dropped from the list
    and recursively tries to select another one.
    Selected/used tag is then placed into config.json file.
    If all tags were used, than raises the ValueError and config.json
    has to be clean - either manually or via manage.py utility.
        :param tags:list: 
        :param blown_tags:list: 
        :returns tag:str
    """
    tagcount = len(tags)
    try:
        randint = randrange(0, tagcount, step=1)
    except ValueError:
        raise ValueError(
            f"No tags to choose from, see for yourself:\ntags: {tags}\nblown tags: {blown_tags}\n Clean JSON file."
        )
    tag = tags[randint]

    if tag not in blown_tags:
        blown_tags.append(tag)
        save_json(PATH_CONFIG, blown_tags)
        return tag

    else:
        del tags[randint]
        return get_random_tag(tags, blown_tags)


def run_random(tags: list):
    """
    Starts behave framework.
    Only feature files tagged by randomly selected tag are ran.
        :param tags:list: 
    """
    blown_tags = get_blown_tags(load_json(PATH_CONFIG))
    random_tag = get_random_tag(tags, blown_tags)
    bmain(
        "-f allure_behave.formatter:AllureFormatter"
        " -o allure-results"
        " -f pretty"
        " ./test/features"
        " --tags={}".format(random_tag)
    )


def run_all():
    """
    Starts behave framework.
    All feature files are ran.
    """
    bmain(
        "-f allure_behave.formatter:AllureFormatter"
        " -o allure-results"
        " -f pretty"
        " ./test/features"
    )


def run_tags(tags: list):
    """
    Starts behave framework.
    Only feature files/scenarios tagged by supplied tags are ran.
        :param tags:list: 
    """
    bmain(
        "-f allure_behave.formatter:AllureFormatter"
        " -o allure-results"
        " -f pretty"
        " ./test/features"
        " --tags='{}'".format(",".join(tags))
    )


def clear_json(filepath: str):
    """
    Removes all used tags from the config.json file.
        :param filepath:str: 
    """
    content = {"done": []}

    with open(filepath, mode="w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

    print(f"config.json content after dump:\n{content}")


def parse_args():
    """
    Parses supplied arguments via CLI.
        :returns args:object
    """
    parser = argparse.ArgumentParser(
        description="Manage.py handles your input as best as it can."
    )

    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="runs pseudo-randomly picked feature file",
    )
    parser.add_argument(
        "-c",
        "--clear",
        action="store_true",
        help="runs clearing function - empties 'config.json' file",
    )
    parser.add_argument(
        "-b",
        "--behave",
        action="store_true",
        help="runs all feature files as would normal behave command do.",
    )
    parser.add_argument(
        "-t",
        action="append",
        default=[],
        type=str,
        dest="tags_list",
        help='runs all feature files specified by provided tags. e.g: -t "@t1" -t "@t2" -t "@t3"',
    )

    return parser.parse_args()
