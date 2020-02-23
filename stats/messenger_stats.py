import re
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.backends.backend_pdf import PdfPages
from collections import Counter


class MessengerStats:
    REGEX_XD = re.compile(r"[xX]([dD])+")
    REGEX_CRV = re.compile(r"(ku+rw)|(cooo*rva+)")
    MOST_COMMON = 10
    PARSERS = {"total_msg": ["Całkowita liczba wiadomości"],
               "received_reactions": ["Całkowita liczba otrzymanych reakcji"],
               "given_reactions": ["Całkowita liczba dawanych reakcji"],
               "xds": ["Całkowita liczba wiadomości z 'xD' lub podobnymi"],
               "total_photos":["Całkowita liczba wrzuconych zdjęć"],
               "total_characters": ["Całkowita liczba znaków"],
               "total_words": ["Całkowita liczba słów (rozdzielane spacjami wyrażenia)"],
               "crv":["(ku+rw)|(cooo*rva+) na osobę "]}

    def __init__(self, data, participants):
        self.messages = data
        self.participants = participants
        self.parsers = [self.count_messages, self.count_received_reactions, self.count_xds, self.count_photos, self.count_characters]
        self.parsed_data = {k: Counter() for k in self.PARSERS.keys()}
        self.reactions = Counter()
        self.pdf = PdfPages('multipage_pdf.pdf')
        self.unique_words = {k: Counter() for k in self.participants}



    def run(self):
        for message in self.messages:
            for parser in self.parsers:
                parser(message)
        self.generate_graphs()
        # print(self.unique_words)
        # res = ' '.join(sorted(self.unique_words, key=lambda key: len(self.unique_words[key]), reverse=True))
        # uniq_words = {k: len(self.unique_words[k]) for k in self.unique_words.keys()}
        # sorted_d = sorted(uniq_words.items(), key=lambda x: x[1])
        #
        # print(sorted_d)

    def generate_graphs(self):
        for name, data in self.parsed_data.items():
            keys, vals = self.prepare_data(data)
            self.draw_graph(self.PARSERS[name][0], keys, vals, save=f"graphs/{name}.png")

        keys, vals = self.prepare_data(self.reactions)
        keys = list(keys)
        keys[1] = "Like"
        keys[7] = "Dislike"
        print(keys)
        self.draw_graph("Dystrybucja typów reakcji", keys, vals,save=f"graphs/reakcje.png" )

        uniq_words = {k: len(self.unique_words[k]) for k in self.unique_words.keys()}
        keys, vals = self.prepare_data(uniq_words, True)
        self.draw_graph("Różnorodność słownictwa", keys, vals, save=f"graphs/distinct_words.png")

        self.pdf.close()

    def count_messages(self, message):
        self.parsed_data["total_msg"][message["sender_name"]] += 1

    def count_received_reactions(self, message):
        if "reactions" in message:
            self.parsed_data["received_reactions"][message["sender_name"]] += len(message["reactions"])
            for reaction in message["reactions"]:
                self.parsed_data["given_reactions"][reaction["actor"]] += 1
                self.reactions[reaction["reaction"]] += 1

    def count_xds(self, message):
        if "content" in message:
            if self.REGEX_XD.search(message["content"]):
                self.parsed_data["xds"][message["sender_name"]] += 1
            if self.REGEX_CRV.search(message["content"]):
                self.parsed_data["crv"][message["sender_name"]] += 1

            words = message["content"].split()
            for word in words:
                try:
                    self.unique_words[message["sender_name"]][word] += 1
                except KeyError as e:
                    print(e)
    def count_photos(self, message):
        if "photos" in message:
            self.parsed_data["total_photos"][message["sender_name"]] += len(message["photos"])

    def count_characters(self, message):
        if "content" in message:
            self.parsed_data["total_characters"][message["sender_name"]] += len(message["content"])
            self.parsed_data["total_words"][message["sender_name"]] += len(message["content"].split())



    def draw_graph(self, title, keys, values, x_label="", y_label="", save=""):
        fig, ax = plt.subplots()
        for i, v in enumerate(values):
            ax.text(v + 1, i - 0.05, v)
        plt.barh(keys, values)
        plt.title(title)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.gca().invert_yaxis()
        if save is "":
            plt.show()
        else:
            # plt.show()
            self.pdf.savefig(fig, bbox_inches='tight')
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
