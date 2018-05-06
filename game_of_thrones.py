import urllib
import re

from BeautifulSoup import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/Game_of_Thrones'
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

print soup.html.head.title.string
print "Gledalci na posamezno sezono:"

season_table = soup.find('table', attrs={'class': 'wikitable plainrowheaders'})
seasons_links = season_table.findAll('a', attrs={'href': re.compile('\/wiki\/Game_of_Thrones_\(season_?[0-9]+\)')})

total_views = 0
for season_link in seasons_links:
    season_url = 'https://en.wikipedia.org' + season_link['href']
    season_html = urllib.urlopen(season_url).read()
    season_content = BeautifulSoup(season_html)

    episodes_table = season_content.find('table', attrs={'class': 'wikitable plainrowheaders wikiepisodetable'})
    episode_rows = episodes_table.findAll('tr', attrs={'class': 'vevent'})

    views = 0
    for episode_row in episode_rows:
        episode_views = episode_row.findAll('td')[-1].text
        if episode_views == "TBD":
            episode_views = True
        else:
            views += float(re.sub(r'\[?[0-9]+\]', '', episode_views))
            total_views += float(re.sub(r'\[?[0-9]+\]', '', episode_views))
    print season_link.text + ": " + str(views) + " miljonov"
print "Skupno stevilo vseh gledalcev je bilo " + str(total_views) + " miljonov"
