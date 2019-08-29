#python3.6                                                         


def parse_webpage_table(table):
    """Accepts a selenium WebElement table of zip codes information from
    http://localistica.com/usa/zipcodes/most-populated-zipcodes/ and
    returns a list of only zip codes.
    :param table: selenium.webdriver.remote.webelement.WebElement class

    :return: list of zip codes as integers
    """
    parsed_table = table.text.split('\n')

    # first element is header
    zipcodes = [i.split()[0] for i in parsed_table[1:]]
    cities = []
    for row in parsed_table[1:]:
        split_row = row.split()

    # abbreviation is uppercase only
    abbrev = [i for i, v in enumerate(split_row) if v.isupper()]
    cities.append(''.join(split_row[1:abbrev[0]]))

    return list(zip(cities, zipcodes))
