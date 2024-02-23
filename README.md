# lab5_part1_HealthEdBot
Scrape oil wells information from pdfs and drillingedge website, preprocess the data, and save to MySQL database

## OilWells_PDFExtraction.py
The provided code is a Python script designed to connect to a MySQL database, extract text from PDF files, parse specific information from the extracted text, and save the information to both the MySQL database and a CSV file (oil_wells_pdf_data.csv). 

## OilWells_WebScraping.py
The script is designed to read API numbers from the database or the CSV file, scrape well details for each API number from a website, and save the scraped data into a new CSV file. It uses requests to fetch web pages, BeautifulSoup to parse HTML, and csv for reading and writing CSV files. The read_api_numbers_from_csv function extracts API numbers from the specified CSV file. The scrape_well_details function constructs a URL for each API number, scrapes the web page for well details, and stores the information in a dictionary. Finally, the write_scraped_data_to_csv function writes the scraped details for all API numbers into a new CSV file (oil_wells_details_scraped.csv).
