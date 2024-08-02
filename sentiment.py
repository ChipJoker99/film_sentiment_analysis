import os
import logging
import nltk
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import time
from datetime import datetime

# Crea le cartelle logs e data se non esistono
if not os.path.exists('logs'):
    os.makedirs('logs')

if not os.path.exists('data'):
    os.makedirs('data')

# Configura il logging
log_date = datetime.now().strftime("%Y%m%d")
log_number = 1
log_filename = f'logs/scraping_{log_date}_{log_number:07d}.log'
while os.path.exists(log_filename):
    log_number += 1
    log_filename = f'logs/scraping_{log_date}_{log_number:07d}.log'

logging.basicConfig(filename=log_filename,
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configura il driver di Chrome
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Chiave API di OMDb
api_key = "feac89b1"

# Estrapola i primi 100 film da Flickchart
url_flickchart = "https://www.flickchart.com/Charts.aspx?perpage=100"
driver.get(url_flickchart)
logging.info(f"ACCESSED URL: {url_flickchart}")

film_titles = driver.find_elements(By.CSS_SELECTOR, "h2.movieTitle")
for title_element in film_titles:
    title = title_element.text
    if title:
        logging.info(f"FOUND FILM TITLE: {title}")

# Effettua lo scraping dei titoli dei film da Flickchart
soup = BeautifulSoup(driver.page_source, "html.parser")
film_titles = [title.text for title in soup.select("h2.movieTitle a span[itemprop='name']")]
logging.info(f"SCRAPED FILM TITLES: {film_titles}")

# Inizializza un DataFrame vuoto
df = pd.DataFrame(columns=["Title", "Year", "Rating", "Sentiment"])

# Scarica il file vader_lexicon
nltk.download('vader_lexicon')

# Effettua richieste all'API di OMDb per ciascun film
start_time = time.time()
total_films = len(film_titles)

for i, title in enumerate(film_titles):
    url_omdb = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response_omdb = requests.get(url_omdb).json()
    if "Title" in response_omdb and "Year" in response_omdb and "imdbRating" in response_omdb:
        rating = response_omdb["imdbRating"]
        if rating != "N/A":
            rating = float(rating)
        else:
            rating = None
        reviews = []
        review_url = f"https://www.imdb.com/title/{response_omdb['imdbID']}/reviews"
        driver.get(review_url)
        review_soup = BeautifulSoup(driver.page_source, "html.parser")
        review_elements = review_soup.select("div.text.show-more__control")
        for review_element in review_elements[:10]:  # Limita alle prime 10 recensioni
            reviews.append(review_element.text)
        
        # Analisi del sentiment
        sia = SentimentIntensityAnalyzer()
        sentiments = [sia.polarity_scores(review)['compound'] for review in reviews]
        average_sentiment = sum(sentiments) / len(sentiments) if sentiments else None
        
        df = pd.concat([df, pd.DataFrame([{"Title": response_omdb["Title"], "Year": response_omdb["Year"], "Rating": rating, "Sentiment": average_sentiment}])], ignore_index=True)
        logging.info(f"PROCESSED FILM: {response_omdb['Title']}")

    # Stampa il progresso e il tempo rimanente stimato
    elapsed_time = time.time() - start_time
    avg_time_per_film = elapsed_time / (i + 1)
    remaining_time = avg_time_per_film * (total_films - (i + 1))
    print(f"Processed {i + 1}/{total_films} films. Estimated time remaining: {remaining_time:.2f} seconds.")

# Rimuovi le righe con valutazioni mancanti
df = df.dropna(subset=["Rating"])

# Calcola la valutazione media
average_rating = df["Rating"].mean()

# Visualizza i risultati
print(df)
print(f"Valutazione media dei film: {average_rating:.2f}")

# Crea un grafico a barre
plt.bar(df["Title"], df["Rating"])
plt.xlabel("Film")
plt.ylabel("Valutazione")
plt.title("Valutazione dei Film")
plt.xticks(rotation=45)
plt.show()

# Salva i dati in un file CSV con nome unico
csv_date = datetime.now().strftime("%Y%m%d")
csv_number = 1
csv_filename = f'data/film_data_{csv_date}_{csv_number:07d}.csv'
while os.path.exists(csv_filename):
    csv_number += 1
    csv_filename = f'data/film_data_{csv_date}_{csv_number:07d}.csv'

df.to_csv(csv_filename, index=False)
logging.info(f"DATA SAVED TO {csv_filename}")

driver.quit()
