#!/bin/bash

if [[ "$#" -ne 2 ]]; then
    echo "Usage: ./index.sh <path_to_wiki_dump> <path_to_index_folder>"
    exit 2
fi

python3 wiki_indexer.py $1 $2
