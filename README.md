# Log Analysis Project #

## Download ##

This project is available on [GitHub] (https://github.com/brewerdave)

## Requirements ##

* PostgreSQL
* psycopg pyhton library: [psycopg] (http://initd.org/psycopg/)
* [News] (https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) database file installed with `psql -d news -f newsdata.sql`

## To Run ##

```python
python reporter.py
```

## Description ##

This program runs some database queries to answer a few question about the database, such as: What are the most popular articles? It uses the psycopg python library to interface with PostgreSQL.