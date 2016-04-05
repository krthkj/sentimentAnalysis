# Extracting twitter data
setwd("../test/")

library("twitteR")
library("ROAuth")

# Credenciales

consumer_key =   "cZUYhg1AGiFeERJyk1yEgE5oI"
consumer_secret = "JHkGyWALQNe1avsRYJovsUwqzCY0nWCtG9nFrq0JuNmKbMs0u6"
access_token = "178344419-BpArn9mWvIgRd0m0wZ83iI52BzgLjR7IVgBCR6Yg"
access_secret = "Yj6jijQWx4FWYw6TAhJDEi9lwTbdrcidUNBOBh3IwuR6l"
setup_twitter_oauth(consumer_key, consumer_secret, access_token, access_secret)
load_twitter_oauth("cred_1.RData")


