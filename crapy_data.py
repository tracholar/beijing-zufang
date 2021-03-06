import time
import gzip
import os
import urllib, urllib2, re, smtplib, urlparse, time, threading
from lxml import etree
from StringIO import StringIO

def get_dom_from_string(html):
	try:
		tree = etree.parse(StringIO(html), etree.HTMLParser())
	except Exception:
		tree = etree.parse(StringIO(''), etree.HTMLParser())
	return tree
	
def dom_to_html(elem):
	return etree.tostring(elem, pretty_print=True)	

def dom_text_content(elem):
	
	return re.sub(r'\s+', '-', etree.tostring(elem, method='text',encoding='unicode').strip())

	


visited_urls = set()
	
def save_url(url):
	f = open('urls.txt','a')
	f.write(url + '\n')
	f.close()
	
base_url = r'http://zu.fang.com/house/i%d%d/'

hourse_dl_re = re.compile(r'<dl class="list hiddenMap rel">.+?</dl>',  re.S)

outfile = 'fj_%s.txt' % time.strftime('%Y%m%d')

if os.path.exists(outfile):
	newday = False
else:
	newday = True
	
fp = open(outfile, 'a');

for s in range(1,4):
	for i in range(1,101):
		url = base_url % (s, i)
		html = urllib2.urlopen(url).read()
		html = gzip.GzipFile(fileobj=StringIO(html)).read()
		#open('data.html','w').write(html)
		print url
		
		dls = hourse_dl_re.findall(html)
		
		for dl in dls:
			#open('dl.html','w').write(dl)
			T = get_dom_from_string(dl.decode('gbk','ignore'))
			link = T.find('//p[@class="title"]/a')
			title = link.attrib['title']
			href =  link.attrib['href']
			
			if href in visited_urls:
				print 'found!' , href
				continue
			else:
				save_url(href)
				visited_urls.add(href)
				
			
			infos = dom_text_content(T.find('//p[@class="font16 mt20 bold"]'))
			
			addrs = dom_text_content(T.find('//p[@class="gray6 mt20"]'))
			
			price = T.find('//span[@class="price"]').text
				
			data = [title, href,  infos, addrs, price]
			
			fp.writelines('\t'.join(data).encode('utf-8','ignore') + "\n")
			
			#print href
		#break
		time.sleep(2)
		

fp.close()

		

