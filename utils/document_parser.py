# Import PyPDF2 for reading and extracting text from PDF files
import PyPDF2
# Import python-docx for reading and extracting text from Word documents
import docx
from typing import Dict

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        file_path (str): The path to the PDF file.
        
    Returns:
        str: The extracted text from all pages.
    """
    # Open the PDF file in read-binary mode ("rb") which is required by PyPDF2
    with open(file_path, "rb") as f:
        # Initialize the PDF reader object
        reader = PyPDF2.PdfReader(f)
        text = ""
        # Iterate through all the pages in the PDF document
        for page in reader.pages:
            # Extract the text from the current page
            extracted = page.extract_text()
            if extracted:
                # Append the extracted text with a newline separator
                text += extracted + "\n"
    # Return the fully extracted text
    return text

def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file.
    
    Args:
        file_path (str): The path to the Word document.
        
    Returns:
        str: The extracted text from all paragraphs.
    """
    # Load the Word document using the docx library
    doc = docx.Document(file_path)
    # Extract text from each paragraph and join them with newline characters
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file_path: str) -> Dict[str, str]:
    """
    Auto-detect the file format based on its extension and extract its text.
    
    Args:
        file_path (str): The path to the document file.
        
    Returns:
        Dict[str, str]: A dictionary containing the detected format and the extracted text.
    """
    # Check if the file is a PDF by its extension
    if file_path.endswith(".pdf"):
        return {"format": "pdf", "text": extract_text_from_pdf(file_path)}
    # Check if the file is a DOCX by its extension
    elif file_path.endswith(".docx"):
        return {"format": "docx", "text": extract_text_from_docx(file_path)}
    # Check if the file is a standard TXT file
    elif file_path.endswith(".txt"):
        # Open the text file in read mode with UTF-8 encoding
        with open(file_path, "r", encoding="utf-8") as f:
            return {"format": "txt", "text": f.read()}
    
    # Return empty text if the file format is unsupported
    return {"format": "unknown", "text": ""}
