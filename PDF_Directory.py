import os
import datetime
import pandas as pd
import PyPDF2

# Set the folder path where the PDF documents are stored
folder_path = "/path/to/folder"

# Initialize an empty list to hold the PDF file details
pdf_list = []

# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a PDF
    if filename.endswith(".pdf"):
        # Open the PDF file
        with open(os.path.join(folder_path, filename), "rb") as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Get the number of pages in the PDF
            num_pages = pdf_reader.numPages

            # Extract the creation date of the PDF
            creation_date = datetime.datetime.strptime(pdf_reader.documentInfo['/CreationDate'][2:], '%y%m%d%H%M%S')

            # Extract the text from the first page of the PDF
            page_obj = pdf_reader.getPage(0)
            text = page_obj.extractText()

            # Add the PDF file details to the list
            pdf_list.append({"Filename": filename, "Pages": num_pages, "Creation Date": creation_date, "Text": text})

# Convert the list of PDF file details to a pandas DataFrame
pdf_df = pd.DataFrame(pdf_list)

# Export the DataFrame to an Excel file
pdf_df.to_excel("pdf_inventory.xlsx",index=False)