SELECT
    COUNT(DISTINCT created_by_id) AS czechs,
    str_to_date(concat(yearweek(created_at), ' monday'), '%X%V %W') AS date
FROM
    core_healthcheck
GROUP BY
    yearweek(created_at)
