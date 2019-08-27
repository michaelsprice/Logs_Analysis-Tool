#!/usr/bin/python

import psycopg2

conn = psycopg2.connect("dbname=news")

cursor = conn.cursor()
question1 = 'The most popular three articles of all time are: '
question2 = 'The most popular article authors of all time are: '
question3 = 'More than 1% of requests lead to errors on: '
blankline = ''
# 1. What are the most popular three articles of all time?
cursor.execute("CREATE VIEW topThreeTitles as select count(*) as num, path \
    from log where path <> '/' group by path order by num desc limit 3")
cursor.execute("CREATE VIEW titleSlug as select distinct slug, title, path \
    from articles,log where log.path = CONCAT('/article/', articles.slug)")
cursor.execute("select title, num from titleSlug, topThreeTitles where \
    topThreeTitles.path = titleSlug.path order by num desc")
answer1 = cursor.fetchall()
print(question1)
for x in range(len(answer1)):
    print("\"" + str(answer1[x][0]) + "\"" + " -- "
          + str(answer1[x][1]) + " views")
print(blankline)
# =================================================================
# 2. Who are the most popular article authors of all time?
cursor.execute("CREATE VIEW authorSlug as select name, slug, authors.id \
    from authors, articles where authors.id=articles.author")
cursor.execute("select name, num from authorSlug, topThreeTitles \
    where topThreeTitles.path like '%' || authorSlug.slug order by num desc")

answer2 = cursor.fetchall()
print(question2)
for x in range(len(answer2)):
    print(str(answer2[x][0]) + " -- " + str(answer2[x][1]) + " views")
print(blankline)
# =================================================================
# 3. On which days did more than 1% of requests lead to errors?
# This groups dates together and shows the count of ALL requests.
cursor.execute("CREATE VIEW totalRequests as select date(time) as \
    theTotalDate, count(*) as total from log group by theTotalDate")
# This groups dates together and shows the count of BAD requests
cursor.execute("CREATE VIEW badRequests as select date(time) as theBadDate, \
    count(*) as numBad from log where status <> '200 OK' group by theBadDate")
# This gives the percentage of bad requests
cursor.execute("CREATE VIEW percentBadRequests as \
    select (cast(numBad as decimal) / total)*100 as percentBad, theTotalDate \
        from badRequests,totalRequests where theBadDate = theTotalDate")
cursor.execute("select theTotalDate, round(percentBad, 2) from \
    percentBadRequests where percentBad > 1 ")
answer3 = cursor.fetchall()
print(question3)
for x in range(len(answer3)):
    print(str(answer3[x][0]) + " -- " + str(answer3[x][1]) + "% errors")
# =================================================================

conn.close()
