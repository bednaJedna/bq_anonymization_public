/*
Anonymized version of SQL template.
Select returns zero rows, if values queried fields in given dataset and partition table were not anonymized.
That means, that all values comply with provided regexes.
*/
BEGIN

DECLARE r_ca_1_2 STRING;
DECLARE r_id_2 STRING;
DECLARE r_d_id1 STRING;

SET r_ca_1_2 = "^regex$";
SET r_d_id1 = "^regex$";
SET r_id_2 = "^regex$";

SELECT
  idfield1,
  idfield2,
  idfield3,
  date
FROM
  (SELECT
      idfield1,
      idfield2,
      (SELECT MAX(IF(index=1, value, NULL)) FROM UNNEST (hits.customDimensions)) AS idfield3,
      date
  FROM `project.{dataset}.datatable_*`, UNNEST (hits) AS hits
  WHERE _TABLE_SUFFIX = "{date_}"
  GROUP BY idfield1, idfield2, idfield3, date
  )
WHERE
    ((REGEXP_CONTAINS(idfield1, r_ca_1_2) IS NOT TRUE AND REGEXP_CONTAINS(idfield1, r_d_id1) IS NOT TRUE) OR
    REGEXP_CONTAINS(idfield2, r_id_2) IS NOT TRUE OR
    (REGEXP_CONTAINS(idfield3, r_ca_1_2) IS NOT TRUE AND idfield3 IS NOT NULL)
    );
END;
