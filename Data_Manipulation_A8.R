# load the tidyverse library
library(tidyverse)

# read in the file of player salaries from spotrac
spotrac_salaries <- read_csv("player_salaries.txt") %>% 
  select(Name, Position, Salary)

# read in the fWAR for each player and remove a player that I could not find
# a salary for
fangraphs_WAR <- read.csv("FanGraphsWAR.csv") %>%
  select(Name, PA, IP, Primary.WAR, Total.WAR) %>% slice(-1335)

# join the fWAR table with the spotrac salary table
fangraphs_WAR_salaries <- left_join(fangraphs_WAR, spotrac_salaries)

# find all players without a spotrac salary
no_salary <- fangraphs_WAR_salaries %>% filter(is.na(Salary))

# find all players with a spotrac salary
has_spotrec_salary <- fangraphs_WAR_salaries %>% 
  filter(!is.na(Salary))

# read in the baseball reference dataframe
bb_ref <- read_csv("bb_ref_war.csv")

# take out the $ in all baseball reference salaries
vec <- c()
for (val in bb_ref$Salary) {
  if (!is.na(val)) {
    val <- substr(val, 2, nchar(val))
  }
  vec <- append(vec, val)
}

# change the Salary column type to a numeric in the baseball reference
# dataframe
bb_ref$Salary <- as.numeric(vec)

# join the players with missing salaries to the baseball reference dataframe
with_bb_ref_salary <- left_join(no_salary, bb_ref, by=c('Name' = 'Name')) %>% 
  select(Name, PA, IP, Primary.WAR, Total.WAR, Position, Salary.y)

# find all players where a salary was found from baseball reference
has_bb_ref_salary <- with_bb_ref_salary %>% filter(!is.na(Salary.y))

# change column name
colnames(has_bb_ref_salary)[which(names(has_bb_ref_salary) == "Salary.y")] <- "Salary"

# find all players without a salary from spotrac and baseball reference
no_salary <- with_bb_ref_salary %>% filter(is.na(Salary.y))

# write the missing salaries to a csv
write_csv(no_salary, 'missing_salaries.csv')

# after finding values for all missing salaries by hand, read in that dataframe
found_salaries <- read_csv("salaries_found.csv") %>% 
  select(Name, Primary.WAR, Total.WAR, Position, Salary)

# join the found salaries with the fWAR table
found_salaries <- inner_join(found_salaries, fangraphs_WAR, by=c('Name' = 'Name'))
found_salaries <- found_salaries %>% 
  select(Name, PA, IP, Primary.WAR.x, Total.WAR.x, Position, Salary)

# change column names
colnames(found_salaries)[which(names(found_salaries) == "Primary.WAR.x")] <- "Primary.WAR"
colnames(found_salaries)[which(names(found_salaries) == "Total.WAR.x")] <- "Total.WAR"

# join missing salaries to the found salaries table
no_salary_found_salary <- left_join(no_salary, found_salaries, by=c('Name' = 'Name')) %>% 
  select(Name, PA.x, IP.x, Primary.WAR.x, Total.WAR.x, Position.y, Salary)

# change column names
colnames(no_salary_found_salary)[which(names(no_salary_found_salary) == "Primary.WAR.x")] <- "Primary.WAR"
colnames(no_salary_found_salary)[which(names(no_salary_found_salary) == "Total.WAR.x")] <- "Total.WAR"
colnames(no_salary_found_salary)[which(names(no_salary_found_salary) == "PA.x")] <- "PA"
colnames(no_salary_found_salary)[which(names(no_salary_found_salary) == "IP.x")] <- "IP"
colnames(no_salary_found_salary)[which(names(no_salary_found_salary) == "Position.y")] <- "Position"

# create csv of players so we can find the last missing salaries and change them in the file
write_csv(no_salary_found_salary, "final_missing_salaries.csv")

# reread the complete salaries table
final_missing_salaries <- read_csv("final_missing_salaries.csv")

# change column name
colnames(final_missing_salaries)[which(names(final_missing_salaries) == "Position.y")] <- "Position"

# bind all tables to one final table and remove all duplicated names if they exist
final_table <- rbind(has_spotrec_salary, has_bb_ref_salary)
final_table <- rbind(final_table, found_salaries)
final_table <- rbind(final_table, final_missing_salaries)
final_table <- final_table[!duplicated(final_table$Name), ]

# find all players with no position
no_positions <- final_table %>% filter(is.na(Position))

# write csv of players with missing position
write_csv(no_positions, 'no_positions.csv')

# read in the csv of players that now have positions
yes_positions <- read_csv("positions_found.csv")

# join the table to have all players have a position
positions <- left_join(no_positions, yes_positions, by=c('Name' = 'Name')) %>%
  select(Name, PA.x, IP.x, Primary.WAR, Total.WAR, Position.y, Salary.x)

# change column names
colnames(positions)[which(names(positions) == "PA.x")] <- "PA"
colnames(positions)[which(names(positions) == "IP.x")] <- "IP"
colnames(positions)[which(names(positions) == "Position.y")] <- "Position"
colnames(positions)[which(names(positions) == "Salary.x")] <- "Salary"

# add one guy's position because he has a weird name
positions[positions$Name == 'Michael A Taylor', 'Position'] <- "CF"

#filter out players without position, bind the table with their positions
final_table <- final_table %>% filter(!is.na(Position))
final_table <- rbind(final_table, positions) %>% arrange(Position)

# mutate a variable for lpsolve onto each player
final_table <- final_table %>% mutate("variable" = paste("x_", row_number(), sep=''))

# make the minimum salary for all players 570500 and make salaries in terms of millions
final_table <- final_table %>% 
  mutate(Salary = case_when(Salary < 570500 ~ .570500,
                              TRUE ~ Salary / 1000000))

# write a csv file for the final table
write_csv(final_table, 'final_table_for_LP.csv')
