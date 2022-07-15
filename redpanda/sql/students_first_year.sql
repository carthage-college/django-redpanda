SELECT
unique
    id_rec.lastname, id_rec.firstname, id_rec.id
FROM
    id_rec
INNER JOIN
    prog_enr_rec
ON
    id_rec.id = prog_enr_rec.id
LEFT JOIN
    stu_acad_rec
ON
    id_rec.id = stu_acad_rec.id
LEFT JOIN
    stu_serv_rec
ON
    id_rec.id = stu_serv_rec.id
WHERE
    prog_enr_rec.subprog
NOT IN
    ("UWPK","RSBD","SLS","PARA","MSW","KUSD","ENRM","CONF","CHWK")
AND
    prog_enr_rec.lv_date IS NULL
AND
    stu_acad_rec.sess
IN
    ("RA","RC","AM","GC","PC","TC","GD","GA","GC")
AND prog_enr_rec.cl IN ("FN","FF","UT","PF","PN")
AND stu_serv_rec.yr = "2022"
AND stu_serv_rec.sess IN ("RA","AM","GD","GA")
ORDER BY id
