
#Get hugo and pagefind
export BUNNYCDN_APIKEY=`security find-generic-password -s bunny-apikey -w`
export BUNNYCDN_PASSWORD=`security find-generic-password -s bunny-storage -w`
export BUNNYCDN_PULLZONE="3422848"

export PAGEFIND_VERSION="1.5.2"
export ARCHITECTURE=$(uname -m)

which hugo
if [$? -ne 0]; then
    echo "Hugo not found, downloading..."
    brew install hugo
else
    echo "Hugo found, skipping download."
fi
which pagefinde
if [ $? -ne 0 ]; then
    echo "Pagefind not found, downloading..."
    PAGEFIND_DOWNLOAD=pagefind-v${PAGEFIND_VERSION}-aarch64-apple-darwin.tar.gz
    if [ "${ARCHITECTURE}" = "x86_64" ]; then
        PAGEFIND_DOWNLOAD=pagefind-v${PAGEFIND_VERSION}-x86_64-unknown-linux-musl.tar.gz
    fi
    echo "Downloading Pagefind version ${PAGEFIND_VERSION} for architecture ${ARCHITECTURE}..."
    curl -o ${PAGEFIND_DOWNLOAD} https://github.com/CloudCannon/pagefind/releases/download/v${PAGEFIND_VERSION}/${PAGEFIND_DOWNLOAD}
    tar xvzf ${PAGEFIND_DOWNLOAD} 

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
