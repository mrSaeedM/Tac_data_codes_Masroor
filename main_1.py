from xls2xlsx import XLS2XLSX
import glob
import os

# get all the xls files in the current directory and its subdirectories
files = glob.glob('**/*.xls', recursive=True)

# loop through the files and convert them to xlsx
for file in files:
    print(file)
    # if os.path.exists(file+'x'):
    #     print(f'file {file} already exists')
    #     continue
    
    try:
        x2x = XLS2XLSX(file)
    except Exception as e:
        # in case of error reading the file, print the file name and error message
        print(f"Skipped {file} due to error: {e}")  
    try:    
        x2x.to_xlsx(file + 'x')
    except Exception as e:
    # in case of error writing the file, print the file name and error message
        print(f"Skipped {file} due to error: {e}")     


