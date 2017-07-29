
import urllib
import os.path
import urllib2
from bs4 import BeautifulSoup
import re

#### functions ######

# get the year of the PDF
def get_year_from_pdf_filename(pdf_filename):
    return re.findall(r'\d+',pdf_filename)[0] # findall returns a list, I need only the first element of the list so I add the index [0] as this represents the first element


# check if the year exists, if not make a folder for year
def define_pdf_path(path, pdf_filename, tittle):
    year = re.compile('\d+')
    if year.search(tittle):
        path_1 = path + get_year_from_pdf_filename(tittle) + "/"
    else:
        path_1 = path + get_year_from_pdf_filename(pdf_filename)+"/" # concatenate pdf_path with pdf_filename

    if os.path.isdir(path_1)== False:
        os.makedirs(path_1) # generate pdf_path containing year folder
    return path_1   # returns the final path


 # check if the file already exists
def pdf_exists(path_2):
    return os.path.isfile(path_2)  #returns True or False, whether the file exists already or not

# opens the url, if it fails it keeps trying
def access_url(url_to_access, headers):
    '''
    Keeps trying to access a URL until we do so successfully
    '''
    iterate = True
    while iterate:
        try:
            # As I'm accessing again IMF with a different link, I have to introduce myself again with my user-agent.
            request_url = urllib2.Request(url_to_access, headers=headers)
            # now I can open and read the link
            response_url = urllib2.urlopen(request_url, timeout=20).read()
            iterate = False
        except Exception, e:
            print "Failed to open url with error:", str(e)
    return response_url

# downloads the pdf, it it fails it keeps trying
def donwload_PDF(url, path):
    iterate = True
    while iterate:
        try:
            urllib.urlretrieve(url, filename= path + ".pdf")
            iterate = False
        except Exception, e:
            print "Failed donwloading PDF with error:", str(e)
    return



####### Getting the PDFs ####

def main():


    # lets introduce myself to IMF
    # for that I need to use a user-Agent, to find out this information I used http://www.whoishostingthis.com/tools/user-agent/
    headers = {'User-agent': 'Mozilla/5.0'}
    request = urllib2.Request("http://www.imf.org/external/np/sec/aiv/index.aspx?listby=c", headers=headers)
    # Now that I have introduce myself to IMF, IMF allows me to connect to their site
    # open and read the website
    response = urllib2.urlopen(request).read()
    # parse the website
    soup = BeautifulSoup(response,'html.parser')
    # define a pattern with regex to look for
    pattern = re.compile("country/[A-Z]{1,3}") #regex, this pattern will look for text that looks like 'country/XXX' X represents a letter

    # We need to loop inside the website to find the pattern per country and get the link of each country
    for countries in soup.findAll('a', attrs={'href': pattern}):

        link_1 = countries['href']+"?type=9998" # the link is incomplete, so I have to concatenate each one with '?type=9998' to be able to acces the link
        print link_1
        # run the function access_url. similar code of Lines 53-57 was used before in this area of the script. But I need to
        # run a 'while' loop so we decided to create a function for that, so now the function will return the value for the 'response' variable
        response_c = access_url(link_1, headers)
        # parse the site
        soup_c = BeautifulSoup(response_c,'html.parser')
        # create a pattern to look for
        pattern_c = re.compile("Article IV Consultation") # pattern I need to find inside the text
        Href_pattern = re.compile("aspx") #regex. pattern I need to find inside the tag under the 'href' attribute

        # Now I need to loop inside the country and look for the links of the 'article IV' documents
        for country in soup_c.findAll('a', attrs={'href': Href_pattern}, text=pattern_c): # searches for the tag 'a', then searches for a pattern inside the 'href', then searches for a pattern inside the text (text of the link, text inside the tag <a href="..."> text</a>
            link_2 = "http://www.imf.org" + country['href'] # The link can't be access using only the 'href', so I had to concatenate it with "http://www.imf.org"
            print link_2, country.text

            # run the function access_url. similar code of Lines 53-57 was used before in this area of the script. But I need to
            # run a 'while' loop so we decided to create a function for that, so now the function will return the value for the 'response' variable
            response_d = access_url(link_2,headers)
            # parse the site
            soup_d = BeautifulSoup(response_d,'html.parser')
            # create a pattern to look for
            pattern_d = re.compile("Free Full text") # pattern I need to fin inside the text
            ashx_pattern = re.compile("ashx") #regex. pattern I need to find inside the tag under the 'href' attribute

            for doc in soup_d.findAll('a',attrs={'href': ashx_pattern}, text=pattern_d):
                myPDF = "http://www.imf.org" + doc['href']
                print myPDF
                pathPDF = "/Users/astrid/Downloads/PDF_Download/"
                pdf_name = re.sub(r'[^a-zA-Z0-9 ]', r'',country.text) #country.text
                path_file = define_pdf_path(pathPDF, myPDF, pdf_name) + pdf_name[:250] # Mac can handle a [255] max unicode for file names
                if not pdf_exists(path_file): # I initally used the code "if pdf_exists(path_file)==False" but is cleaner using "not"


                    _= access_url(myPDF, headers)

                    # Download the PDF
                    #urllib.urlretrieve(myPDF, filename= path_file +".pdf")
                    _= donwload_PDF(myPDF, path_file)


            #break
        #break

if __name__ == '__main__':
    main()



