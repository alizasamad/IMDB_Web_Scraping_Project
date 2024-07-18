# IMPORT LIBRARIES
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import csv

# PATH TO CHROMEDRIVER
service = Service('/Applications/chromedriver-mac-arm64/chromedriver', port=9516)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode to not open a browser window
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')
options.add_argument('--ignore-certificate-errors')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Add a user agent header

# INITIALIZE WEBDRIVER
driver = webdriver.Chrome(service=service, options=options)
print("WebDriver initialized successfully.")


# NAV TO URL
url ='https://www.imdb.com/search/title/?title_type=feature,tv_series&release_date=1950-01-01,2024-12-31&countries=IN&languages=hi'
driver.get(url)


# LOOP THROUGH 'SEE MORE' BUTTON
click_count = 0
while click_count < 30:
    try:
        # WAIT FOR BUTTON TO BE CLICKABLE
        load_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ipc-see-more__text')))

        # SCROLL TO BUTTON
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
        time.sleep(2)

        # CLICK THE BUTTON
        load_more_button.click()
        print('Clicked "See More" button...')
        click_count+=1  # view 50 more movies

    except Exception as e:
        print(f"Exception occured: {e}")
        break  # exit loop if error OR no more button

    
# PARSE HTML WITH BEAUTIFUL SOUP
soup = BeautifulSoup(driver.page_source, 'html.parser')

# INITIALIZING LISTS TO STORE DATA
titles = []
years = []
durations = []
descriptions = []
ratings = []
votes = []
metacritic = []
mediaType = []
        
try:
    # IDENTIFY MOVIE CONTAINERS
    movie_containers = soup.find_all('li', class_='ipc-metadata-list-summary-item')
    for container in movie_containers:
        
        # FIND & STORE MOVIE TITLES
        movieTitles = container.find_all('h3', class_='ipc-title__text')
        for movie in movieTitles:
            if movie.text[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                titles.append(movie.text)

        # FIND & STORE YEARS
        movieYear = container.find_all('span', class_='sc-b189961a-8 kLaxqf dli-title-metadata-item')
        for year in movieYear:
            if ((year.text[-1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ']) and (year.text[0] in ['1', '2'])):
                years.append(year.text.strip())

        # FIND & STORE DESCRIPTIONS
        movieDesc = container.find_all('div', class_='ipc-html-content-inner-div')
        if len(movieDesc) == 1:
            descriptions.append(movieDesc[0].text)
        else:
            descriptions.append('NA')

        # FIND & STORE AUDIENCE RATINGS
        movieRatings = container.find_all('span', class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating')
        if len(movieRatings) > 0:
            for rating in movieRatings:
                split = rating.text.split('\xa0')
                ratings.append(split[0])
                votes.append(split[1][1:-1])
        else:
            ratings.append('NA')
            votes.append('NA')
    
        # FIND & STORE DURATION 
        movieDuration = container.find_all('span', class_='sc-b189961a-8 kLaxqf dli-title-metadata-item')
        if len(movieDuration) > 1:
            if movieDuration[1].text[-1] in ['h', 'm']:
                durations.append(movieDuration[1].text)
            else:
                durations.append('NA')
        else:
            durations.append('NA')

        # FIND METACRITIC SCORE
        metaScore = container.find_all('span', class_='sc-b0901df4-0 bcQdDJ metacritic-score-box')
        if len(metaScore) == 1:
            metacritic.append(metaScore[0].text)
        else:
            metacritic.append('NA')

        # MOVIE/TV SHOW IDENTIFIER
        movie_TV = container.find_all('span', class_='sc-b189961a-3 hidKPx dli-title-type-data')
        if len(movie_TV) == 1:
            mediaType.append('TV SERIES')
        else:
            mediaType.append('MOVIE')
                
                
except Exception as e:
    print(f"Exception occurred: {e}")


# CLOSE BROWSER
driver.quit()
print("Browser successfully closed, waiting on CSV file...")

# VERIFY DATA
print(len(titles))
print(len(years))
print(len(descriptions))
print(len(ratings))
print(len(durations))
print(len(metacritic))
print(len(mediaType))
print(len(votes))


# OPEN A NEW CSV FILE
file = open('IMDB_Indian_Scraped.csv', 'w')

# CREATE A VARIABLE FOR WRITING TO THE CSV
writer = csv.writer(file)

# CREATE HEADER ROW
writer.writerow(['Title', 'Year Released', 'Media Type', 'Movie Duration', 'Audience Rating', 'Audience Vote Count', 'Metacritic Score', 'Plot Description'])

# ADD DATA TO FILE
for title, year, rating, description, duration, meta, media, vote  in zip(titles, years, ratings, descriptions, durations, metacritic, mediaType, votes):
    writer.writerow([title, year, media, duration, rating, vote, meta, description])  # write each item as new row in file
    
#CLOSE THE CSV FILE
file.close()
print("CSV file successfully saved")
