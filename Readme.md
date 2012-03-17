Footy
=====

An Eredivise (Dutch football leauge) prediction program. Runs several supervised algorithms over scraped match results, picks the best algorithm based on its normal distribution of its predictions, and used it makes new predictions.

Usage
-----

    ./scrape.sh   # get match results from eredivisielive.nl
    ./predict.py  # run algorithms and use best one to predict results

Example predictor output:

    …
    
    score: 4.89 (-2.28 ± 2.60) for NaiveClassifier
    score: 3.01 (-0.39 ± 2.61) for MeanScore
    score: 2.63 (-0.40 ± 2.23) for LinearRegressionScore

    NEW PREDICTIONS by LinearRegressionScore

             Vitesse 2 - 1 Heracles Almelo
        RKC Waalwijk 2 - 1 De Graafschap
           Excelsior 2 - 2 Roda JC Kerkrade
           VVV-Venlo 1 - 2 NEC
        ADO Den Haag 2 - 2 Ajax
                 PSV 1 - 1 sc Heerenveen
          FC Utrecht 2 - 1 FC Groningen
           FC Twente 1 - 2 Feyenoord
                  AZ 1 - 1 NAC Breda

See `predict.py` for the algorithm descriptions and the list of future matches to predict.

Requirements
------------

 * Python 2.7 (other versions may work, too)
 * [Scrapy](http://scrapy.org/) to run the scraper
 * [matplotlib](http://matplotlib.sourceforge.net/) if you want to plot some graphs
