import os

show_console = False

def rename_folders_with_py_file(directory):
    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)
        
        if os.path.isdir(folder_path):
            if any(file.endswith('.py') for file in os.listdir(folder_path)):
                new_folder_name = folder_name
                if "Python" not in folder_name:
                    new_folder_name = f"Python - {folder_name}"
                    new_folder_path = os.path.join(directory, new_folder_name)
                    os.rename(folder_path, new_folder_path)
                    print(f'Renamed "{folder_name}" to "{new_folder_name}"')
                
                move_folder_to_python_programming(directory, new_folder_name)

def move_folder_to_python_programming(directory, folder_name):
    python_programming_path = os.path.join(os.getcwd(), "Python Programming")
    if not os.path.exists(python_programming_path):
        os.mkdir(python_programming_path)

    folder_path = os.path.join(directory, folder_name)
    new_folder_path = os.path.join(python_programming_path, folder_name)
    os.rename(folder_path, new_folder_path)
    print(f'Moved "{folder_name}" to "Python Programming" folder')

if __name__ == "__main__":
    current_directory = os.getcwd()
    rename_folders_with_py_file(current_directory)
    if show_console:
        print("If you would like to disable this pop-up, edit variable show_console and make it False.")
        input()
