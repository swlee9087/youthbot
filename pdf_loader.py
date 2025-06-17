import os
from pdfminer.high_level import extract_text

def load_pdfs_from_local_repo():
    repo_path = "./data"  # 또는 GitHub 클론한 경로
    pdf_files = [f for f in os.listdir(repo_path) if f.endswith(".pdf")]
    
    docs = []
    for pdf_file in pdf_files:
        path = os.path.join(repo_path, pdf_file)
        text = extract_text(path)
        docs.append(text)
    
    return docs
