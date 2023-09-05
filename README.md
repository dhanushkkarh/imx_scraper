**SCRAPER FOR IMX.TO**
Scraper galleries from imx.to (full images) to the local disk.

**usage**
1. Search the required gallery from yandex.com (through dorks)
2. Dork is site:imx.to <gallery/model name> (eg. "site:imx.to wals nikki")
3. copy the entire search results and paste it in text_corpus.txt
4. The corpus_handler in 'scarperfromsearch.py' will identify gallery links and starts downloading each gallery
5. The destination is hard coded in the soruce code. make sure to edit it.
6. for each link, the script created a new folder to store its images
7. on each folder, along with images, there is a file called 'details.txt'
8. details.txt contains all the links from where the images were downloaded
9. example:
     https://imx.to/u/t/2020/09/06/2cwqvh.jpg gives the thumbnail version
     https://imx.to/i/t/2020/09/06/2cwqvh.jpg gives the full HD image (replace the u with i)


**NOTES**

SCRIPT USES MAX MULTITHREAIDING.
AVOID FEEDEING MORE THAN 3 PAGES OF RESULTS AS IT COULD CHOKE THE NETWORK AND MESS UP THE PROCESS
COMPLETED_DOWNLOADS.TXT TRACKS THE COMPLETED DOWNLOADS.
   

