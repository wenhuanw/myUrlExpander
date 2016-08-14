import requests


def get_url(url, timestamp):
    api = 'http://archive.org/wayback/available' 
    params = {'url': url, 'timestamp': timestamp}
    r = requests.get(api, params=params)
    urls = r.json()
    if (urls['archived_snapshots'] == {}):
        return None
    waybackurl = urls['archived_snapshots']['closest']['url']
   # timestamp = urls['archived_snapshots']['closest']['timestamp']
    return waybackurl
