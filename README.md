# social-media-university
This SPARQL Query for wikidata written in Python selects all social media accounts from German unievrsites as documented in Wikidata
Output is JSON. The output can be further analyzed by pipign it to [jq](https://jqlang.github.io/jq/)

## Usage
`$ python3 wikidata-social-media-university.py | jq .`

## Requirements
- [sparqlwrapper](https://rdflib.github.io/sparqlwrapper/)
- json
