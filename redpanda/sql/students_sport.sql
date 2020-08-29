SELECT
    CUR.id, TRIM(IR.lastname) AS lastname,
    TRIM(IR.firstname) AS firstname
FROM
    cc_current_students_vw CUR
INNER JOIN
    id_rec IR
ON
    CUR.id = IR.id
WHERE
    CUR.prog in ('UNDG', 'GRAD')
AND
    CUR.subprog in ('ACT', 'BDI', 'MED', 'MM', 'TRAD')
AND 
    '{SPORT}' IN (
        SELECT
            TRIM(IT.invl) AS sport_code
        FROM
            invl_table IT
        INNER JOIN
            involve_rec INR
        ON
            TRIM(IT.invl) = TRIM(INR.invl)
        AND
            IT.sanc_sport = 'Y'
        WHERE
            TODAY BETWEEN IT.active_date AND NVL(IT.inactive_date, TODAY)
        AND
            YEAR(INR.end_date) = {YEAR}
        AND
            INR.id = IR.id
    )
