SELECT
    TRIM(ACTIVE.crs_no) || '-' || TRIM(ACTIVE.sec_no) AS Course,
    ACTIVE.title,
    TRIM
    (
        TRIM(REPLACE(MTG.days,'-','')) || ' ' ||
        TRIM(TO_CHAR(CASE WHEN MOD(FLOOR(MTG.beg_tm / 100), 12) = 0 THEN 12 ELSE MOD(FLOOR(MTG.beg_tm / 100), 12) END)) || ':' || TO_CHAR(MOD(MTG.beg_tm, 100), '&&')
        || ' - ' ||
        TRIM(TO_CHAR(CASE WHEN MOD(FLOOR(MTG.end_tm / 100), 12) = 0 THEN 12 ELSE MOD(FLOOR(MTG.end_tm / 100), 12) END)) || ':' || TO_CHAR(MOD(MTG.end_tm, 100), '&&')
        || ' ' ||
        CASE
            WHEN
                FLOOR(MTG.end_tm / 100) >= 12
            THEN
                'PM'
            ELSE
                'AM'
        END
    ) AS Schedule,
    TRIM(STU.lastname) AS lastname,
    TRIM(STU.firstname) AS firstname,
    STU.id AS student_id
FROM
    (
        SELECT
            TO_NUMBER(CRP.host_id) AS id, TRIM(CRS.title) AS title, SR.*
        FROM
            jenzcrp_rec CRP
        INNER JOIN
            jenzcrs_rec CRS
        ON
            CRP.course_code = CRS.course_code
        AND
            CRP.sec = CRS.sec
        AND
            CRP.term_code = CRS.term_code
        INNER JOIN
            jenztrm_rec TRM
        ON
            CRS.term_code = TRM.term_code
        INNER JOIN
            sec_rec SR
        ON
            CRS.sec = SR.sec_no
        AND
            TRIM(CRS.course_code) = TRIM(SR.crs_no) || ' (' || TRIM(SR.cat) || ')'
        AND
            LEFT(CRS.term_code,2) = TRIM(SR.sess)
        WHERE
            TRM.start_date <= ADD_MONTHS(TODAY,6)
        AND
            TRM.end_date >= ADD_MONTHS(TODAY,-1)
        AND
            RIGHT(TRIM(CRP.term_code),4) NOT IN ('PRDV','PARA','KUSD')
        AND
            TRIM(CRP.status_code) = 'STU'
        UNION ALL
            SELECT
                CW.id,
                TRIM(
                    TRIM(NVL(CR.title1,'')) || ' ' ||
                    TRIM(NVL(CR.title2,'')) || ' ' ||
                    TRIM(NVL(CR.title3,''))
                ) AS Title,
                SR.*
            FROM
                sec_rec SR
            INNER JOIN
                crs_rec CR
            ON
                SR.crs_no = CR.crs_no
            AND
                SR.cat = CR.cat
            INNER JOIN
                cw_rec CW
            ON
                CR.crs_no = CW.crs_no
            AND
                CR.cat = CW.cat
            WHERE
                SR.stat = 'X'
            AND
                SR.end_date > TODAY
            AND
                SR.stat_date > TODAY - 4
    ) ACTIVE
    INNER JOIN
        secmtg_rec SM
    ON
        ACTIVE.crs_no = SM.crs_no
    AND
        ACTIVE.cat = SM.cat
    AND
        ACTIVE.sec_no = SM.sec_no
    AND
        ACTIVE.yr = SM.yr
    INNER JOIN
        mtg_rec MTG
    ON
        SM.mtg_no = MTG.mtg_no
    INNER JOIN
        id_rec STU
    ON
        ACTIVE.id = STU.id
WHERE
    ACTIVE.fac_id = CID
AND
    ACTIVE.yr = 2020
AND
    ACTIVE.sess = 'RA'
GROUP BY
     Course, ACTIVE.title, Schedule, lastname, firstname, student_id
ORDER BY
    course, lastname, firstname
