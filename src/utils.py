import os


def write_to_file(content: str, folder_name: str, filename: str):
    """
    Write the provided content to a file in the specified folder. If the file already exists, it will be overwritten.

    Parameters:
        content (str): The content to be written to the file.
        folder_name (str): The name of the folder where the file will be saved.
        filename (str): The name of the file to write the content to.

    Returns:
        str: A message indicating the content was successfully written and the path to the file.
    """
    directory = f"artifacts/{folder_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    return f"Content successfully written to {file_path}."
