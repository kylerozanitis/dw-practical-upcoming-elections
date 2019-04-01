""" This file contains the function for querying data from the Turbovote API
and storing in a dictionary """

# Library Imports
import requests
import json


def generate_ocdids(request_form):
    """ Provided the request form, generate ocd-id """
    city_name = str(request_form['city']).lower().replace(' ', '_')
    state_abbreviation = str(request_form['state']).lower()

    city_ocdid = 'ocd-division/country:us/state:{0}/place:{1}'.format(
        state_abbreviation, city_name)
    state_ocdid = 'ocd-division/country:us/state:{}'.format(state_abbreviation)

    return ','.join([city_ocdid, state_ocdid])


def query_google_civic(request_form):
    """ Provided the request form, gather civic information in area """
    api_key = ''

    street_address = str(request_form['street'])
    city_name = str(request_form['city'])
    state_abbreviation = str(request_form['state'])
    zip_code = str(request_form['zip'])

    query = ' '.join([street_address, city_name, state_abbreviation, zip_code])

    url = 'https://www.googleapis.com/civicinfo/v2/representatives'
    payload = {'address': query, 'key': api_key}

    response = requests.get(url, params=payload)
    json_response = response.json()
    ocdids = json_response['divisions'].keys()
    return ocdids


def query_turbovote(ocdids):
    """ Query the Turbovote API for local elections; return json if election data
    available else empty list """

    joined_ocdids = ','.join(ocdids)

    query = 'https://api.turbovote.org/elections/upcoming'
    payload = {'district-divisions': joined_ocdids}
    headers = {'Accept': 'application/json'}

    response = requests.get(query, params=payload, headers=headers)

    # print(payload)
    # print(response.text)
    if response.json() != {}:
        json_response = response.json()
        return json_response
    else:
        return []


def temp_store_data(json_response):
    """ Temporarily store Turbovote API response data in dictionary """

    election_results_dict = {}

    election_results_dict['description'] = json_response[0]['description']
    election_results_dict['website'] = json_response[0]['website']
    election_results_dict['date'] = json_response[0]['date']
    election_results_dict['polling_place_url'] = json_response[0]['polling-place-url']
    election_results_dict['population'] = json_response[0]['population']
    election_results_dict['election_authority_level'] = json_response[0]['district-divisions'][0]['election-authority-level']
    election_results_dict['early_voting'] = True if json_response[0][
        'district-divisions'][0]['voting-methods'][0]['type'] == 'early-voting' else False
    election_results_dict['in_person'] = True if json_response[0][
        'district-divisions'][0]['voting-methods'][1]['type'] == 'in-person' else False
    election_results_dict['by_mail'] = True if json_response[0][
        'district-divisions'][0]['voting-methods'][2]['type'] == 'by-mail' else False

    return election_results_dict
