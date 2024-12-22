def convert_to_utf8(file_path):
    # Read the file with UTF-
    with open(file_path, "r", encoding="utf-16") as f:
        content = f.read()

    # Write the content back with UTF-8 encoding
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


# Replace 'requirements.txt' with the path to your file
convert_to_utf8("../requirements.txt")
