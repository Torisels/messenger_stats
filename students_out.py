from matplotlib import pyplot as plt
import csv

file_mako_1 = "m1.csv"
file_mako_2 = "m2.csv"


mako1_people = []


def get_people(f_n):
    people = []
    with open(f_n, encoding="utf8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            people.append(row[0]+" "+row[1])
    people.pop(0)
    return people


mako1 = get_people(file_mako_1)
mako2 = get_people(file_mako_2)
stay = len((set(mako1).intersection(mako2)))


labels = f'Zostało {stay}', f'Odpadło {len(mako1) - stay}'
sizes = [stay, len(mako1) - stay]


fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
         startangle=90)
ax1.axis('equal')
plt.title("Odsiew na podstawie list MAKO1/2 \n MAKO1: 144")
plt.show()