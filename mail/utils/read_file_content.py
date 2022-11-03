def read_file_content(filename: str) -> str:
    with open(filename, 'r') as content_file:
        content = content_file.read()
    return content
