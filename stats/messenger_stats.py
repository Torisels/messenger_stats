import re
import matplotlib.pyplot as plt
from collections import Counter


class MessengerStats:
    REGEX_XD = re.compile(r"[xX]([dD])+")
    MOST_COMMON = 10
    PARSERS = {"total_msg": ["Całkowita liczba wiadomości"],
               "received_reactions": ["Całkowita liczba otrzymanych reakcji"],
               "given_reactions": ["Całkowita liczba dawanych reakcji"],
               "xds": ["Całkowita liczba wiadomości z 'xD' lub podobnymi"],
               "total_photos":["Całkowita liczba wrzuconych zdjęć"],
               "total_characters": ["Całkowita liczba znaków"],
               "total_words": ["Całkowita liczba słów (rozdzielane spacjami wyrażenia)"]}

    def __init__(self, data):
        self.messages = data["messages"]
        self.participants = [person["name"] for person in data["participants"]]
        self.parsers = [self.count_messages, self.count_received_reactions, self.count_xds, self.count_photos, self.count_characters]
        self.parsed_data = {k: Counter() for k in self.PARSERS.keys()}
        self.reactions = Counter()

    def run(self):
        for message in self.messages:
            for parser in self.parsers:
                parser(message)
        self.generate_graphs()

    def generate_graphs(self):
        for name, data in self.parsed_data.items():
            keys, vals = self.prepare_data(data)
            self.draw_graph(self.PARSERS[name][0], keys, vals, save=f"graphs/{name}.png")

        keys, vals = self.prepare_data(self.reactions)
        self.draw_graph("Dystrybucja typów reakcji", keys, vals,save=f"graphs/reakcje.png" )

    def count_messages(self, message):
        self.parsed_data["total_msg"][message["sender_name"]] += 1

    def count_received_reactions(self, message):
        if "reactions" in message:
            self.parsed_data["received_reactions"][message["sender_name"]] += len(message["reactions"])
            for reaction in message["reactions"]:
                self.parsed_data["given_reactions"][reaction["actor"]] += 1
                self.reactions[reaction["reaction"]] += 1

    def count_xds(self, message):
        if "content" in message and self.REGEX_XD.search(message["content"]):
            self.parsed_data["xds"][message["sender_name"]] += 1

    def count_photos(self, message):
        if "photos" in message:
            self.parsed_data["total_photos"][message["sender_name"]] += len(message["photos"])

    def count_characters(self, message):
        if "content" in message:
            self.parsed_data["total_characters"][message["sender_name"]] += len(message["content"])
            self.parsed_data["total_words"][message["sender_name"]] += len(message["content"].split())


    @staticmethod
    def draw_graph(title, keys, values, x_label="", y_label="", save=""):
        fig, ax = plt.subplots()
        for i, v in enumerate(values):
            ax.text(v + 1, i - 0.25, v)
        plt.barh(keys, values)
        plt.title(title)
        plt.ylabel(y_label)
        plt.xlabel(x_label)

        if save is "":
            plt.show()
        else:
            # plt.show()
            plt.savefig(save, bbox_inches='tight')

    @classmethod
    def prepare_data(cls, data, reverse=False):
        if type(data) == dict:
            sorted_dict = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=reverse)}
            return list(sorted_dict.keys())[:cls.MOST_COMMON], list(sorted_dict.values())[:cls.MOST_COMMON]
        if type(data) == Counter:
            m_common = data.most_common(cls.MOST_COMMON)
            return list(zip(*m_common))
        return None
