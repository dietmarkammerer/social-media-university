# social-media-university
This SPARQL Query for wikidata written in Python selects all social media accounts from universities (`?uni wdt:P31/wdt:P279* wd:Q875538`) in Germany (`?uni wdt:P17 wd:Q183.`) as documented in Wikidata
Output is JSON. The output can be further analyzed by pipign it to [jq](https://jqlang.github.io/jq/)

## Usage
`$ python3 wikidata-social-media-university.py | jq .`

## Requirements
- [sparqlwrapper](https://rdflib.github.io/sparqlwrapper/)
- json
