import re
import pandas as pd

# read the messy data file to a list
lines = []
with open("/Users/djl47/PycharmProjects/MATH_381/Assignment 8/salaries_mess.txt") as file:
    for line in file:
        lines.append(line.strip())

# remove any empty elements of the list (blank lines in the file)
lines = list(filter(None, lines))

# remove the player's salary ranking
for element in lines:
    if element.isnumeric():
        lines.remove(element)

# if a period exists at the end of a name, remove it
# remove whitespace in the player's team
for element in lines:
    index = lines.index(element)
    if index % 3 == 0:
        element = element.replace(".", "")
        element += ","
        lines[index] = element
    if index % 3 == 1:
        element = element.strip()
        element += ","
        lines[index] = element

# reformat the salary and make relief pitchers/closers just closers
for element in lines:
    if lines.index(element) % 3 == 2:
        index = lines.index(element)
        element = element.replace("$", "")
        element = element.replace(",", "")
        element = element.replace("\t", ",")
        if element.__contains__("RP/CL"):
            element = element.replace("RP/CL", "CL")
        lines[index] = element

# add all information for one player as a single element of a new list
final_csv_list = []
for i in range(len(lines)):
    if i % 3 == 0:
        final_csv_list.append("")
    final_csv_list[int(i / 3)] += lines[i]

# write the list to a file in CSV format
with open("/Users/djl47/PycharmProjects/MATH_381/Assignment 8/player_salaries.txt", "w") as f:
    f.write("Name,Team,Position,Age,Salary\n")
    for item in final_csv_list:
        f.write(item + "\n")

# reformat the names in the baseball reference dataset
bb_ref_war = pd.read_csv("/Users/djl47/PycharmProjects/MATH_381/Assignment 8/bbref_war copy.txt")
new_names = []
for val in bb_ref_war['Name']:
    splt = re.split('\W+', val)
    new_names.append("")
    for name in splt:
        if name[0].isupper():
            new_names[bb_ref_war[bb_ref_war['Name'] == val].index[0]] += name + " "
for item in new_names:
    index = new_names.index(item)
    item = item.rstrip()
    if item.endswith("Jr"):
        item += "."
    new_names[index] = item

# rewrite the baseball reference dataset to csv with only relevant information
bb_ref_war['Name'] = new_names
bb_ref_war = bb_ref_war[['Name', 'Tm', 'Age', 'Salary']]
bb_ref_war.to_csv("/Users/djl47/PycharmProjects/Math_381/Assignment 8/bb_ref_war.csv", index=False)

fangraphs_WAR = pd.read_csv("/Users/djl47/PycharmProjects/MATH_381/Assignment 8/FanGraphs_WAR.csv")
fangraphs_WAR = fangraphs_WAR[['Name', 'PA', 'IP', 'Primary WAR', 'Total WAR']]
fangraphs_WAR.to_csv("/Users/djl47/PycharmProjects/Math_381/Assignment 8/FanGraphsWAR.csv", index=False)

