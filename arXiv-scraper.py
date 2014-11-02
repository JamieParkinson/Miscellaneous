import feedparser
from urllib2 import Request, urlopen
from StringIO import StringIO
from pyPdf import PdfFileReader
from multiprocessing.dummy import Pool as ThreadPool
import numpy

NPAPERS = 1000

def getNPersonal(paper):
	#print paper.title

	pdfLinks = paper.links
	for link in pdfLinks:
		try:
			if link.title == 'pdf':
				pdfURL = link['href']
				break
		except AttributeError:
			continue
	try:
		rFile = urlopen(Request(pdfURL)).read()
		mFile = StringIO(rFile)
		pdfFile = PdfFileReader(mFile)
	
		nPages = pdfFile.getNumPages()
		thisNPersonal = 0
		for page in range(0, nPages):
			pageStr = pdfFile.getPage(page).extractText().lower()
			thisNPersonal += pageStr.count(' we ')
			thisNPersonal += pageStr.count(' i ')
	except:
		print "Error reading file"
		return -1
	
	thisNPersonal = 0 if thisNPersonal == 1 else thisNPersonal
	print thisNPersonal
	return thisNPersonal

url = 'http://export.arxiv.org/api/query?search_query=all:physics&max_results=' + repr(NPAPERS)
papers = feedparser.parse(url).entries

pool = ThreadPool(4)
results = pool.map(getNPersonal, papers)
pool.close()
pool.join()

NPAPERS -= results.count(-1)
percentage = 100*numpy.count_nonzero(results)/NPAPERS
print 'Percentage of papers using personal pronouns: ' + repr(percentage) + '%'
	
