# social-media-university
This SPARQL Query for wikidata written in Python selects all social media accounts from universities (`?uni wdt:P31/wdt:P279* wd:Q875538`) in Germany (`?uni wdt:P17 wd:Q183.`) as documented in Wikidata.  
Output is JSON. The output can be further analyzed by piping it to [jq](https://jqlang.github.io/jq/)

## Usage
`$ python3 wikidata-social-media-university.py | jq .`

## Requirements
- [sparqlwrapper](https://rdflib.github.io/sparqlwrapper/)
- json

## Query
``` SPARQL
SELECT ?uni ?uniLabel
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

GROUP BY ?uni ?uniLabel
```
