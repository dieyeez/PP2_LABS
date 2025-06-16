import os

def list_contents(path):
    if not os.path.exists(path):
        print("The specified path does not exist.")
        return
    
    all_items = os.listdir(path)
    
    directories = [item for item in all_items if os.path.isdir(os.path.join(path, item))]
    files = [item for item in all_items if os.path.isfile(os.path.join(path, item))]
    
    print("\nDirectories:")
    print(directories if directories else "No directories found.")
    
    print("\nFiles:")
    print(files if files else "No files found.")
    
    print("\nAll items:")
    print(all_items if all_items else "The directory is empty.")

path = input("Enter the path: ")
list_contents(path)
