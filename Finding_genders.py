import pandas as pd

import glob

# get all the xls files in the current directory and its subdirectories
files = glob.glob('**/*Basic*.xlsx', recursive=True)

col_names= columns=['ID','Gender_retreieved']
df_Gender = pd.DataFrame(columns=col_names)

for file in files:
    try:
        print(file)
        df = pd.read_excel(file)
        for c in df.columns.tolist():
            if (c.lower() == 'id'):
                id_column = c 

            if ('sex' in c.lower()) and ('donor' not in c.lower()):
                gender_column = c
        if id_column and gender_column:        
            df_new = df.loc[:,[id_column, gender_column]] 
            df_new.columns = col_names     
            df_Gender = pd.concat([df_Gender,df_new],axis=0,ignore_index=True)
            # print(df_new.head())
            # df_Gender.ID = df_Gender.ID.astype(str)
    except Exception as e:
        print(f"Error reading Excel file: {e}")

df_Gender = df_Gender.drop_duplicates()
# drop entries with missing gender
df_Gender = df_Gender.dropna(subset=['Gender_retreieved'])
#sort df_Gender by ID column
df_Gender.sort_values(by=['ID'], inplace=True)    
print(df_Gender.head())
df_Gender.to_csv('df_Gender.csv',index=False)