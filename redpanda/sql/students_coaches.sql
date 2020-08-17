    select coach_id, coach_fname, coach_lname, student_id, player_fname, player_lname, description, sys_connect_by_path(notes, '&') as notes
    from (
            select unique coach.id as coach_id, trim(coach_name.firstname) as coach_fname, trim(coach_name.lastname) as coach_lname,
                   player.id as student_id, trim(player_name.firstname) as player_fname, trim(player_name.lastname) as player_lname,
                   "" as description, TRIM(invl_table.txt) as notes,
                   rank() over (partition by player.id, coach.id order by txt) AS seq,
                   rank() over (partition by player.id, coach.id order by txt desc) AS rseq          
            from involve_rec player join involve_rec coach on player.invl = coach.org
            join invl_table on invl_table.invl = player.invl and invl_table.edi_invl = "DOS" and invl_table.sanc_sport = "Y"
            join id_rec coach_name on coach.id = coach_name.id
            join id_rec player_name on player.id = player_name.id
            join prog_enr_rec on player.id = prog_enr_rec.id
            where (     (player.yr = 2020 and player.sess = "RA")
                     or (player.yr = 2021 and player.sess = "RC")
                  )
            AND prog_enr_rec.acst in ('GOOD' ,'LOC' ,'PROB' ,'PROC' ,'PROR' ,'READ' ,'RP' ,'SAB' ,'SHAC' ,'SHOC')
        ) ath
    WHERE rseq = 1 start with seq = 1
    CONNECT BY prior student_id = student_id
           AND prior seq = seq-1
