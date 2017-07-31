#!/usr/bin/env python
import psycopg2

DBNAME = "news"


def db_execute(query):
    """
    connect to datebase, run the query and return the result.
    Input:
        query  => SQL query need to run.
    Output:
        result => the result returned from datebase
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


# Calculate number of access for every article
query_log_article = """
SELECT title, views
FROM log_articles
ORDER BY views DESC
LIMIT 3;
"""

# Calculate number of access for every author
query_log_author = """
SELECT name, sum(views) as total
FROM log_articles, authors
WHERE author = id
GROUP BY name
ORDER BY total DESC;
"""

# Calculate error rate
query_log_error = """
SELECT log_daily.date , count_error*1000/count_total AS error_rate
FROM log_daily, log_error
WHERE log_daily.date = log_error.date
AND (count_error*1000/count_total) >= 10;
"""


# ----------------------- Main ----------------------- #

# Display the report of log analysis of article.
print("\nWhat are the most popular three articles of all time?\n")
for title, total in db_execute(query_log_article):
    print("\"%s\"  --  %s Views" % (title, total))

# Display the report of log analysis of author.
print("\nWho are the most popular article authors of all time?\n")
for name, total in db_execute(query_log_author):
    print("\"%s\"  --  %s Views" % (name, total))

# Display the report of log error.
print("\nOn which days did more than 1% of requests lead to errors?\n")
for date, rate in db_execute(query_log_error):
    print("%s  --  %s %% errors" % (date, rate/10.0))
