import random

df_index_columns = [
    # "product_identifier",
    # "page_id",
    "product_title",
    "published_price",
    "discounted_price",
    "linked_images"]

# scrape uri for fetching the current euro exchange reference
scrape_website_uri = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"
__agent_header_list = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
]
## defined the Agent Header identifier for secure protocol
AGENT_HEADER = {'User-Agent': random.choice(__agent_header_list), 'X-Requested-With': 'XMLHttpRequest'}

DYNAMODB_PARTITION_KEY: str = "pk"
DYNAMODB_SORT_KEY: str = "sk"
table_name: str = "local_currency_exchange"
