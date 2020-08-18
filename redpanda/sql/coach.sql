SELECT
    trim(fullname) as fullname,
    involve_rec.*
FROM
    involve_rec
JOIN
    id_rec
ON
    involve_rec.id = id_rec.id
WHERE
    invl IN (
        SELECT
            invl
        FROM
            invl_table
        WHERE
            edi_invl = "HR"
    )
AND
    id_rec.id={CID}
