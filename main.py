# Program for scraping a given webpage for all of its images

# Libraries:
from html.parser import HTMLParser
import requests
import sys
import os
import datetime

# Classes:
class ImageParser(HTMLParser):
    urlLoc = ""
    
    def __init__(self, urlL):
        self.urlLoc = urlL
        HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        # Only want 'img' tags, so that's what we'll check for
        if tag != "img":
            return
        # Find the 'src' attribute, and download the image
        for x in attrs:
            if x[0] == "src":
                print("Downloading image " + x[1])
                downloadImage(x[1].strip("https://").strip("http://"))

    def handle_data(self, data):
        # Don't care about data, so just return
        return

    def parsePage(self):
        r = requests.get(self.urlLoc)
        self.feed(r.text)

# Code starts here:
def getHTML(urlLoc):
    parser = ImageParser(urlLoc)
    parser.parsePage()

def downloadImage(urlLoc):
    # Grab the last segment of the url for the filename
    # eg. "i.4cdn.org/g/1531602832712s.jpg" becomes "1531602832712s.jpg"
    filename = urlLoc.split('/')[-1]
    # Create a folder with the date and time of access
    foldername = datetime.date.today().strftime("%I:%M%p on %B %d, %Y")
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    # Download the image and save to disk
    path = foldername + "/" + filename
    r = requests.get("http://"+urlLoc, stream=True)
    if r.status.code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        print("Error downloading image!")
        print("Expected status 200, got status " + str(r.status.code))
        

print(sys.argv)

if len(sys.argv) < 2:
    print("Invalid arguments!")
    exit()

getHTML(sys.argv[1])
