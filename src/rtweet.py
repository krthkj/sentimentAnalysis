#!/usr/bin/env python
# MIT License
#
# Copyright (c) 2016 Karthik Jain <karthikjain@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import requests, json, urllib, urllib2, base64
import random

def get_state():
    state_list = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
    return random.choice(state_list)


def get_age():
    return random.randint(18,60)

def read(filename):
    searchList = []
    with open (filename) as f:
        for line in f:
            searchList.append(line.rstrip())

    print (searchList)
    main (searchList)
    
    return

def main(searchList):
    # Get credentials for Twitter
    api_keys = get_credentials()
    auth = oauth (api_keys)
    
    return

def oauth(api_keys):
    try:
        # Encode credentials
        encoded_credentials = base64.b64encode(api_keys['twitter_consumer_key'] + ':' + api_keys['twitter_consumer_secret'])        
        # Prepare URL and HTTP parameters
        post_url = "https://api.twitter.com/oauth2/token"
        parameters = {'grant_type' : 'client_credentials'}
        # Prepare headers
        auth_headers = {
            "Authorization" : "Basic %s" % encoded_credentials,
            "Content-Type"  : "application/x-www-form-urlencoded;charset=UTF-8"
            }

        # Make a POST call
        results = requests.post(url=post_url, data=urllib.urlencode(parameters), headers=auth_headers)
        response = results.json()

        # Store the access_token and token_type for further use
        auth = {}
        auth['access_token'] = response['access_token']
        auth['token_type']   = response['token_type']

        print("rtweet.py: Twitter OAuth test = PASS")
        return auth

    except Exception as e:
        print("rtweet.py: Twitter OAuth test = FAIL", e)
        print("Twitter consumer key:", api_keys['twitter_consumer_key'])
        print("Twitter consumer secret:", api_keys['twitter_consumer_secret'])
        sys.exit()

def get_credentials():
    api_keys = {}
    api_keys['twitter_consumer_key']    = ''
    api_keys['twitter_consumer_secret'] = ''

    try:
        import credentials
        api_keys['twitter_consumer_key']    = credentials.twitter_consumer_key
        api_keys['twitter_consumer_secret'] = credentials.twitter_consumer_secret
    except ImportError:
        print("rtweet.py: ALERT: No credentials.py found")
        api_keys['twitter_consumer_key']    = raw_input("Enter your Twitter API consumer key: ")
        api_keys['twitter_consumer_secret'] = raw_input("Enter your Twitter API consumer secret: ")
    except:
        print("rtweet.py: ERROR: unable to import credentials - unknown reason")

    return api_keys

# command line arguments are read from here.
if __name__ == "__main__":
    if len(sys.argv) == 2:
        print("rtweet.py: Reading alternate input file")
        read(sys.argv[1])
    
    elif len (sys.argv) == 1 :
        print("rtweet.py: Reading default input file")
        read('searchMe.txt')

    else:
        print("rtweet.py: ERROR: cannot accept multiple files")
        sys.exit()

