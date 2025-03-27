#!/bin/bash

# URL à scraper
URL="https://fr.advfn.com/bourses/SPI/SP500/cours"

# Boucle infinie
while true
do
  # Télécharger la page HTML
  curl -s "$URL" -o sp500_cours.html

  # Extraire le cours (ex: 5 667,56)
  price=$(sed -n '/<div>Dernier<\/div>/,/<\/div>/p' sp500_cours.html | grep -oP '\d{1,3}(?: \d{3})*(?:,\d{2})?')

  # Sauvegarder avec timestamp
  echo "$(date '+%Y-%m-%d %H:%M:%S'), $price" >> sp500_prices.csv

  # Attendre 5 min
  sleep 300
done
