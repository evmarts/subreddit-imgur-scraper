import urllib3
import urllib2
import sys 
import os 
import io
from bs4 import BeautifulSoup

## returns the html representation of the page at the url
def getHTML(url):
	header = { 'User-Agent' : 'my happy little bot' }
	req = urllib2.Request(url, headers=header)
	html = urllib2.urlopen(req).read()
	return html

## returns the html metadata for each post 
def parseHTML(html):
	soup = BeautifulSoup(html, 'html.parser')
	links = soup.find_all("a",class_="title may-blank outbound")
	return links

## returns a tuple containing the title of the post as a string and 
#  the href link to the post's content 
def getPostTuple(posts_html):
	titles = []
	hrefs = [] 
	for post_html in posts_html:
		titles.append((post_html.contents[0]).encode('utf-8'))
		hrefs.append((post_html.get("href")).encode('utf-8'))
	return (titles,hrefs)

def isImgurHref(href):
	return 'imgur.com' in href

def isImgurAlbum(opath):
	return "/a/" in opath

## download the imgur image from the given reddit post url
def downloadImgurImage(url):
	opath = getPath(url)				# create a path for the downloaded image
	download_url = getDownloadUrl(url) 	# convert the reddit post url to a url we can easily download with
	if not isImgurAlbum(opath):			# do not download imgur albums
		with open(opath, 'wb+') as f:
			req = urllib3.PoolManager().urlopen("GET", download_url, preload_content=False)
			buf = io.BufferedReader(req)
			f.write(buf.read())
			f.close()
	return

## returns a path for the downloaded image (e.g. .../workingdir/HLXFacj.jpg)
def getPath(url):
	path = os.path.dirname(os.path.realpath(__file__))
	file_name = getFileName(url)
	opath = os.path.abspath(os.path.join(path, file_name))
	return opath

## returns a new imgur url that we can easily download from
def getDownloadUrl(url):
	domain = "http://i.imgur.com/"
	file_name = getFileName(url)
	file_ext = getFileExtension(file_name)
	download_url = "{0}download/{1}".format(domain, file_name)
	return download_url

## gets the name of the imgur file (e.g. jRrOWqD.jpg, HLXFacj.jpg)
def getFileName(url):
	return url.split("imgur.com/")[1]

## returns the file extension (e.g. getFileExtension('HLXFacj.jpg') returns '.jpg')
def getFileExtension(file_name):
	file_ext = ""
	fileSplit = file_name.split(".")
	n = len(fileSplit)
	if (n > 1):
		file_ext = fileSplit[1]
	return file_ext

def main():
	subreddit = raw_input("Enter a subreddit: ")
	url = 'http://reddit.com/r/' + str(subreddit)
	html = getHTML(url)
	posts_html = parseHTML(html)
	titles = getPostTuple(posts_html)[0]
	hrefs = getPostTuple(posts_html)[1]
	for href in hrefs:
		if isImgurHref(href):
			print "downloading image: " + str(href) + " ..."
			downloadImgurImage(href)

main()
