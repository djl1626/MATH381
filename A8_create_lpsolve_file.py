import pandas as pd

# read in the dataframe
players_table = pd.read_csv("/Users/djl47/PycharmProjects/MATH_381/Assignment 8/final_table_for_LP.csv")

# create a list of each relevant column
variable_list = list(players_table['variable'])
fWAR_list = list(players_table['Total.WAR'])
salary_list = list(players_table['Salary'])

# initialize all constraints as strings
var_string = ""
obj_function = "max:"
roster_constraint = ""
starting_pitchers_constraint = ""
relief_pitchers_constraint = ""
closing_pitchers_constraint = ""
catchers_constraint = ""
first_base_constraint = ""
second_base_constraint = ""
third_base_constraint = ""
shortstop_constraint = ""
left_fielders_constraint = ""
center_fielders_constraint = ""
right_fielders_constraint = ""
infielders_constraint = ""
outfielders_constraint = ""
salary_constraint = ""

# add the values/variables to each constraint string
for i in range(1, len(variable_list) + 1):
    var_string += str(variable_list[i - 1]) + ","
    obj_function += str(fWAR_list[i - 1]) + str(variable_list[i - 1]) + "+"
    roster_constraint += str(variable_list[i - 1]) + "+"
    salary_constraint += str(salary_list[i - 1]) + str(variable_list[i - 1]) + "+"
    if i <= 62:
        first_base_constraint += str(variable_list[i - 1]) + "+"
    elif 62 < i <= 147:
        second_base_constraint += str(variable_list[i - 1]) + "+"
    elif 147 < i <= 216:
        third_base_constraint += str(variable_list[i - 1]) + "+"
    elif 216 < i <= 331:
        catchers_constraint += str(variable_list[i - 1]) + "+"
    elif 331 < i <= 422:
        center_fielders_constraint += str(variable_list[i - 1]) + "+"
    elif 422 < i <= 456:
        closing_pitchers_constraint += str(variable_list[i - 1]) + "+"
    elif 456 < i <= 529:
        left_fielders_constraint += str(variable_list[i - 1]) + "+"
    elif 529 < i <= 599:
        right_fielders_constraint += str(variable_list[i - 1]) + "+"
    elif 599 < i <= 1125:
        relief_pitchers_constraint += str(variable_list[i - 1]) + "+"
    elif 1125 < i <= 1414:
        starting_pitchers_constraint += str(variable_list[i - 1]) + "+"
    else:
        shortstop_constraint += str(variable_list[i - 1]) + "+"

    if i <= 216 or i > 1414:
        infielders_constraint += str(variable_list[i - 1]) + "+"
    elif 331 < i <= 422 or 456 < i <= 599:
        outfielders_constraint += str(variable_list[i - 1]) + "+"

# get rid of extra + or , at the end of each constraint
var_string = var_string.rstrip(var_string[-1])
obj_function = obj_function.rstrip(obj_function[-1])
roster_constraint = roster_constraint.rstrip(roster_constraint[-1])
starting_pitchers_constraint = starting_pitchers_constraint.rstrip(starting_pitchers_constraint[-1])
relief_pitchers_constraint = relief_pitchers_constraint.rstrip(relief_pitchers_constraint[-1])
closing_pitchers_constraint = closing_pitchers_constraint.rstrip(closing_pitchers_constraint[-1])
catchers_constraint = catchers_constraint.rstrip(catchers_constraint[-1])
first_base_constraint = first_base_constraint.rstrip(first_base_constraint[-1])
second_base_constraint = second_base_constraint.rstrip(second_base_constraint[-1])
third_base_constraint = third_base_constraint.rstrip(third_base_constraint[-1])
shortstop_constraint = shortstop_constraint.rstrip(shortstop_constraint[-1])
left_fielders_constraint = left_fielders_constraint.rstrip(left_fielders_constraint[-1])
center_fielders_constraint = center_fielders_constraint.rstrip(center_fielders_constraint[-1])
right_fielders_constraint = right_fielders_constraint.rstrip(right_fielders_constraint[-1])
infielders_constraint = infielders_constraint.rstrip(infielders_constraint[-1])
outfielders_constraint = outfielders_constraint.rstrip(outfielders_constraint[-1])
salary_constraint = salary_constraint.rstrip(salary_constraint[-1])

# write all constraints and the objective function to a .txt file for lpsolve
with open("/Users/djl47/Documents/lp_solve_5.5/lp_solve/bin/osx64/Assignment_8/mlb_team_lp.txt", 'w') as f:
    f.write(obj_function + ";\n")
    f.write(starting_pitchers_constraint + "=5;\n")
    f.write(relief_pitchers_constraint + "=6;\n")
    f.write(closing_pitchers_constraint + "=1;\n")
    f.write(roster_constraint + "<=26;\n")
    f.write("payroll=" + salary_constraint + ";\n")
    f.write("catchers=" + catchers_constraint + ";\n")
    f.write("first_basemen=" + first_base_constraint + ";\n")
    f.write("second_basemen=" + second_base_constraint + ";\n")
    f.write("third_basemen=" + third_base_constraint + ";\n")
    f.write("shortstops=" + shortstop_constraint + ";\n")
    f.write("left_fielders=" + left_fielders_constraint + ";\n")
    f.write("center_fielders=" + center_fielders_constraint + ";\n")
    f.write("right_fielders=" + right_fielders_constraint + ";\n")
    f.write("infielders=" + infielders_constraint + ";\n")
    f.write("outfielders=" + outfielders_constraint + ";\n")
    f.write("payroll<=230;\n")
    f.write("catchers>=2;\n")
    f.write("first_basemen>=1;\n")
    f.write("second_basemen>=1;\n")
    f.write("third_basemen>=1;\n")
    f.write("shortstops>=1;\n")
    f.write("left_fielders>=1;\n")
    f.write("center_fielders>=1;\n")
    f.write("right_fielders>=1;\n")
    f.write("infielders>=5;\n")
    f.write("outfielders>=4;\n")
    f.write("bin " + var_string + ";")
