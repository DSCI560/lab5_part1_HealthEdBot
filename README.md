# lab5_part1_HealthEdBot
Scrape oil wells information from pdfs and drillingedge website, preprocess the data, and save to MySQL database

## OilWells_PDFExtraction.py
The provided code is a Python script designed to connect to a MySQL database, extract text from PDF files, parse specific information from the extracted text, and save the information to both the MySQL database and a CSV file (oil_wells_pdf_data.csv). 

## OilWells_WebScraping.py
The script is designed to read API numbers from the database or the CSV file, scrape well details for each API number from a website, and save the scraped data into a new CSV file.(oil_wells_details_scraped.csv).
