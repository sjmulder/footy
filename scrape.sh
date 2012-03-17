#!/bin/sh
pushd scraper \
    && scrapy crawl match_results -o ../match_results.json -t json \
    ; popd