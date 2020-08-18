    select coach_id, coach_fname, coach_lname, student_id, student_fname, student_lname, description, sys_connect_by_path(notes, '&') as notes
    from (
            select unique coach.id as coach_id, trim(coach_name.firstname) as coach_fname, trim(coach_name.lastname) as coach_lname,
                   student.id as student_id, trim(student_name.firstname) as student_fname, trim(student_name.lastname) as student_lname,
                   "" as description, TRIM(invl_table.txt) as notes,
                   rank() over (partition by student.id, coach.id order by txt) AS seq,
                   rank() over (partition by student.id, coach.id order by txt desc) AS rseq
            from involve_rec student join involve_rec coach on student.invl = coach.org
            join invl_table on invl_table.invl = student.invl and invl_table.edi_invl = "DOS" and invl_table.sanc_sport = "Y"
            join id_rec coach_name on coach.id = coach_name.id
            join id_rec student_name on student.id = student_name.id
            join prog_enr_rec on student.id = prog_enr_rec.id
            where (     (student.yr = 2020 and student.sess = "RA")
                     or (student.yr = 2021 and student.sess = "RC")
                  )
            AND prog_enr_rec.acst in ('GOOD' ,'LOC' ,'PROB' ,'PROC' ,'PROR' ,'READ' ,'RP' ,'SAB' ,'SHAC' ,'SHOC')
        ) ath
    WHERE rseq = 1 start with seq = 1
    CONNECT BY prior student_id = student_id
           AND prior seq = seq-1
