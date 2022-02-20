import requests



cookies = {
    'visid_incap_2483049': 'bCT5kPvuTMCMpIzeT1EhF11kEmIAAAAAQUIPAAAAAADeCMPlMAp5E+IHJLKom4IG',
    'reese84': '3:wQuxBNSu+9/FF95uF9ol4w==:vWHR2HSv889OhE0sR6Ehs32OW7kNatU947bClBm5rUonren4hSCvCEtUZAEr7ExJ/8Rzo2cHLLSXA9V+YMfmyEREYwHOirZwGtz0LfTYUFwgpzSASxKBaEmDKEfxl6z0HdzGamWdEtYaSaqgokrvm5ZcsTUSJ6uC7pZ660hpKgjw7c9Rguqton9Cinv3TtCwZzeJiRVKSt2u9/2mci4kMyXHtQILPVHrqvdU1Ym98hldl/bPFW0Y9RUS9ZH6Y3Ib+GGRAvv7CYbnw21rL8Nq5nyoo6pF6uUKWAOwt9mA21AqnB28FAbNcHSsvUV0in5FrplZdhIXPpGF7sl468h/yLdP6mpmJOh7Pf/6t4RJDyHfCKeZ44oqjMTVIDfvJlQlGj2Gh7Mgzsui7GYULcH5rqodNPWqKEdgFwe+QZsdQbKqq9YM24XE8pCbPAhQ53oA:tr4lJvU9F2MMr1851rKcoQldL25fZSDe3Emf82E2fNI=',
    'incap_ses_1458_2483049': 'KhmQGGs1by7dOG4CfNs7FKF0EmIAAAAAIrfRHM9xI1lKVw33g68bIQ==',
    'nlbi_2483049_2147483392': 'sHuATBbWYE9YEDUnYsb6kQAAAABTzMkYKl7N1HNt8L5BruaH',
    'JSESSIONID': '658582A0F52179E041AFBD4A0C069B42.f5sk',
    'recentlyBrowsedProducts': '191430',
    'uk-anonymous-consents': '%5B%7B%22templateCode%22%3A%22Analytics%22%2C%22templateVersion%22%3A0%2C%22consentState%22%3A%22GIVEN%22%7D%2C%7B%22templateCode%22%3A%22Essential%22%2C%22templateVersion%22%3A0%2C%22consentState%22%3A%22GIVEN%22%7D%2C%7B%22templateCode%22%3A%22Functional%22%2C%22templateVersion%22%3A0%2C%22consentState%22%3A%22GIVEN%22%7D%2C%7B%22templateCode%22%3A%22Targeting%22%2C%22templateVersion%22%3A0%2C%22consentState%22%3A%22GIVEN%22%7D%5D',
    'uid': 'uk',
    'GCLB': 'COj_2qGY2_jVoQE',
    'nlbi_2483049': 'IPkJanZb8F672bxAYsb6kQAAAACyyGyQzuUe+kApdW2dQZTI',
    'smyths_gtm_GTM': 'false',
    'smyths_gtm_GOOGLEOPTIMIZE': 'true',
    'smyths_gtm_CYBERSOURCE': 'false',
    'smyths_gtm_KLARNA': 'false',
    'smyths_gtm_HOTJAR': 'true',
    'smyths_gtm_RAKUTEN': 'false',
    'smyths_gtm_GA': 'true',
    'smyths_gtm_BAZAARVOICE': 'false',
    'smyths_gtm_FLIXMEDIA': 'false',
    'smyths_gtm_WEBCOLLAGE': 'false',
    'smyths_gtm_FRESHCHAT': 'false',
    'smyths_gtm_YOUTUBE': 'false',
    'smyths_gtm_SYNDIGO': 'true',
    'smyths_gtm_SITEVISIT': 'false',
    'smyths_gtm_LOCATION': 'false',
    'smyths_gtm_FACEBOOK': 'true',
    'smyths_gtm_GOOGLEADWORDS': 'true',
    'siteVisited': 'false',
    '_hjOptOut': 'false',
    'locationCookie': '_',
    '_gcl_au': '1.1.2112808728.1645376751',
    '_ga_FHGLQ54MHW': 'GS1.1.1645376751.1.0.1645376751.0',
    '_ga': 'GA1.1.352503110.1645376752',
    'flixgvid': 'flixb541ee1f000000.81646115',
    'inptime0_1764_en': '0',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.smythstoys.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.smythstoys.com/uk/en-gb/video-games-and-tablets/playstation-5/playstation-5-consoles/playstation-5-digital-edition-console/p/191430',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

data = {
  'cartPage': 'false',
  'entryNumber': '0',
  'latitude': '',
  'longitude': '',
  'searchThroughGeoPointFirst': 'false',
  'xaaLandingStores': 'false',
  'CSRFToken': 'd9339d75-f628-402b-809a-4a99441f3fc6'
}

response = requests.post('https://www.smythstoys.com/uk/en-gb/store-pickup/191430/pointOfServices', headers=headers, cookies=cookies, data=data)
print(response)
print(response.content)