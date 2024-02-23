import csv
import requests
from bs4 import BeautifulSoup
import re

# Assuming 'data' is a list of dictionaries read from your CSV
# Each dictionary contains keys 'API#' and 'Well Name'


# Define the function to read API numbers again
def read_api_numbers_from_csv(csv_file_path):
    # Regular expression to find API numbers
    api_regex = re.compile(r'\b\d{2}-\d{3}-\d{5}\b')
    api_numbers = set()

    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Search for API numbers in the 'Well Name' column
            if 'Well Name' in row and row['Well Name']:
                found_api = api_regex.search(row['Well Name'])
                if found_api:
                    api_numbers.add(found_api.group())

    return list(api_numbers)




def scrape_well_details(api_number):
    # Construct the URL using the API number
    search_url = f'https://www.drillingedge.com/search?type=wells&api_no={api_number}&page=1'
    well_details = {'API Number': api_number}

    # Use requests to perform the search on the website
    response = requests.get(search_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Assuming that the first match is the desired one
        # Since we have the direct URL, we don't need to iterate through the rows
        # Extract the well name, lease name, location, operator, and status from the table
        well_name = soup.find('a', title=lambda x: x and 'Well in' in x).get_text(strip=True) if soup.find('a', title=lambda x: x and 'Well in' in x) else 'Not found'
        lease_name = soup.find('td', class_='nowrap').find_next_sibling('td').get_text(strip=True)
        location = soup.find('td', class_='nowrap').find_next_siblings('td')[2].get_text(strip=True)
        operator = soup.find('a', title=lambda x: x and 'Operator in' in x).get_text(strip=True) if soup.find('a', title=lambda x: x and 'Operator in' in x) else 'Not found'
        status = soup.find('td', class_='nowrap').find_next_siblings('td')[4].get_text(strip=True)

        # Add the extracted data to the well_details dictionary
        well_details['Well Name'] = well_name
        well_details['Lease Name'] = lease_name
        well_details['Location'] = location
        well_details['Operator'] = operator
        well_details['Status'] = status

    else:
        print(f"Failed to retrieve data for API number {api_number}. Status Code: {response.status_code}")

    return well_details



# # Modify this function to write results to a new CSV
# def write_scraped_data_to_csv(input_csv, output_csv):
#     with open(input_csv, mode='r') as csvfile, open(output_csv, mode='w', newline='') as outputfile:
#         reader = csv.DictReader(csvfile)
#         fieldnames = ['API#', 'Well Name', 'Well Status', 'Well Type', 'Closest City', 'Barrels of Oil Produced']
#         writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
#         writer.writeheader()

#         for row in reader:
#             api_number = row['API#']
#             well_name = row['Well Name']
#             additional_info = scrape_well_details(api_number)
#             # Combine row data with the additional_info
#             row.update(additional_info)
#             writer.writerow(row)

# # Specify your input and output CSV filenames
# input_csv_filename = 'oil_wells_data.csv'
# output_csv_filename = 'scraped_well_details.csv'

# # Call the function with the CSV filenames
# write_scraped_data_to_csv(input_csv_filename, output_csv_filename)



# Define the function to write the scraped data to a new CSV file
def write_scraped_data_to_csv(api_numbers, output_csv_path):
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['API Number', 'Well Name', 'Lease Name', 'Location', 'Operator', 'Status']  # Extend fieldnames as needed
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for api_number in api_numbers:
            well_details = scrape_well_details(api_number)
            writer.writerow(well_details)

# Input and output CSV paths
input_csv_path = 'oil_wells_data.csv'
output_csv_path = 'oil_wells_details_scraped.csv'

# Read API numbers and write the scraped data to the output CSV
api_numbers = read_api_numbers_from_csv(input_csv_path)
write_scraped_data_to_csv(api_numbers, output_csv_path)