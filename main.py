"""
    Script designed to run on Windows machines
    
    Requirments:
        python2.7
        requests
        beautifulsoup4

    Script requires an <url> argument !
    Example of running script:
        python main.py <url>
    
    This script was designed for downloading all alboms
    with containing mp3 files from http://pendujatt.net/ website.
    
    For further development and new offers:
    
        Vardan Aloyan: 
            gmail:    valoyan2@gmail.com
            telegram: @vardanaloyan

        Kiril Vardapetyan:
            gmail:    vardapetyankiril@gmail.com
            telegram: @kvardapetyan
"""

"""Standard Library"""
import sys, os,re 

"""3rd party Library"""
import requests
from bs4 import BeautifulSoup

os.environ['PYTHONWARNINGS']="ignore:Unverified HTTPS request"

rlist = ['<', '>', ':', '"', '|', '?', '*']
#rlist = ['"', '-']

def correct(fname):
    """For correcting path string"""
    for i in fname:
        if i in rlist:
            fname = fname.replace(i,"_").strip()
    return fname
    

def parse_page():
    """Main script for parsing web site, and downloading mp3 files"""
    session = requests.Session()
    session.max_redirects = 9999999
    page = session.get(sys.argv[1], verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    res =  soup.find_all('a', class_='album', href=True)
    domain = sys.argv[1].split('/')
    for k, i in enumerate(res):
        album =  i.text.strip()
        print 'Downloading "{}" albom'.format(album)
        if not os.path.exists(correct(i.text)):
            os.makedirs(correct(i.text.strip()))
        sub_page = session.get(domain[0] + '//' + domain[2] +  i['href'], verify=False)
        soup = BeautifulSoup(sub_page.content, 'html.parser')
        list_song =  soup.find_all('a', class_='song', href=True)
        for i in list_song:
            sub_album = i.text.strip()
            if not os.path.exists(correct(album) + '/' + correct(i.text.strip())):
                os.makedirs(correct(album) + '/' + correct(i.text.strip()))
            music_page = session.get(domain[0] + '//' + domain[2] +  i['href'], verify=False)
            soup = BeautifulSoup(music_page.content, 'html.parser')
            list_song =  soup.find_all('a', class_='download', href=True)
            for i in list_song:
                doc = session.get(i['href'], verify=False) 
                frm = i['href'].split('/')[-1]
                frm = re.sub(r'\([^)]*\)', '', frm)
                with open(correct(album) + '/' + correct(sub_album) + '/' + correct(i['href'].split('/')[-2]).split('_')[0] + "_" + frm, 'wb') as f:
                    f.write(doc.content)
    print "Finished ...".format(len(res))

if __name__ == "__main__":
    parse_page()
