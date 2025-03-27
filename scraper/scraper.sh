#!/bin/bash
URL="https://fr.advfn.com/bourses/SPI/SP500/cours"
while true
do
curl -s "$URL" -o sp500_cours.html
price=$(sed -n '/<div>Dernier<\/div>/,/<\/div>/p' sp500_cours.html | grep -oP '\d{1,3}(?: \d{3})*(?:,\d{2})?' | tail -1)
echo "$(date '+%Y-%m-%d %H:%M:%S'), $price" >> sp500_prices.csv
# Commit & push automatique
git add sp500_prices.csv
git commit -m "MAJ auto - $(date '+%Y-%m-%d %H:%M:%S')" > /dev/null 2>&1
git push origin main > /dev/null 2>&1
sleep 300
done
