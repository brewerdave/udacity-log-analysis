#!/usr/bin/env python2

import psycopg2

dbconnection = psycopg2.connect("dbname=news")
cursor = dbconnection.cursor()

cursor.execute("""
               select articles.title, count(path) as views
                 from articles
                      join log
                      on log.path like '%' || articles.slug || '%'
                group by articles.title
                order by views desc
                limit 3;
                """)

results = cursor.fetchall()

print "What are the most popular three articles of all time?"
print "\"" + str(results[0][0]) + "\" -- " + str(results[0][1]) + " views"
print "\"" + str(results[1][0]) + "\" -- " + str(results[1][1]) + " views"
print "\"" + str(results[2][0]) + "\" -- " + str(results[2][1]) + " views"

cursor.execute("""
               select authors.name, count(path) as views
                 from articles
                      join authors
                      on articles.author = authors.id
                      join log
                      on log.path like '%' || articles.slug || '%'
                group by authors.name
                order by views desc;
                """)

results = cursor.fetchall()

print ""
print "Who are the most popular article authors of all time?"
print str(results[0][0]) + " -- " + str(results[0][1]) + " views"
print str(results[1][0]) + " -- " + str(results[1][1]) + " views"
print str(results[2][0]) + " -- " + str(results[2][1]) + " views"
print str(results[3][0]) + " -- " + str(results[3][1]) + " views"

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

results = cursor.fetchall()

print ""
print "On which days did more than 1% of requests lead to errors?"

for day in results:
    print str(day[0]) + " -- " + str(day[1]) + "% errors"

dbconnection.close()
