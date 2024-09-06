from InquirerPy import inquirer

url = inquirer.text(message="Enter a medium.com URL:").execute()
extensions = inquirer.select(message="Choose a file format:", choices=['pdf', 'md']).execute()
confirm = inquirer.confirm(message="Are you sure you want to proceed?", default=True).execute()