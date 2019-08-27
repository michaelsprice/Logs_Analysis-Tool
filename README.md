# Logs Analysis Project 
The Logs Analysis Project will use a datebase containing over a million records to show you the 3 top articles of all time, their authors and what day more than 1% of the requests lead to errors.

## Installation
You will need to make sure you have a virtual machine installed and running (for info see [this page](https://classroom.udacity.com/nanodegrees/nd004/parts/51200cee-6bb3-4b55-b469-7d4dd9ad7765/modules/c57b57d4-29a8-4c5f-9bb8-5d53df3e48f4/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)). The following is using VirtualBox and Vagrant. 

Once you have VirtualBox and Vagrant installed, make sure vagrant is running ( run `vagrant up` then `vagrant ssh`).

1. Download the data from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).

2. Unzip the file after downloading it, then move the `newsdata.sql` file into the vagrant directory.

3. Insider your terminal window, cd into the vagrant directory and run the following command `psql -d news -f newsdata.sql`.


## Usage

- Inside your terminal window (still in the vagrant directory), run `psql -d news` to explore the tables using the `\dt` and `d table` commands and `select` statements. 

- To see the results from the LogsAnalysis.py file, make sure you're in the vagrant directory (ctrl + z to get out of psql if needed), then run `python LogsAnalysis.py`.

## CREATE VIEWS
The following views were created:

- CREATE VIEW topThreeTitles as select count(*) as num, path from log where path <> '/' group by path order by num desc limit 3

- CREATE VIEW titleSlug as select distinct slug, title, path from articles,log where log.path like '%' || articles.slug

- CREATE VIEW authorSlug as select name, slug, authors.id from authors, articles where authors.id=articles.author

- CREATE VIEW totalRequests as select date(time) as theTotalDate, count(*) as total from log group by theTotalDate

- CREATE VIEW badRequests as select date(time) as theBadDate, count(*) as numBad from log where status <> '200 OK' group by theBadDate

- CREATE VIEW percentBadRequests as select (cast(numBad as decimal) / total)*100 as percentBad, theTotalDate from badRequests,totalRequests where theBadDate = theTotalDate
