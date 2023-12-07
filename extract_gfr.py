
import re

def extract_gfr_measurements(text):
    # Define a regular expression pattern to match the GFR measurements

    pattern = "GFR/1\.73sq\.m\.:(\d+)"


    # Use the modified pattern to search for matches in the text
    text = str(text)
    matches = re.findall(pattern, ''.join(text.split()))
    gfr_per_173_sqm = [int(match) for match in matches]

    if gfr_per_173_sqm is not None:
        return gfr_per_173_sqm
    else :
        return None
    # matches = re.search(pattern, ''.join(text.split()))
    # # If a match is found, extract the measurements
    # gfr_per_173_sqm = []
    # if matches is not None:
    #     for match in matches:
    #         # print(text)
    #         # print('The match is ',int(match))
    #         gfr_per_173_sqm.append(int(match))
    #         # print('The list is ',gfr_per_173_sqm)
    #     return gfr_per_173_sqm
    # else:
    #     return None

# Example usage
# text = "GFR: 63mls/min. GFR/sq.m.:52 mls/min. GFR/1.73 sq.m.:91 mls/min"
# text = "GFR:103 mls/min. GFR/sq.m.:108 mls/ min. GFR/1.73 sq .m .:187 mls/min."
# measurements = extract_gfr_measurements(text)

# if measurements:
#     gfr_per_173_sqm = measurements

#     print("GFR/1.73 sq.m.:", gfr_per_173_sqm)
# else:
#     print("No GFR measurements found in the text.")




import numpy as np

def extract_Patient_ID(input_string, max_chars=4):
    # Use a regular expression to match the numeric prefix
    match = re.match(r'^\d{1,' + str(max_chars) + '}', str(input_string))
    
    # Check if a match is found
    if match:
        # Extract the matched numeric prefix
        numeric_prefix = match.group(0)
        return int(numeric_prefix)
    else:
        # No numeric prefix found, return NaN
        return np.nan

# Example usage
# input_string_1 = "1abc"
# input_string_2 = "abc123"
# input_string_3 = "446abc"
# input_string_4 = "9876xyz"

# result_1 = extract_numeric_prefix(input_string_1)
# result_2 = extract_numeric_prefix(input_string_2)
# result_3 = extract_numeric_prefix(input_string_3)
# result_4 = extract_numeric_prefix(input_string_4)

# print(result_1)  # Output: 123
# print(result_2)  # Output: NaN
# print(result_3)  # Output: NaN
# print(result_4)  # Output: 9876



def extract_date_from_text(text):
    # Define a regular expression pattern to match the date format "YYYY-MM-DD"
    date_pattern = r'\b(\d{4}-\d{2}-\d{2})\b'

    # Use re.search to find the pattern in the text
    match = re.search(date_pattern, str(text))

    # Check if a match is found
    if match:
        extracted_date = match.group(1)
        return extracted_date
    else:
        return None

