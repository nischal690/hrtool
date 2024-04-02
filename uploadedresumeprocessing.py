def process_uploaded_file(uploaded_file):
    # ... Your file processing logic ...
    # Read the file contents
    file_contents = uploaded_file.read()

    # Example: If it's a text-based resume
    resume_text = file_contents.decode('utf-8')  

    # Debug print statements
    print("File successfully accessed!")  
    print("File contents:", resume_text) 