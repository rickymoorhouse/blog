
#Get hugo and pagefind
export BUNNYCDN_APIKEY=`security find-generic-password -s bunny-apikey -w`
export BUNNYCDN_PASSWORD=`security find-generic-password -s bunny-storage -w`
export BUNNYCDN_PULLZONE="3422848"

which hugo
if [$? -ne 0]; then
    echo "Hugo not found, downloading..."
    brew install hugo
else
    echo "Hugo found, skipping download."
fi
which pagefind
if [ $? -ne 0 ]; then
    echo "Pagefind not found, downloading..."
    brew install pagefind
fi

hugo
pagefind
python3 scripts/generate_flights.py

# Deploy to Bunny
duck -y \
    --username rm-uk-standard \
    --password ${BUNNYCDN_PASSWORD} \
    --existing overwrite \
    --upload ftps://uk.storage.bunnycdn.com/ ./public/

curl -X POST \
    -H "AccessKey: ${BUNNYCDN_APIKEY}" \
    https://api.bunny.net/pullzone/${BUNNYCDN_PULLZONE}/purgeCache
