import os
import subprocess

os.environ['KAGGLE_USERNAME'] = "januarymagori"
os.environ['KAGGLE_KEY'] = "bc6ce7bdd037b4b7edf3c329d842f4f3"


download_cmd = "kaggle datasets download -d saurabhshahane/mango-varieties-classification --unzip"
process = subprocess.Popen(download_cmd.split(), stdout=subprocess.PIPE)
output, error = process.communicate()


# create_folder = "mkdir datasets/birds-species"
# process = subprocess.Popen(create_folder.split(), stdout=subprocess.PIPE)
# output, error = process.communicate()

# cp_folder = "cp -R train/ datasets/birds-species/images/"
# process = subprocess.Popen(cp_folder.split(), stdout=subprocess.PIPE)
# output, error = process.communicate()
