from docling.document_converter import DocumentConverter

converter = DocumentConverter()

def load_document(file_path):
    result = converter.convert(file_path)
    return result.document.export_to_markdown()