import requests
import json
import custom_func as cf
from passwords import api_key


headers = {'Authorization': 'Bearer %s' % api_key}
location = 'Toronto'

def restaurants(location, offset):
    """
    Create a list of restaurants
    """
    url='https://api.yelp.com/v3/businesses/search'
    params = {'location' : location, 'limit' : 50, 'offset' : offset}
    req = requests.get(url, params=params, headers=headers)
    if req.status_code == 200:
        j = json.loads(req.text)
        list_business = j['businesses']
        total = j['total']
        latitude = j['region']['center']['latitude']
        longitude = j['region']['center']['longitude']
    return {'list' : list_business, 
            'total' : total, 
            'latitude' : latitude, 
            'longitude' : longitude}

main = restaurants(location=location, offset=0)
businesses = main['list']

offset = 50
while offset <= 950:
    rest = restaurants(location=location, offset=offset)
    if rest['list']:
        businesses += rest['list']
    offset = offset + 50
    
cf.save_obj(businesses, 'businesses_api', '..\\references\\')
