#!/usr/bin/env python2

import psycopg2


def connect(database_name="news"):
    try:
        database_connection = psycopg2.connect("dbname={}".format(database_name))
        cursor = database_connection.cursor()
        return database_connection, cursor
    except psycopg2.Error as e:
        print "Unable to connect to the database"
        sys.exit(1)


def fetch_query(query):
    db, cursor = connect()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results;


def print_top_articles():
    query = """
               select title, count(*) as views
                 from articles
                      join log
                      on log.path = concat('/article/', articles.slug)
                group by title
                order by views desc
                limit 3;
                """

    results = fetch_query(query)

    print("Most popular articles:")
    for (title, count) in results:
        print("    {} - {} views".format(title, count))
    print("*" * 70)
    print(" ")


def print_top_authors():
    query = """
               select authors.name, count(*) as views
                 from articles
                      join authors
                      on articles.author = authors.id
                      join log
                      on log.path = concat('/article/', articles.slug)
                group by authors.name
                order by views desc;
                """

    results = fetch_query(query)

    print("Most popular authors:")
    for (author, count) in results:
        print("    {} - {} views".format(author, count))
    print("*" * 70)
    print(" ")


def print_top_error_days():
    query = """
               select day, percentage
                 from
                      (select time::date as day,
                              (100.0 * count(status) filter
                                  (where status = '404 NOT FOUND')::decimal
                              / count(status)::decimal)
                              as percentage
                         from log
                        group by day
                        order by percentage)
                           as subq
                where percentage >= 1.0;
               """

    results = fetch_query(query)

    print("Days with most errors:")
    for day, percent in results:
        print("    {} - {:.2f}% errors".format(day, percent))
    print("*" * 70)
    print(" ")

if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()
