import os
import shutil
from git.repo.base import Repo

# Check that we're actually in the Spectre directory
if os.path.isfile("Spectre.py") == True:
    # Check that data exists. This could still error out if you don't have one of the other two, but if you don't, what are you doing
    if os.path.exists("data") == True:
        if os.path.exists("../SpectreData") == False:
            os.mkdir("../SpectreData")
            
        # Code to copy existing data files to a temporary directory
        shutil.move("data", "../SpectreData/data")
        shutil.move(".env", "../SpectreData")
        shutil.move("config.json", "../SpectreData")
        
        # Move to the parent directory (to create the new directory and later delete the old ones)
        os.chdir("../")
        os.rename("Spectre", "SpectreOld")
        os.mkdir("Spectre")
        
        # Clone the newest GitHub repo version
        Repo.clone_from("https://github.com/CooldudePUGS/Spectre", "Spectre")
        
        # Remove the "new" config file. There might be a better way to do this, but this works
        os.remove("Spectre/config.json")
        
        # Move the old data files from the temporary folder into the new Spectre folder
        shutil.move("SpectreData/data", "Spectre/data")
        shutil.move("SpectreData/.env", "Spectre")
        shutil.move("SpectreData/config.json", "Spectre")
        
        # Print that the system hasn't imploded yet
        print("Moved Spectre's data files succesfully!")
        print("Deleting old Spectre files...")
        
        # Remove temporary folders
        shutil.rmtree("SpectreOld")
        shutil.rmtree("SpectreData")
    else:
        print("Run the file inside the OLD Spectre directory that has your data!")
else:
    print("Run the file inside the Spectre directory!")
    
# Yes, this uses both shutil and os. I'm really not sure if this is fine or a "sin" to programmers. I did this because os wouldn't accept me moving the .env file properly.
