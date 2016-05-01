#!/bin/bash
mongoexport --db=twitter_db --collection=tweets_2  --type csv --fields id,search_term,location,age,sentiment,score,user.followers_count > processed_data.csv
