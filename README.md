# Logs Analysis

An internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

This tool will answer three question.

* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which days did more than 1% of requests lead to errors?

## Quick Start

You should Install python2 to run this script

### Install

* Set up a VirtualBox/Vagrant environment
  1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
  2. Install [Vagrant](https://www.vagrantup.com/downloads.html)
  3. Start the virtual machine

    From your terminal, inside the **vagrant** subdirectory, run the command **vagrant up**. This will cause Vagrant to download the Linux operating system and install it.

    When **vagrant up** is finished running, you will get your shell prompt back. At this point, you can run **vagrant ssh** to log in to your newly installed Linux VM!

* [optional step] Install python module [psycopg2](https://pypi.python.org/pypi/psycopg2) (IF haven't installed)

If your pip version supports wheel packages it should be possible to install a binary version of Psycopg including all the dependencies from PyPI. Just run:
```
$ pip install -U pip      # make sure your pip is up-to-date
$ pip install psycopg2
```

* Download database
Next, [download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called newsdata.sql.

To load the data, use the command **psql -d news -f newsdata.sql**.

* Create View in database
You shold create three view in database, **log_articles**, **log_daily**, **log_error**.


* Run the script

```
python logs_analysis.py
```

## Database View

### log_articles
Outputing a table of successful log record for every article and its author

```
CREATE VIEW  log_articles AS
  SELECT author, title FROM articles
  LEFT JOIN log
  ON '/article/' || slug = path
  WHERE status = '200 OK';
```

**Example:**

| id      | author |               title             |
| :------ | :----- | :------------------------------ |
| 1678924 |      2 | Candidate is jerk, alleges rival|
| 1678925 |      1 | Goats eat Google's lawn         |
| 1678926 |      1 | Goats eat Google's lawn         |
| 1678927 |      4 | Balloon goons doomed            |
| 1678929 |      2 | Candidate is jerk, alleges rival|

### log_daily
Outputing a table of all requests for each day.
```
CREATE VIEW log_daily AS
  SELECT DATE(time), COUNT(*) AS count_total
  FROM log
  GROUP BY DATE(time);
```
**Example:**

| date       | count_total |
| :--------- | :---------- |
| 2016-07-01 |       38705 |
| 2016-07-02 |       55200 |
| 2016-07-03 |       54866 |
| 2016-07-04 |       54903 |

### log_error
Outputing a table of error requests for each day

```
CREATE VIEW log_error AS
  SELECT DATE(time), COUNT(*) AS count_error
  FROM log
  WHERE status LIKE '404%'
  GROUP BY DATE(time);
```
**Example:**

| date       | count_error |
| :--------- | :---------- |
| 2016-07-31 |         329 |
| 2016-07-06 |         420 |
| 2016-07-17 |        1265 |
| 2016-07-19 |         433 |
