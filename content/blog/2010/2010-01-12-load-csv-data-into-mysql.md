---
author: rickymoorhouse
categories:
- MySQL
- tech
comments: true
date: "2010-01-12T11:20:58Z"
link: https://rickymoorhouse.uk/2010/01/12/load-csv-data-into-mysql/
slug: load-csv-data-into-mysql
title: Load CSV data into MySQL
wordpress_id: 1396
---

<code>
    load data local infile '<em>export.csv</em>' into table <em>table_name</em>
    fields terminated by ','
    enclosed by '"'
    lines terminated by 'n'
    (<em>field_list</em>)
    </code>
