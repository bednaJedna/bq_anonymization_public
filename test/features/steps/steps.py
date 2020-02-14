from behave import given, then, when
from hamcrest import assert_that, empty, equal_to, is_, is_not

from helpers import functions as f


@given(
    'I get data for "{dataset}" dataset "{state}" table in timepoint t-"{timedelta_}"'
)
def step_impl(context, dataset, state, timedelta_):
    """
    implements python code logic for @given decorator
    - Given statement from feature files.
        :param context:object
        :param dataset:str
        :param state:str
        :param timedelta_:str
        :returns context:object
    
    Context object is behave framework object, which allows for storing and using variables
    across step implementation functions.
    """
    if state == "not-anonymized":
        results = f.run_bq_job(f.FILEPATH_SQL_NOTANON, dataset, timedelta_)
    elif state == "anonymized":
        results = f.run_bq_job(f.FILEPATH_SQL_ANON, dataset, timedelta_)

    context.results = results
    context.timedelta_ = timedelta_
    context.dataset = dataset

    assert_that(context.results, is_not(empty()))


@when("I count rows")
def step_impl(context):
    """
    implements python code logic for @when decorator
    - When statement from feature files.
        :param context:object
        :returns context:object
    
    Context object is behave framework object, which allows for storing and using variables
    across step implementation functions.
    """
    if context.results.total_rows == 0:
        context.flag = True
    else:
        context.flag = False
        df = f.convert_to_dataframe(context.results)
        f.save_data_to_excel(
            f.FILEPATH_BQ_DATA,
            df,
            context.dataset,
            context.timedelta_,
            context.scenario.name[:11],
        )
        f.add_html_attachment(
            f.render_df_html_snapshot(df), "First 10 rows of BQ data of failed test."
        )
        f.add_file_link_attachment(f.FILEPATH_BQ_DATA, "BQ data of failed tests")


@then("data {state} anonymized if count is zero")
def step_impl(context, state):
    """
    implements python code logic for @then decorator
    - Then statement from feature files.
        :param context:object
        :param state:str
        :returns context:object
    
    Context object is behave framework object, which allows for storing and using variables
    across step implementation functions.
    """
    if state in ("were", "were not"):
        assert_that(context.flag, is_(equal_to(True)))
