import os
import csv
import mysql.connector
from mysql.connector import Error
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import fitz
import re
# from bs4 import BeautifulSoup
# import requests

# Define the function to check the MySQL connection and return the cursor and connection
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='oil_wells',
            user='root',
            password='Ldy990912')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            return cursor, connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None, None

# Define the function to save data to CSV
def save_to_csv(data, filename='oil_wells_data.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Test Date', 'Operator', 'Well Name', 'Location', 'Formation', 'Tool Type', 'Tubing Size', 'Well Type'])
        writer.writerows(data)

# Define the function to extract text from PDF using OCR
    # def extract_text_from_pdf(pdf_path):
    #     images = convert_from_path(pdf_path)
    #     text = ''
    #     for image in images:
    #         text += pytesseract.image_to_string(image)
    #     return text
def extract_text_from_pdf(pdf_path):
    text = ''
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

# Define the function to parse the text and extract relevant data
# def parse_text(text):
#     # Here you will implement the parsing logic based on the format of your PDF
#     # This is a placeholder function to demonstrate the workflow
#     reader = PdfReader(pdf_path)
#     page = reader.pages[0]  # Assuming information is on the first page
#     text = page.extract_text()
#     # Use text processing here to extract the required fields
#     # Example:
#     test_date = text.split("Test Date:")[1].split("\n")[0].strip()
#     operator = text.split("Operator:")[1].split("\n")[0].strip()
#     well_name = text.split("Well Name:")[1].split("\n")[0].strip()
#     location = text.split("Location:")[1].split("\n")[0].strip()
#     # ... continue for other fields
#     return [test_date, operator, well_name, location]  # Example return


def parse_text(text):
    # Dictionary to hold the parsed data
    parsed_data = {
        'Test Date': None,
        'Operator': None,
        'Well Name': None,
        'Location': None,
        # Add more fields as necessary
    }
    
    # Helper function to safely get data
    def get_data_after_colon(label, default=None):
        parts = text.split(label)
        return parts[1].split("\n")[0].strip() if len(parts) > 1 else default

    # Use the helper function to extract data
    parsed_data['Test Date'] = get_data_after_colon("Test Date:")
    parsed_data['Operator'] = get_data_after_colon("Operator:")
    parsed_data['Well Name'] = get_data_after_colon("Well Name:")
    parsed_data['Location'] = get_data_after_colon("Location:")
    # Continue for other fields
    
    # Return the data as a list or in the desired format
    return [parsed_data[field] for field in parsed_data]


# # Function to extract text from PDF and find API numbers
# def find_api_numbers_in_pdf(pdf_path):
#     api_numbers = []
#     with fitz.open(pdf_path) as pdf:
#         for page in pdf:
#             text = page.get_text()
#             matches = api_pattern.findall(text)
#             api_numbers.extend(matches)
#     return api_numbers



# # Function to iterate over all PDFs and save API numbers to a CSV file
# def save_api_numbers_to_csv(folder_path, output_filename='api_numbers.csv'):
#     api_numbers = []
#     for pdf_file in os.listdir(folder_path):
#         if pdf_file.lower().endswith('.pdf'):
#             pdf_path = os.path.join(folder_path, pdf_file)
#             api_numbers_in_file = find_api_numbers_in_pdf(pdf_path)
#             api_numbers.extend(api_numbers_in_file)
    
#     # Remove duplicates and sort the API numbers
#     api_numbers = sorted(set(api_numbers))

#     # Save the API numbers to a CSV file
#     with open(output_filename, mode='w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['API Number'])  # Write header
#         for api_number in api_numbers:
#             writer.writerow([api_number])  # Write each API number in a new row



# Connect to MySQL
cursor, connection = connect_to_mysql()

# Check if connection is successful, if not save the data in a CSV or Excel
if cursor is not None and connection is not None:
    # Implement the logic to create the database tables and insert data
    # Example:
    # cursor.execute("CREATE TABLE IF NOT EXISTS wells (test_date VARCHAR(255), operator VARCHAR(255), well_name VARCHAR(255), location VARCHAR(255), ...)")
    pass
else:
    print("MySQL connection could not be established, saving data to CSV.")

# Path to the directory containing PDFs
pdf_folder_path = 'DSCI560_Lab5'  # Replace with the path to your PDF folder
extracted_data = []

# Iterate over all the PDFs in the folder
for pdf_file in os.listdir(pdf_folder_path):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder_path, pdf_file)
        text = extract_text_from_pdf(pdf_path)
        data = parse_text(text)
        extracted_data.append(data)

        # If connected to MySQL, insert data into the database
        if cursor is not None and connection is not None:
            # Example INSERT statement (you will need to adapt this to your table schema)
            insert_query = "INSERT INTO wells (test_date, operator, well_name, location) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, data)
            connection.commit()

# If MySQL connection was not successful, save the extracted data to CSV
if cursor is None or connection is None:
    save_to_csv(extracted_data)



# # Define a pattern to match API numbers
# api_pattern = re.compile(r'\bAPI\s*#?:?\s*(\d{2}-\d{5}-\d{5})\b')


# # Call the function with the folder path
# save_api_numbers_to_csv(pdf_folder_path)


# Close the MySQL connection
if connection is not None and connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")


