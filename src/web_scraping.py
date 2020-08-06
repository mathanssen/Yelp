import custom_func as cf
import requests
import pandas as pd

path_references = '..\\references\\'


list_businesses = cf.load_obj('businesses', path_references)


url = 'https://www.yelp.com/biz/banh-mi-boys-toronto?adjust_creative=K4PW6zBh8_pfAdRBLscq4Q&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=K4PW6zBh8_pfAdRBLscq4Q'
html = requests.get(url).content
html_list = pd.read_html(html)

