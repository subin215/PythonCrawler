from HTMLParser import HTMLParser
import validators


class LinkParser(HTMLParser):

    links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for link in attrs:
                try:
                    if validators.url(link[1]):
                        self.links.append(link[1])
                except TypeError as e:
                    # TODO: switch this to logger.error
                    print("Encountered type error parsing HTML", e)
