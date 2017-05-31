import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

import pandas as pd

CREDENTIALS = {
    "url": "https://gateway.watsonplatform.net/discovery/api",
    "username": "06f33cca-7f50-4fec-b45a-8aed4d07355c",
    "password": "nsSQDvkCClRG"
}

country_list = [
    'Brazil',
    'China',
    'India',
    'Russia',
    'United States',
    'Georgia',
    'Scotland',
    'England',
    'France',
    'Germany',
    'Argentina',
    'Canada',
    "Turkey",
]

import sys, pprint
import os

sys.path.append(os.path.join(os.getcwd(), '..'))
import watson_developer_cloud

DISCOVERY_USERNAME = CREDENTIALS["username"]
DISCOVERY_PASSWORD = CREDENTIALS["password"]
# ENVIRONMENT_NAME='CHANGE_ME' # this is the 'name' field of your environment
# CONFIGURATION_NAME='CHANGE_ME' # this is the 'name' field of your configuration
pp = pprint.PrettyPrinter(indent=4)


def get_news_environment_id(discovery_variable):
    environments = discovery_variable.get_environments()
    news_environments = [x for x in environments['environments'] if
                         x['name'] == 'Watson News Environment']
    id = news_environments[0]['environment_id']
    return id


def get_country_sentiment(discovery, news_environment_id, collection_id, query, country):
    query_options = {'query': '{}'.format(query), "count": 0, "offset": 50,
                     "filter": "entities:(text::{},type::Country)".format(country),
                     "aggregation": "filter(entities.text:bitcoin).term(docSentiment.type)"
                     }
    query_results = discovery.query(news_environment_id,
                                    collection_id,
                                    query_options)
    return query_results


def main():
    discovery = watson_developer_cloud.DiscoveryV1(
        '2017-05-30',
        username=DISCOVERY_USERNAME,
        password=DISCOVERY_PASSWORD)

    news_environment_id = get_news_environment_id(discovery)
    collections = discovery.list_collections(news_environment_id)
    news_collections = [x for x in collections['collections']]

    countries_results = []
    labels = ["country", "positive", "negative", "neutral", "without"]

    for country in country_list:
        res = get_country_sentiment(discovery, news_environment_id, news_collections[0]['collection_id'],
                                    "bitcoin", country)
        aggregation = res["aggregations"][0]
        if aggregation["matching_results"] > 0:
            all_aggregations = aggregation["aggregations"][0]["results"]
            row = [country, 0, 0, 0, 0]
            for aggregation in all_aggregations:
                if aggregation["key"] == "positive":
                    row[1] = aggregation["matching_results"]
                if aggregation["key"] == "negative":
                    row[2] = aggregation["matching_results"]
                if aggregation["key"] == "neutral":
                    row[3] = aggregation["matching_results"]
                if aggregation["key"] == "":
                    row[4] = aggregation["matching_results"]
            countries_results.append(tuple(row))
        else:
            countries_results.append((country, 0, 0, 0, 0))
    df = pd.DataFrame.from_records(countries_results, columns=labels)
    df.set_index(["country"], inplace=True)
    df.plot.bar()
    plt.show()
    # print(df)

    # query_options = {'query': 'bitcoin', "count": 0, "offset": 50,
    #                  "filter": "entities:(text::Ukraine,type::Country)",
    #                  "aggregation": "filter(entities.text:bitcoin).term(docSentiment.type)"
    #                  }
    # query_results = discovery.query(news_environment_id,
    #                                 news_collections[0]['collection_id'],
    #                                 query_options)
    # print(json.dumps(query_results, indent=2))


if __name__ == '__main__':
    main()
