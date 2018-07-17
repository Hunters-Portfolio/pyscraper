# Program for scraping a given webpage for all of its images]
# Usage: python pyscraper.py <url> [folder]

# Libraries:
from html.parser import HTMLParser
import requests
import sys
import os
import datetime

# Classes:
class ImageParser(HTMLParser):
    urlLoc = ""

    # Constructor
    def __init__(self, urlL):
        self.urlLoc = urlL
        HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        # Only want 'img' and 'a' tags, so that's what we'll check for
        if tag != "img" and tag != "a":
            return
        # Make sure links point to images if we're scraping them
        filetypes = ["jpeg","gif","jpg","png","bmp","svg"]
        # Find the 'src' attribute, and download the image
        for x in attrs:
            if x[0] == "src" and tag == "img":
                downloadImage(x[1])
            elif x[0] == "href" and tag == "a" and x[1].split(".")[-1] in filetypes:
                downloadImage(x[1])
    
    def parsePage(self):
        r = requests.get(self.urlLoc)
        self.feed(r.text)

# Code starts here:

# Create a list of already downloaded files to avoid double-dipping
alreadyDownloaded = []

def downloadImage(urlLoc):
    # Ensure that the url is correct
    urlLoc = formatUrl(urlLoc)
    # Grab the last segment of the url for the filename
    # eg. "i.4cdn.org/g/1531602832712s.jpg" becomes "1531602832712s.jpg"
    filename = urlLoc.split('/')[-1]
    # Download the image and save to disk
    path = foldername + "/" + filename
    print("Downloading image " + urlLoc)
    # Double check to see if the image has already been downloaded
    if urlLoc in alreadyDownloaded:
        print("Image already downloaded!")
        return
    # Download time
    r = requests.get(urlLoc, stream=True)
    # Make sure we're good to go
    if r.status_code == 200:
        # Open the file on disk and write the image stream to it
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        # Add it to the list so we don't download the image again
        alreadyDownloaded.append(urlLoc)
    # Didn't work, abort the download
    else:
        print("Error downloading image!")
        print("Expected status 200, got status " + str(r.status.code))
        
# Strip anything that might cause requests to panic and break
# Make sure it's in the right format so requests doesn't panic and break
def formatUrl(urlStr):
    urlStr = urlStr.replace("https://","").replace("http://","")
    if urlStr[0:2] == '//':
        urlStr = urlStr[2:]
    return "http://" + urlStr

# Double check to make sure the user is using the program correctly
if len(sys.argv) < 2:
    print("Invalid arguments!")
    print("Useage: python pyscraper.py <url> [folder]")
    exit(1)

# Use the user provided folder name or just default to today's date
if len(sys.argv) == 3:
    foldername = sys.argv[2]
else:
    foldername = datetime.date.today().strftime("%B %d, %Y")
# Make sure the folder exists, if not, create it
if not os.path.exists(foldername):
    os.makedirs(foldername)

# Create an ImageParser object and run the code
parser = ImageParser(sys.argv[1])
parser.parsePage()
