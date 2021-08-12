from market_auction_challenge import get_valid_ids, get_valid_years, calc_rates
import json


def test_market_data_loaded():
    market_auction_data = json.load(open('api-response.json'))
    assert '67352' in market_auction_data
    assert 'schedule' in market_auction_data['87390']
    assert market_auction_data['67352']['schedule']['years']['2009'] == \
           {"marketRatio": 0.330725, "auctionRatio": 0.192716}
    assert market_auction_data['87390']['classification']['model'] == "340AJ"


def test_valid_ids():
    market_auction_data = json.load(open('api-response.json'))
    valid_ids = get_valid_ids(market_auction_data)
    assert len(valid_ids) == len(market_auction_data)
    assert valid_ids[1] == '87390'


def test_valid_years():
    market_auction_data = json.load(open('api-response.json'))
    valid_years = get_valid_years('87390', market_auction_data)
    len_years = len(market_auction_data['87390']['schedule']['years'])
    assert len(valid_years) == len_years
    assert '2020' in market_auction_data['87390']['schedule']['years']
    assert '2021' not in valid_years


def test_calc_rates_with_invalid_id():
    # when id is not present in the data set, return None for rate calculation
    market_auction_data = json.load(open('api-response.json'))
    assert calc_rates('87392', '2020', market_auction_data) == \
           {'classification': None, 'marketValue': 0.00,
            'auctionValue': 0.00}


def test_calc_rate_with_year_less_than_floor():
    # when invalid year, use default market and auction ratios
    market_auction_data = json.load(open('api-response.json'))
    classifier = market_auction_data['67352']['classification']
    assert calc_rates('67352', '2014', market_auction_data) == \
           {'classification': classifier, 'marketValue': 305709.36096523685,
            'auctionValue': 151095.1475857824, 'schedule_year': '2014', 'id': '67352'}


def test_calc_rate_with_year_greater_than_ceiling():
    market_auction_data = json.load(open('api-response.json'))
    classifier = market_auction_data['87390']['classification']
    assert calc_rates('87390', '2014', market_auction_data,
                      format_dollar=True) == \
           {'classification': classifier, 'marketValue': '$ 26,514.86',
            'auctionValue': '$ 18,048.67', 'schedule_year': '2014',
            'id': '87390'}


def test_calc_rate_for_2018():
    market_auction_data = json.load(open('api-response.json'))
    classifier = market_auction_data['87390']['classification']
    assert calc_rates('87390', '2018', market_auction_data) != \
           {'classification': {}, 'marketValue': 47974.150565,
            'auctionValue': 33515.924639, 'schedule_year': '2018'}

    classifier = market_auction_data['67352']['classification']
    assert calc_rates('67352', '2009', market_auction_data,
                      format_dollar=True) == \
           {'classification': classifier, 'marketValue': '$ 225,307.07',
            'auctionValue': '$ 131,288.16', 'schedule_year': '2009',
            'id': '67352'}


def test_calc_rate_for_actual_tests():
    market_auction_data = json.load(open('api-response.json'))
    classifier = market_auction_data['67352']['classification']
    assert calc_rates('67352', '2007', market_auction_data,
                      format_dollar=True) == \
           {'classification': classifier, 'marketValue': '$ 216,384.71',
            'auctionValue': '$ 126,089.53', 'schedule_year': '2007',
            'id': '67352'}

    assert calc_rates('87964', '2011', market_auction_data) == \
           {'classification': None, 'marketValue': 0.00,
            'auctionValue': 0.00}
