# Top 1500 Hindi Movies (IMDB)

## Project Overview:
I used Python's web scraping capabilities to compile data on the top 1500 Hindi Movies and TV Series. These results are based on IMDB ratings alone and were received through this [link](https://www.imdb.com/search/title/?title_type=feature,tv_series&release_date=1950-01-01,2024-12-31&countries=IN&languages=hi). 

### Objective: 
The purpose of this project is to demonstrate my ability to gather data and construct datasets from scratch. This beginner project is intended to be a learning experience, and I plan to continue building the skills I learned through this project in future projects. 

### Methodology:
I utilized Python's Beautiful Soup library to parse the website's HTML code. Then, I created a "for loop" to extract data from the individual movie containers. This was useful for extracting data from the first 50 movies; however, I needed to use Selenium WebDriver (instead of the Requests library) to manually scroll to the bottom of the IMDB page and click the "50 More" button. This process was repeated 30 times to populate the desired 1500 items. After this point, the program proceeded as it originally had: I used Beautiful Soup Version 4 to parse the HTML, looped through the movie containers, and stored the resulting data in their respective variables. At the end of the program, the variable data is verified and then written in a CSV file.

### Results:
The program creates and stores a CSV file containing the compiled raw data. The features included in this file are as follows: Title, Year Released, Media Type, Movie Duration, Audience Rating, Audience Vote Count, Metacritic Score, and Plot Description.

### Challenges and Learnings:
The first challenge I faced was overcoming the "Forbidden 403" error. I overcame this error by including a user agent so the website didn't automatically shut my computer out. After finally succeeding in gathering some data, I realized my program would not collect any more data than the initial 50 movies. I realized this was because the URL only populated the first 50 movies on the page, and I had to click the "50 More" button each time I wanted to populate more movies. I overcame this challenge by utilizing Selenium WebDriver's capabilities to scroll and click the button. Since I had no experience using this library, I used ChatGPT to make the information-gathering process more efficient. This included learning which ChromeDriver version to install for my computer and which functions to use in order to create a functioning "button-clicker." 

### Code and Repository:
This repository currently contains the final code and CSV file. I will be adding a full project blog soon with my previous attempts and a breakdown of how I achieved the final result. Stay tuned for more updates!
