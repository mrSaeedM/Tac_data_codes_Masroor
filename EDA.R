# Install and load the gtsummary package if not already installed
if (!requireNamespace('gtsummary', quietly = TRUE)) {
  install.packages('gtsummary')
}

library(dplyr)
library(gtsummary)
setwd('/Users/saeedmasroor/Documents/applications/Bioinformatician Pharmacology and Toxicology - Radboud')

# read the df_merged.csv file
all_data <- read.csv('merged_df2.csv')
# list of columns in the data
names(all_data)
# select the columns of interest
selected_cols <- c('Type.of.transplant','Age.at.Tx',
                  'gender_MF' , 'AverageTacDose', 
                  'TotalTacDose' , 'CKD'   )
data <- all_data[, selected_cols, drop = FALSE]

# Create a summary table using gtsummary

table1 <-
  tbl_summary(
    data,
    by = CKD, # split table by group
    missing = "no" # don't list missing data separately
  ) %>%
  add_n() %>% # add column with total number of non-missing observations
  add_p() %>% # test for a difference between groups
  modify_header(label = "**Variable**") %>% # update the column header
  bold_labels()

print(table1)
table1 %>%
  as_gt() %>%
  gt::gtsave(filename = "Table1.png") # use extensions .png, 

##############################################################
# build logistic regression model
model1 <- glm(CKD ~ Type.of.transplant + Age.at.Tx+I((Age.at.Tx)^2)+
                gender_MF+AverageTacDose+ 
              TotalTacDose , data, family = binomial)

table2 <- tbl_regression(model1, exponentiate = TRUE)%>% bold_labels()

print(model1)

table2 %>%
  as_gt() %>%
  gt::gtsave(filename = "Table2.png") # use extensions .png, 
##############################################################
# Build linear regression model
model2 <- glm(Last_GFR173 ~ Type.of.transplant + Age.at.Tx+ 
                gender_MF+AverageTacDose+ 
                TotalTacDose , all_data, family = gaussian)

table3 <- tbl_regression(model2)%>% bold_labels()

print(model2)

table3 %>%
  as_gt() %>%
  gt::gtsave(filename = "Table3.png") # use extensions .png, 