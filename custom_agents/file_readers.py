from docx import Document
from agents import Agent, function_tool

@function_tool
def read_docx_document(path: str) -> str:
    """Extract text content from a Word document (.docx)."""
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

@function_tool
def read_text_file(path: str) -> str:
    """Extract text content from a plain text file (.txt)."""
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

file_reader_triage_agent = Agent(
    name="File Reader Triage Agent",
    instructions="""
    Analyze the provided file path and read its contents based on the file extension:
    
    1. Extract the file extension from the path
    2. Use appropriate tool based on file type:
       - .docx files → use read_docx_document
       - .txt files → use read_text_file
    3. For unsupported file types, return an error message
    
    Important: Return the raw file content exactly as read, without any modifications, 
    summaries, or augmentations.
    
    Input: File path as string
    Output: Unmodified text content from the file
    """,
    tools=[read_docx_document, read_text_file],
)