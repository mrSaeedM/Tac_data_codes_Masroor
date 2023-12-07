import pandas as pd 

# read the file Age at transplant.xlsx
Age_at_transplant = pd.read_excel('Assignment/Data/Age at transplant.xlsx')
# Age_at_transplant.ID = (Age_at_transplant.ID).astype(int)
latest_GFR173 = pd.read_csv('latest_GFR173.csv')

latest_GFR173.rename(columns={'LatestMeasurement': 'Last_GFR173'}, inplace=True)


merged_df = pd.merge(Age_at_transplant, latest_GFR173, left_on='ID', right_on='ID1000', how='outer')
merged_df = merged_df.drop(columns=['ID_y', 'ID1000'])
merged_df.rename(columns={'ID_x': 'StudyID'}, inplace=True)
merged_df.StudyID = (merged_df.StudyID).astype(str)
##################################################################
df_Gender = pd.read_csv('df_Gender.csv')
df_Gender.rename(columns={'ID': 'StudyID'}, inplace=True)
df_Gender.StudyID = (df_Gender.StudyID+1000).astype(str)

merged_df = pd.merge(merged_df, df_Gender, on='StudyID', how='outer')

merged_df['gender_MF'] = merged_df['Gender'].combine_first(merged_df['Gender_retreieved'])
merged_df = merged_df.drop(columns=['Gender', 'Gender_retreieved'])


merged_df.to_csv('merged_df.csv')

print(merged_df.head())

####################################################################
# read the file Medication.xlsx
Medication = pd.read_excel('Assignment/Data/Medication.xlsx')

# save the unique entries in the Drug column in a list
Meds = Medication.Drug.unique().tolist()
# Search in the Meds list for entries that contain the word 'tacro' 
# and save them in a list
# the search is not case sensitive
tacro = [med for med in Meds if 'tacro' in med.lower()]
# Find entries that contain the word 'tacro' in the Drug column and save
#  them in a new dataframe

Medication_tacrolimus = Medication[Medication.Drug.isin(tacro)]
# save Medication_tacrolimus in a new excel file
Medication_tacrolimus.to_excel('Medication_tacrolimus.xlsx')
##################################################################
Medication_tacrolimus = pd.read_excel('Medication_tacrolimus.xlsx')

Medication_tacrolimus.Dose = (Medication_tacrolimus.Dose).astype(float)

Medication_tacro_mean_total = Medication_tacrolimus.groupby('StudyID').agg(AverageTacDose=('Dose', 'mean'),
                               TotalTacDose=('Dose', 'sum')).reset_index()

Medication_tacro_mean_total['AverageTacDose'] = Medication_tacro_mean_total['AverageTacDose'].round(2)
Medication_tacro_mean_total['TotalTacDose'] = Medication_tacro_mean_total['TotalTacDose'].round(2)

Medication_tacro_mean_total.head()

merged_df2 = pd.merge(merged_df, Medication_tacro_mean_total, on='StudyID', how='outer')
merged_df2 = merged_df2.dropna(subset=['CKD']).drop_duplicates()

merged_df2.to_csv('merged_df2.csv')
##################################################################
import pandas as pd
merged_df2 = pd.read_csv('merged_df2.csv')
# Count the number of missing values in each column
missing_values_count = merged_df2.isnull().sum()
# Print the result
print(missing_values_count)
print(merged_df2.shape)