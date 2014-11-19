import sys
import xbmcgui
import xbmcplugin

from bs4 import BeautifulSoup
import urllib

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'audio')

def addDirectory(url, dirName, plimage):
#add a new directory
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=1"
    liz = xbmcgui.ListItem(unicode(dirName),
                           iconImage="DefaultFolder.png",
                           thumbnailImage=plimage)
    liz.setInfo(type="Audio", infoLabels={"Title":dirName})
    ok = xbmcplugin.addDirectoryItem(addon_handle,
                                 url=u,
                                 listitem=liz,
                                 isFolder=True)
    return ok


def listPods(url):
    r = urllib.urlopen(url)
    html = r.read()
    soup = BeautifulSoup(html)
    titles = []
    audiofiles = []

# Extracts the URLs and titles for the podcasts
    for link in soup.find_all('a'):
        li = None
        href = link.get('href')
        if href.find('http') != -1:
           if href.find('mp3') != -1:
               audiofiles.append(href)  # podcasts
        else:
            if len(link.contents) > 1:
                titles.append(link.contents[0].strip())

# Matches the titles and the URLs for each list entry
    for i in range(len(audiofiles)):
        li = xbmcgui.ListItem(titles[i], iconImage='icon.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle,
                                    url=audiofiles[i], listitem=li)
def get_params():
    param = []
    paramstring = sys.argv[2]

    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params)-1] == '/'):
            params = params[0: len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param

params = get_params()
fullUrl = None
name = None
mode = None

try:
    fullUrl = urllib.unquote_plus(params['url'])
except:
    pass

try:
    name = urllib.unquote_plus(params['name'])
except:
    pass

try:
    mode = int(params['mode'])
except:
    pass

if mode == None or fullUrl == None or len(fullUrl)<1:
# Sets the live feed on top of the list
    liveurl = 'http://airtime.heartbeats.dk:8000/stream'
    li = xbmcgui.ListItem('Heartbeats [LIVE]', iconImage='icon.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle,
                                url=liveurl, listitem=li)
    baseUrl = 'http://heartbeats.dk/'
    extUrl = ['en/', 'da/', 'sv/', 'fr/']
    dirNames = ['English', 'Dansk', 'Svenska', 'Francais']
    plImageUrl = "wp-content/uploads/2014/01/logo-playlist.png"
    for i in range(len(dirNames)):
        addDirectory(baseUrl+extUrl[i], dirNames[i], baseUrl+plImageUrl)
elif mode == 1:
    print(""+fullUrl)
    listPods(fullUrl)


xbmcplugin.endOfDirectory(addon_handle)
