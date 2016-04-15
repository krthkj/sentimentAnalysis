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
    cerdentials = get_credentials()
    
    return

def get_credentials():
    api_keys = {}
    api_keys['twitter_consumer_key']    = ''
    api_keys['twitter_consumer_secret'] = ''

    try:
        import credential
        if credentials.twitter_consumer_key == '' or credentials.twitter_consumer_key == 'TWITTER_CONSUMER_KEY' :
            raise ImportError
        elif credentials.twitter_consumer_key == '' or credentials.twitter_consumer_key == 'TWITTER_CONSUMER_SECRET' :
            raise ImportError
        else:
            api_keys['twitter_consumer_key']    = credentials.twitter_consumer_key
            api_keys['twitter_consumer_secret'] = credentials.twitter_consumer_secret
    except ImportError:
        print "twitterRest.py: ALERT: No credentials.py found"
        api_keys['twitter_consumer_key']    = raw_input("Enter your Twitter API consumer key: ")
        api_keys['twitter_consumer_secret'] = raw_input("Enter your Twitter API consumer secret: ")
    except:
        print ("twitterRest.py: ERROR: unable to import credentials - unknown reason")

    return

# command line arguments are read from here.
if __name__ == "__main__":
    if len(sys.argv) == 2:
        print("twitterRest.py: Reading alternate input file")
        read(sys.argv[1])
    
    elif len (sys.argv) == 1 :
        print("twitterRest.py: Reading default input file")
        read('searchMe.txt')

    else:
        print("twitterRest.py: ERROR: cannot accept multiple files")
        sys.exit()

