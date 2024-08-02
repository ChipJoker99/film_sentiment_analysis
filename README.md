# Film Sentiment Analysis

## Description

This project uses Python to scrape movie titles from Flickchart, obtain movie information from the OMDb API, and analyze the sentiment of movie reviews from IMDb. The sentiment of the reviews is analyzed using the NLTK library. The results are saved in a CSV file and displayed in a bar chart.

## Features

- **Movie Title Scraping**: Uses Selenium and BeautifulSoup to extract movie titles from Flickchart.
- **OMDb API Requests**: Obtains movie information such as title, year, and rating.
- **Review Scraping**: Extracts movie reviews from IMDb.
- **Sentiment Analysis**: Uses NLTK to analyze the sentiment of the first 10 reviews of each movie.
- **Data Saving**: Saves the collected data in a CSV file with a unique name based on the date and a progressive number.
- **Logging**: Logs operations in a log file with a unique name based on the date and a progressive number.

## Requirements

- Python 3.11
- Python Libraries: `requests`, `pandas`, `matplotlib`, `beautifulsoup4`, `selenium`, `webdriver_manager`, `nltk`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ChipJoker99/film_sentiment_analysis.git
    cd film_sentiment_analysis
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Manually download the `vader_lexicon` file and place it in the correct directory:
    - Download the `vader_lexicon` file from this [link ](https://github.com/cjhutto/vaderSentiment/blob/master/vaderSentiment/vader_lexicon.txt)
    - Create a folder named `nltk_data` in your user directory (e.g., `C:\Users\YourUsername\nltk_data`).
    - Inside the `nltk_data` folder, create a subfolder named `sentiment`.
    - Save the `vader_lexicon.txt` file in the `sentiment` folder.

## Usage

1. Run the script:
    ```bash
    python sentiment.py
    ```

2. The collected data will be saved in a CSV file in the `data` folder with a unique name based on the date and a progressive number.

3. The operation logs will be saved in a log file in the `logs` folder with a unique name based on the date and a progressive number.

## Example Output

Example of collected data:
```csv
Title,Year,Rating,Sentiment
Star Wars: Episode IV - A New Hope,1977,8.6,0.6038
Star Wars: Episode V - The Empire Strikes Back,1980,8.7,0.96146
The Godfather,1972,9.2,0.9686199999999999
Raiders of the Lost Ark,1981,8.4,0.9474699999999998
The Shawshank Redemption,1994,9.3,0.9797
Pulp Fiction,1994,8.9,0.8562999999999998
Star Wars: Episode VI - Return of the Jedi,1983,8.3,0.88724
Back to the Future,1985,8.5,0.9636899999999999
Ikiru,1952,8.3,0.8128100000000001
