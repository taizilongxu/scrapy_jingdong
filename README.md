scrapy crawl test -s JOBDIR=data -0 items.csv

watch -n 1 -d 'wc -l items.csv;du -h items.csv'

