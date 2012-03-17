Footy
=====

An Eredivise (Dutch football leauge) prediction program. Runs several supervised algorithms over scraped match results, picks the best algorithm based on its normal distribution of its predictions, and used it makes new predictions.

Usage
-----

    ./scrape.sh   # get match results from eredivisielive.nl
    ./predict.py  # run algorithms and use best one to predict results

See `predict.py` for the algorithm descriptions and the list of future matches to predict.

Requirements
------------

 * Python 2.7 (other versions may work, too)
 * [Scrapy](http://scrapy.org/) to run the scraper
 * [matplotlib](http://matplotlib.sourceforge.net/) if you want to plot some graphs
