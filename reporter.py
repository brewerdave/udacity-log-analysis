#!/usr/bin/env python2

import psycopg2

dbconnection = psycopg2.connect("dbname=news")
cursor = dbconnection.cursor()

cursor.execute("""
               select title, count(*) as views
                 from articles
                      join log
                      on log.path = concat('/article/', articles.slug)
                group by title
                order by views desc
                limit 3;
                """)


print("Most popular articles:")
for(title, count) in cursor.fetchall():
    print("    {} - {} views".format(title, count))
print("*" * 70)

cursor.execute("""
               select authors.name, count(*) as views
                 from articles
                      join authors
                      on articles.author = authors.id
                      join log
                      on log.path = concat('/article/', articles.slug)
                group by authors.name
                order by views desc;
                """)

print(" ")
print("Most popular authors:")
for(author, count) in cursor.fetchall():
    print("    {} - {} views".format(author, count))
print("*" * 70)

cursor.execute("""
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
               """)

print(" ")
print("Days with most errors:")

for day, percent in cursor.fetchall():
    print("    {} - {:.2f}% errors".format(day, percent))

dbconnection.close()
