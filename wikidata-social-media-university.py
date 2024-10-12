#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pywikibot will automatically set the user-agent to include your username.
# To customise the user-agent see
# https://www.mediawiki.org/wiki/Manual:Pywikibot/User-agent

import pywikibot
from pywikibot.pagegenerators import WikidataSPARQLPageGenerator
from pywikibot.bot import SingleSiteBot


class WikidataQueryBot(SingleSiteBot):
    """
    Basic bot to show wikidata queries.

    See https://www.mediawiki.org/wiki/Special:MyLanguage/Manual:Pywikibot
    for more information.
    """

    def __init__(self, generator, **kwargs):
        """
        Initializer.

        @param generator: the page generator that determines on which pages
            to print
        @type generator: generator
        """
        super(WikidataQueryBot, self).__init__(**kwargs)
        self.generator = generator

    def treat(self, page):
        print(page)


if __name__ == '__main__':
    query = """SELECT DISTINCT ?uni ?uniLabel ?website ?mastodonUrl ?xUri ?facebookUrl ?linkedInUrl ?instagramUrl ?blueskyUrl ?tiktokUrl ?YouTubeUrl
WHERE
{
  ?uni wdt:P31/wdt:P279* wd:Q875538;
       wdt:P17 wd:Q183;
       wdt:P856 ?website.
  
   MINUS { ?uni wdt:P361 ?some. }
  
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
    site = pywikibot.Site()
    gen = WikidataSPARQLPageGenerator(query, site=site.data_repository(),
                                      endpoint='https://query.wikidata.org/sparql')
    bot = WikidataQueryBot(gen, site=site)
    bot.run()
