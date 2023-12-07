import pandas as pd
import numpy as np
from extract_gfr import extract_gfr_measurements, extract_Patient_ID, extract_date_from_text

import glob

# get all the xls files in the current directory and its subdirectories
files = glob.glob('**/*GFR*.xlsx', recursive=True)

df_GFR = pd.DataFrame(columns=['ID','Date','GFR173'])

for file in files:
    try:
        print(file)
        df = pd.read_excel(file, skiprows=1, header=None)
        # print(df.head())
        
        for index, row in df.iterrows():
                GFR173 = []
                # Assuming the first column is numeric and contains the ID that we want 
                ID_patient = extract_Patient_ID(row[0])
                for column, value in row.items():
                    if extract_gfr_measurements(value) is not None:
                        GFR173.extend(extract_gfr_measurements(value))
                    # print(GFR173)
                    Date_measurement = extract_date_from_text(value)
                    if ID_patient is not None:
                        # add ID_patient, Date_measurement, GFR173 to the dataframe using concat
                        df_GFR = pd.concat([df_GFR, pd.DataFrame([[ID_patient, Date_measurement, GFR173]], columns=['ID','Date','GFR173'])])



    #             # print(f"patient {ID_patient} on {Date_measurement} GFR173 is",GFR173 )
    except Exception as e:
        print(f"Error reading Excel file: {e}")
# sord the df_GFR by ID and Date
df_GFR = df_GFR.sort_values(['ID','Date'])

# calculate the minimum GFR173 for each patient at each date
df_GFR['Min_GFR173'] = df_GFR['GFR173'].apply(lambda x: min(x) if x else None)
df_GFR.to_csv('GFR173.csv',index=False)


# calculate the minimum GFR173 for each patient at any time point
# min_measurements = df_GFR.groupby('ID')['Min_GFR173'].apply(lambda x: min(x) if x[0] else None).reset_index()
min_GFR173_overall = df_GFR.groupby('ID')['Min_GFR173'].agg(MinMeasurement='min').reset_index()

min_GFR173_overall.columns = ['ID', 'min_GFR173_overall']
min_GFR173_overall.to_csv('min_GFR173_overall.csv',index=False)

print(len(df_GFR.ID.unique()))

# Count the number of entries below 75 in each column
below_75_count = ((min_GFR173_overall.min_GFR173_overall) < 75).sum()
print(below_75_count)
# Count the number of NaN entries in each column
nan_count = min_GFR173_overall['min_GFR173_overall'].isna().sum()
print(nan_count)

###############################################################################################
#latest measurements

# Convert 'TimePoint' to datetime type
df_GFR['Date'] = pd.to_datetime(df_GFR['Date'],format='%Y-%m-%d')
# Filter out rows with NaN in 'TimePoint'
# df_GFR = df_GFR.dropna(subset=['Date'])

# Find the measurement of the latest time point for each ID
latest_GFR173 = df_GFR.groupby('ID').agg(LatestMeasurement=('Min_GFR173', 'last')).reset_index()


print(latest_GFR173.head())

below_75_count_latest = ((latest_GFR173.LatestMeasurement) < 75).sum()
print(below_75_count_latest)

nan_count = latest_GFR173['LatestMeasurement'].isna().sum()
print(nan_count)

latest_GFR173 = latest_GFR173.dropna()
latest_GFR173['ID1000'] = latest_GFR173.ID + 1000
latest_GFR173['CKD'] = [1 if x < 75 else 0 for x in latest_GFR173['LatestMeasurement']]
latest_GFR173.to_csv('latest_GFR173.csv',index=False)