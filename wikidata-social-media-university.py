# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
import json
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """#Social Media-Auftritte von deutschen Universitäten
SELECT DISTINCT ?uni ?uniLabel ?mastodonUrl ?xUri ?facebookUrl ?linkedInUrl ?instagramUrl ?blueskyUrl ?tiktokUrl ?YouTubeUrl
WHERE
{
  ?uni wdt:P31/wdt:P279* wd:Q875538;
       wdt:P17 wd:Q183.
  
  # mastodon
  OPTIONAL { ?uni wdt:P4033 ?mastodon. }
    BIND(REPLACE(STR(?mastodon), '.*@','') as ?mastodonDomain)
    BIND(REPLACE(STR(?mastodon), '@.*','') as ?mastodonName)
    BIND(IRI(CONCAT('https://', ?mastodonDomain, '/@', ?mastodonName)) as ?mastodonUrl)
  
  # X / twitter
  OPTIONAL { ?uni wdt:P2002 ?x. }
    BIND(IRI(CONCAT('https://x.com/',?x)) as ?xUri)
  
  # facebook https://www.facebook.com/universitaetbremen
  OPTIONAL { ?uni wdt:P2013 ?facebook. }
    BIND(IRI(CONCAT('https://www.facebook.com/', ?facebook)) as ?facebookUrl)
  
  # LinkedIn
  OPTIONAL { ?uni wdt:P4264 ?linkedIn. }
    BIND(IRI(CONCAT('https://www.linkedin.com/company/', ?linkedIn)) as ?linkedInUrl)
  
  # Instagram
  OPTIONAL { ?uni wdt:P2003 ?instagram.}
    BIND(IRI(CONCAT('https://www.instagram.com/', ?instagram)) as ?instagramUrl)
  
  # BlueSky
  OPTIONAL { ?uni wdt:P12361 ?bluesky. }
    BIND(IRI(CONCAT('https://bsky.app/profile/', ?bluesky)) as ?blueskyUrl)
  
  # TikTok
  OPTIONAL { ?uni wdt:P7085 ?tiktok. }
    BIND(IRI(CONCAT('https://www.tiktok.com/@', ?tiktok)) as ?tiktokUrl)
  
  # YouTube
  OPTIONAL { ?uni wdt:P2397 ?YouTube.}
   BIND(IRI(CONCAT("https://www.youtube.com/channel/", STR( ?YouTube ))) AS ?YouTubeUrl ) .
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
}
"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

results = get_results(endpoint_url, query)

print(json.dumps(results))
