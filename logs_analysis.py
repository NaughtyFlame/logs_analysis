#!/usr/bin/env python
import psycopg2

DBNAME = "news"


def db_connect():
    """ Creates and returns a connection to the database defined by DBNAME,
        as well as a cursor for the database.

        Returns:
            db, c - a tuple. The first element is a connection to the database.
                    The second element is a cursor for the database.
    """
    try:
        db = psycopg2.connect(database=DBNAME)
    except psycopg2.Error as e:
        print "Can not connect to the database"
    else:
        return db


def execute_query(query):
    """execute_query takes an SQL query as a parameter.
        Executes the query and returns the results as a list of tuples.
       args:
           query - an SQL query statement to be executed.

       returns:
           A list of tuples containing the results of the query.
    """

    db = db_connect()
    c = db.cursor()
    try:
        c.execute(query)
    except psycopg2.Error as e:
        print "Can not excute the query"
    result = c.fetchall()
    db.close()
    return result


def print_top_articles():
    """Prints out the top 3 articles of all time."""
    query = """
    SELECT title, views
    FROM log_articles
    ORDER BY views DESC
    LIMIT 3;
    """
    results = execute_query(query)

    print("\nWhat are the most popular three articles of all time?\n")
    for title, total in results:
        print('\"{}\" -- {} views'.format(title, total))


def print_top_authors():
    """Prints a list of authors ranked by article views."""
    query = """
    SELECT name, sum(views) as total
    FROM log_articles, authors
    WHERE author = id
    GROUP BY name
    ORDER BY total DESC;
    """
    results = execute_query(query)

    print("\nWho are the most popular article authors of all time?\n")
    for name, total in results:
        print('\"{}\" -- {} views'.format(name, total))


def print_errors_over_one():
    """
    Prints out the days where more than 1% of logged access requests were
    errors.
    """
    query = """
    SELECT log_daily.date , count_error::numeric/count_total AS error_rate
    FROM log_daily, log_error
    WHERE log_daily.date = log_error.date
    AND (count_error::numeric/count_total) >= 0.01;
    """
    results = execute_query(query)

    print("\nOn which days did more than 1% of requests lead to errors?\n")
    for date, rate in results:
        print("{0:%B %d, %Y} - {1:.2%}  errors".format(date, rate))

if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_errors_over_one()
