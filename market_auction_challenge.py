import sys
import json


def get_valid_ids(market_auction_data):
    return [x for x in market_auction_data.keys()]


def get_valid_years(id, market_auction_data):
    if 'schedule' in market_auction_data[id]:
        if 'years' in market_auction_data[id]['schedule']:
            yr_list = [x for x in market_auction_data[id][
                'schedule']['years'].keys()]
        else:
            yr_list = []
    else:
        yr_list = []
    return yr_list


def pretty_print(cost):
    return "$ {:,.2f}".format(cost)


def calc_rates(id, year, market_auction_data, format_dollar=None):
    # guard clause
    marketValue = 0.00
    auctionValue = 0.00
    blank_object = {"classification": None, "marketValue": marketValue,
                    "auctionValue": auctionValue}

    if id not in market_auction_data:
        print(f"ID: {id} not found in source data feed!!")
        return blank_object

    classifier = market_auction_data[id].get("classification", {})

    try:
        sched_year_vals = market_auction_data[id]['schedule']['years'][year]
        marketRatio = sched_year_vals['marketRatio']
        auctionRatio = sched_year_vals['auctionRatio']
    except KeyError:
        marketRatio = market_auction_data[id][
            'schedule']['defaultMarketRatio']
        auctionRatio = market_auction_data[id][
            'schedule']['defaultAuctionRatio']

    sale_detail = market_auction_data[id].get('saleDetails', {})
    if sale_detail:
        marketValue = sale_detail.get('cost', 0.00) * marketRatio
        auctionValue = sale_detail.get('cost', 0.00) * auctionRatio

    if format_dollar:
        (marketValue, auctionValue) = (pretty_print(marketValue),
                                       pretty_print(auctionValue))

    update_details = {"classification": classifier, "marketValue": marketValue,
                      "auctionValue": auctionValue, 'id': id,
                      'schedule_year': year}
    return {**blank_object, **update_details}


def print_object(obj):
    if obj['classification']:
        print("\n\n" + "-" * 50)
        print(f"Identifier: {obj['id']}")
        print(f"Category: {obj['classification']['category']}")
        print(f"Sub-cat: {obj['classification']['subcategory']}")
        print(f"Make: {obj['classification']['make']}\t\t" +
              f"Model: {obj['classification']['model']}\n")
        print(f"Schedule year: {obj['schedule_year']}")
        print(f"Market Value: {obj['marketValue']}\n" +
              f"Auction Value: {obj['auctionValue']}")
        print("-"*50)


if __name__ == "__main__":
    in_file = "api-response.json"

    file_handle = open(in_file)
    market_auction_source = json.load(file_handle)

    if sys.argv == 1:
        valid_ids = get_valid_ids(market_auction_source)

        id = input(f"Enter a valid id {valid_ids}: ")
        if id not in valid_ids:
            raise ValueError("Input not in valid range!!")

        valid_yrs = get_valid_years(id, market_auction_source)
        year = input(f"Enter the year for calculation {valid_yrs}: ")
        if year not in valid_yrs:
            raise ValueError("Year is not in valid range " +
                             f"for specified id {id}!!")
    else:
        input_val = sys.argv[1]
        (id, year) = input_val.split(',')

    obj_dict = calc_rates(id, year, market_auction_source,
                          format_dollar=True)
    print_object(obj_dict)
# end main