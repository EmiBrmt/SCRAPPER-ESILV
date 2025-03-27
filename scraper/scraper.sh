#!/bin/bash
URL="https://fr.advfn.com/bourses/SPI/SP500/cours"
curl -s "$URL" -o sp500_cours.html
price=$(sed -n '/<div>Dernier<\/div>/,/<\/div>/p' sp500_cours.html | grep -oP '\d{1,3}(?: \d{3})*(?:,\d{2})?' | tail -1)
echo "$(date '+%Y-%m-%d %H:%M:%S'), $price" >> sp500_prices.csv

