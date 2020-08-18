SELECT
    STU_INV.id, STU.lastname, STU.firstname
FROM
    involve_rec    HC_INV
INNER JOIN
    involve_rec    STU_INV
ON
    TRIM(HC_INV.org) = STU_INV.invl
AND
    TODAY <= NVL(STU_INV.end_date, TODAY)
AND
    STU_INV.ctgry = 'ATHLETIC'
AND
    STU_INV.yr >= YEAR(TODAY)
INNER JOIN
    id_rec STU
ON
    STU_INV.id = STU.id
WHERE
    HC_INV.id = {CID}
AND
    HC_INV.ctgry = 'HR'
GROUP BY
    STU_INV.id, STU.lastname, STU.firstname
