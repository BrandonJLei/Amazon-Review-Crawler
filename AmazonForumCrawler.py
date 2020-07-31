import re
import urllib.request
import bs4
import csv

def crawlReviewsOnPage(url,pageNumber, FILE_NAME):
    header = {'User-Agent': 'Mozilla/5.0'}
    pageRequest = urllib.request.Request(url=url, headers=header)
    pageReq = urllib.request.urlopen(pageRequest)
    pageSauce = pageReq.read()
    pageSoup = bs4.BeautifulSoup(pageSauce, 'lxml')

    reviewsCsv = open(FILE_NAME, "a", encoding = "utf-8", newline = "")
    fieldnames = ["PageNum", "URL", "Rating", "Date", "Title", "Review"]
    csv_writer = csv.DictWriter(reviewsCsv, fieldnames=fieldnames)

    pageReviews = pageSoup.find_all("div", class_ = "a-section celwidget")
    for review in pageReviews:
        #Gathering the data to be written
        rating = review.find("i", class_ = re.compile("a-icon a-icon-star a-star-\d review-rating")).findChild().text.strip()
        title = review.find("a", class_ = "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold").text.strip()
        date = review.find("span", class_ = "a-size-base a-color-secondary review-date").text.strip()
        reviewText = review.find("span", class_ = "a-size-base review-text review-text-content").findChild().text.strip()

        #Writing the data to FILE_NAME
        csv_writer.writerow({"PageNum":pageNumber, "URL": url, "Rating":rating, "Date": date, "Title" : title, "Review": reviewText})
    reviewsCsv.close()
    
if __name__ == '__main__':
################################             CHANGE THESE VALUES              ###############################
    #Find the patern in the url's for the pages of reviews
    URL_PART_1 = 'https://www.amazon.com/Rain-Labs-Animal-Sounds/product-reviews/B01AHGU3M6/ref=cm_cr_arp_d_paging_btm_next_'
    URL_PART_2 = '?ie=UTF8&reviewerType=all_reviews&pageNumber='
    #Name of the file you wish to write to (will auto create it for you if it doesn't exist)
    FILE_NAME = "AnimalSounds.csv"
    #Num of pages you wish to crawl
    NUM_PAGES = 9
#############################################################################################################

    #This is for writing the header of the csv file, the content will be writen in crawlReviewsOnPage()
    reviewsCsv = open(FILE_NAME, "a", encoding="utf-8", newline="")
    fieldnames = ["PageNum", "URL", "Rating", "Date", "Title", "Review"]
    csv_writer = csv.DictWriter(reviewsCsv, fieldnames = fieldnames)
    csv_writer.writeheader()
    reviewsCsv.close()

    for pageNumber in range(1, NUM_PAGES + 1):
        print("Currently on Page:", pageNumber)
        full_url = URL_PART_1 + str(pageNumber) + URL_PART_2 + str(pageNumber)
        crawlReviewsOnPage(full_url, pageNumber, FILE_NAME)


