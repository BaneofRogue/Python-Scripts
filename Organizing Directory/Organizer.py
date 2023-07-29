import os
import shutil
import time
import re
from datetime import datetime

show_console = False
sort = True

class FileOrganizer:
    def __init__(self, directory):
        self.directory = directory
        self.invalid_folders = ["Shortcuts - Sorter", "Picture Files - Sorter", "MP4 Files - Sorter", "Text Files - Sorter", "FBX and OBJ Files - Sorter", "Blend Files - Sorter"]
        self.move_results = []
        self.total_changes = 0

    def check_invalid_folders(self):
        folders = os.listdir(self.directory)
        for folder in folders:
            if folder in self.invalid_folders:
                raise ValueError(f"Please rename the folder '{folder}' before running the process.")

    def create_folders(self):
        folders_to_create = self.invalid_folders
        for folder_name in folders_to_create:
            folder_path = os.path.join(self.directory, folder_name)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

    def organize_files(self):
        files = os.listdir(self.directory)
        for file in files:
            if os.path.isfile(file):
                file_extension = os.path.splitext(file)[1].lower()
                if file_extension == ".lnk" or file_extension == ".url":
                    self.move_file(file, self.invalid_folders[0])
                elif file_extension == ".png" or file_extension == ".jpg" or file_extension == ".jpeg" or file_extension == ".bmp" :
                    self.move_file(file, self.invalid_folders[1])
                elif file_extension == ".mp4":
                    self.move_file(file, self.invalid_folders[2])
                elif file_extension == ".txt":
                    self.move_file(file, self.invalid_folders[3])
                elif file_extension == ".fbx" or file_extension == ".obj":
                    self.move_file(file, self.invalid_folders[4])
                elif file_extension == ".blend" or file_extension == ".blend1":
                    self.move_file(file, self.invalid_folders[5])

    def move_file(self, file, destination_folder):
        src_path = os.path.join(self.directory, file)
        dest_path = os.path.join(self.directory, destination_folder, file)
        shutil.move(src_path, dest_path)
        self.move_results.append(f"{file} was moved from {self.directory} to {os.path.join(self.directory, destination_folder)}")
        self.total_changes += 1

    def save_move_results(self):
        print(f"Total changes made: {self.total_changes}")
        now = datetime.now()

        current_time = now.strftime("%H %M %S")
        current_date = now.strftime("%D").replace("/", " ")
        
        file_path = os.path.join(self.directory, f"Move File Results {current_date} {current_time}.txt")
        with open(file_path, "w", encoding="utf-8-sig") as file:
            for move_result in self.move_results:
                file.write(move_result + "\n")

        print(f"Move File Results saved to: {file_path}")

    def normalize_path(self, path):
        return path.strip().rstrip(os.sep)

    def revert_file_changes(self):
        file_nm = input("Please enter the file name without the .txt: ")
        move_results_file = os.path.join(self.directory, file_nm + ".txt")
        if not os.path.exists(move_results_file):
            print("Revert cannot be performed. The file was not found.")
            return

        with open(move_results_file, "r", encoding="utf-8-sig") as file:
            lines = file.readlines()

        for line in lines:
            match = re.search(r'(.+) was moved from (.+) to (.+)', line)
            if match:
                file_name, prev_location, next_location = match.groups()
                # Remove the BOM (if present) from the file name
                file_name = file_name.lstrip('\ufeff')
                dest_path = os.path.join(self.directory, prev_location)
                src_path = os.path.join(self.directory, next_location, file_name)

                dest_path = self.normalize_path(dest_path)
                src_path = self.normalize_path(src_path)

                if os.path.exists(src_path) and os.path.exists(dest_path):
                    shutil.move(src_path, dest_path)
                    print(f"Reverted: {file_name} was moved from {next_location} to {prev_location}")
                else:
                    print(f"Failed to revert: {file_name} was not found in {next_location}")
                    if os.path.exists(dest_path):
                        shutil.move(src_path, dest_path)
                        print(f"Reverted: {file_name} was moved from {next_location} to {prev_location}")
                    else:
                        print(f"Failed to create folder: {prev_location} does not exist")
            else:
                print(f"Invalid format in line: {line.strip()}")

if __name__ == "__main__":
    try:
        directory_path = os.getcwd()
        file_organizer = FileOrganizer(directory_path)
        if sort:
            #file_organizer.check_invalid_folders()
            file_organizer.create_folders()
            file_organizer.organize_files()
            file_organizer.save_move_results()
            print("File organization completed successfully!")
            print("DO NOT DELETE THIS FILE OR MAKE ANY CHANGES TO IT IF YOU WANT TO UNDO THIS")
        else:
            file_organizer.revert_file_changes()
            print("File movement reverted successfully!")
            
    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print("Invalid directory path. Please check and try again.")
        print(e)
