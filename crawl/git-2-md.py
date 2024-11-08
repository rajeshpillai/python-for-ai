import os

def combine_files_to_markdown(folder_path, file_extension):
    # Check if folder exists
    if not os.path.isdir(folder_path):
        print("The provided folder path does not exist.")
        return
    
    # Get repository name from folder path
    repo_name = os.path.basename(os.path.normpath(folder_path))
    
    # Initialize markdown content
    markdown_content = f"# Combined Code Files ({file_extension}) for {repo_name}\n\n"
    
    # Walk through the directory to find files with the specified extension
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(f".{file_extension}"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    # Add each file's content to markdown with headers
                    relative_path = os.path.relpath(file_path, folder_path)
                    markdown_content += f"## {relative_path}\n\n```{file_extension}\n{file_content}\n```\n\n"
    
    # Save to markdown file
    output_file = f"{repo_name}.md"
    with open(output_file, "w", encoding='utf-8') as md_file:
        md_file.write(markdown_content)
    
    print(f"Markdown document saved as {output_file}")

# User input
folder_path = input("Enter the local folder path to the GitHub repository: ")
file_extension = input("Enter file extension to extract (e.g., cs, js, py): ")

# Combine files into markdown
combine_files_to_markdown(folder_path, file_extension)

