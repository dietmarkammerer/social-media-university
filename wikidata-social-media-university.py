# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?uni 
      (IRI(MIN(STR(?websites))) as ?website) # only one result per university is needed
      (IRI(MIN(STR(?mastodonUrls))) as ?mastodonUrl)
      (IRI(MIN(STR(?xUris))) as ?xUri)
      (IRI(MIN(STR(?facebookUrls))) as ?facebookUrl)
      (IRI(MIN(STR(?linkedInUrls))) as ?linkedInUrl)
      (IRI(MIN(STR(?instagramUrls))) as ?instagramUrl)
      (IRI(MIN(STR(?blueskyUrls))) as ?blueskyUrl)
      (IRI(MIN(STR(?tiktokUrls))) as ?tiktokUrl)
      (IRI(MIN(STR(?YouTubeUrls))) as ?YouTubeUrl)

WHERE
{
  ?uni wdt:P31/wdt:P279* wd:Q875538;
       wdt:P17 wd:Q183;
       wdt:P856 ?websites.
  
   MINUS { ?uni wdt:P361 ?some. }
  
  # mastodon
  OPTIONAL { ?uni wdt:P4033 ?mastodon. }
    BIND(REPLACE(STR(?mastodon), '.*@','') as ?mastodonDomain)
    BIND(REPLACE(STR(?mastodon), '@.*','') as ?mastodonName)
    BIND(IRI(CONCAT('https://', ?mastodonDomain, '/@', ?mastodonName)) as ?mastodonUrls )
  
  # X / twitter
  OPTIONAL { ?uni wdt:P2002 ?x. }
    BIND(IRI(CONCAT('https://x.com/',?x)) as ?xUris )
  
  # facebook
  OPTIONAL { ?uni wdt:P2013 ?facebook. }
    BIND(IRI(CONCAT('https://www.facebook.com/', ?facebook)) as ?facebookUrls )
  
  # LinkedIn
  OPTIONAL { ?uni wdt:P4264 ?linkedIn. }
    BIND(IRI(CONCAT('https://www.linkedin.com/company/', ?linkedIn)) as ?linkedInUrls )
  
  # Instagram
  OPTIONAL { ?uni wdt:P2003 ?instagram.}
    BIND(IRI(CONCAT('https://www.instagram.com/', ?instagram)) as ?instagramUrls )
  
  # BlueSky
  OPTIONAL { ?uni wdt:P12361 ?bluesky. }
    BIND(IRI(CONCAT('https://bsky.app/profile/', ?bluesky)) as ?blueskyUrls )
  
  # TikTok
  OPTIONAL { ?uni wdt:P7085 ?tiktok. }
    BIND(IRI(CONCAT('https://www.tiktok.com/@', ?tiktok)) as ?tiktokUrls )
  
  # YouTube
  OPTIONAL { ?uni wdt:P2397 ?YouTube.}
   BIND(IRI(CONCAT("https://www.youtube.com/channel/", STR( ?YouTube ))) AS ?YouTubeUrls ) .
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
}

GROUP BY ?uni"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result)
