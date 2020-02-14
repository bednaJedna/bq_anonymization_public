@set2
Feature: Test Anonymization of 2nd set of datasets

    Tests, whether anonymization of ID fields
    of BQ datasets were successful.

    @set2.notanon
    Scenario Outline: Data before treshold are not anonymized

        Tests, whether data before anonymization treshold
        (t - 391 days) are not anonymized.

        Given I get data for "<dataset>" dataset "not-anonymized" table in timepoint t-"<timedelta_>"
        When I count rows
        Then data were not anonymized if count is zero

        Examples:BigQuery datasets
            | dataset   | timedelta_ |
            # country01
            | dataset01 | 1          |
            | dataset01 | 150        |
            | dataset01 | 365        |
            | dataset01 | 388        |
            | dataset01 | 389        |
            | dataset01 | 390        |
            # country02
            | dataset02 | 1          |
            | dataset02 | 150        |
            | dataset02 | 365        |
            | dataset02 | 388        |
            | dataset02 | 389        |
            | dataset02 | 390        |
            # country03
            | dataset03 | 1          |
            | dataset03 | 150        |
            | dataset03 | 365        |
            | dataset03 | 388        |
            | dataset03 | 389        |
            | dataset03 | 390        |
            # country04
            | dataset04 | 1          |
            | dataset04 | 150        |
            | dataset04 | 365        |
            | dataset04 | 388        |
            | dataset04 | 389        |
            | dataset04 | 390        |
            # country05
            | dataset05 | 1          |
            | dataset05 | 150        |
            | dataset05 | 365        |
            | dataset05 | 388        |
            | dataset05 | 389        |
            | dataset05 | 390        |
            # country06
            | dataset06 | 1          |
            | dataset06 | 150        |
            | dataset06 | 365        |
            | dataset06 | 388        |
            | dataset06 | 389        |
            | dataset06 | 390        |
            # country07
            | dataset07 | 1          |
            | dataset07 | 150        |
            | dataset07 | 365        |
            | dataset07 | 388        |
            | dataset07 | 389        |
            | dataset07 | 390        |
            # country08
            | dataset08 | 1          |
            | dataset08 | 150        |
            | dataset08 | 365        |
            | dataset08 | 388        |
            | dataset08 | 389        |
            | dataset08 | 390        |
            # country09
            | dataset09 | 1          |
            | dataset09 | 150        |
            | dataset09 | 365        |
            | dataset09 | 388        |
            | dataset09 | 389        |
            | dataset09 | 390        |
            # country10
            | dataset10 | 1          |
            | dataset10 | 150        |
            | dataset10 | 365        |
            | dataset10 | 388        |
            | dataset10 | 389        |
            | dataset10 | 390        |


    @set2.anon
    Scenario Outline: Data after treshold are anonymized

        Tests, whether data after anonymization treshold
        (t - 391 days) are anonymized.

        Given I get data for "<dataset>" dataset "anonymized" table in timepoint t-"<timedelta_>"
        When I count rows
        Then data were anonymized if count is zero

        Examples:BigQuery datasets
            | dataset   | timedelta_ |
            # country01
            | dataset01 | 391        |
            | dataset01 | 392        |
            | dataset01 | 900        |
            # country02
            | dataset02 | 391        |
            | dataset02 | 392        |
            | dataset02 | 1050       |
            # country03
            | dataset03 | 391        |
            | dataset03 | 392        |
            | dataset03 | 1050       |
            # country04
            | dataset04 | 391        |
            | dataset04 | 392        |
            | dataset04 | 727        |        
            # country05
            | dataset05 | 391        |
            | dataset05 | 392        |
            | dataset05 | 1050       |
            # country06
            | dataset06 | 391        |
            | dataset06 | 392        |
            | dataset06 | 666        |
            # country07
            | dataset07 | 391        |
            | dataset07 | 392        |
            | dataset07 | 723        |
            # country08
            | dataset08 | 391        |
            | dataset08 | 392        |
            | dataset08 | 1059       |
            # country09
            | dataset09 | 391        |
            | dataset09 | 392        |
            | dataset09 | 1070       |
            # country10
            | dataset10 | 391        |
            | dataset10 | 392        |
            | dataset10 | 1050       |