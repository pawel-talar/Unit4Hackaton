import logging
import time
import json
from os.path import expanduser
import unit4_hackaton.history_gatherer as hg
import unit4_hackaton.assistant_client as assistant_client


profile_name = 'mxhml4y1.default'
history_path = expanduser("~") + '/.mozilla/firefox/' + profile_name + \
               '/places.sqlite'


def get_assistant_address(config_path):
    with open(config_path, 'r') as f:
        try:
            config = json.loads(f.read())
            return config["assistant"]
        except json.JSONDecodeError as e:
            logging.error("{} is not valid JSON file: {}".format(
                config_path, str(e)
            ))
        except KeyError as e:
            logging.error("Cannot find assistant configuration in config: {}"
                          .format(str(e)))


def main():
    logging.basicConfig(level=logging.DEBUG)
    history_gatherer = hg.HistoryGatherer(history_path)
    config_path = 'config.json'
    assistant_cli = assistant_client.AssistantClient(
        get_assistant_address(config_path))
    delay = 2
    while True:
        time.sleep(delay)
        urls = [url for url in history_gatherer.get_urls() if
                'wikipedia' in url]
        for url in urls:
            try:
                assistant_cli.submit(url)
                history_gatherer.cache(url)
            except assistant_client.AssistantUnreachable as e:
                logging.error(str(e))


if __name__ == '__main__':
    main()
