# TelegramMap
Using Telegram's Near-By feature to geolocalize people around the globe 🧭  
<br>
Only the first three letters of each name are kept. If the user has no name then the the first 4 characters of the username are used ('@' included)

# Installation
```bash
pip3 install scripts/requirements.txt
```

# Setup
Create a copy of ```.env.sample```, name it  ```.env``` and add your Telegram api information and you're ready to go!<br>
You can also tune other settings in the ```.env``` file to choose how to and where to execute the mapping.

# Usage
```bash
cd scripts
python3 app.py
```
The script will output the results in a temporary file (named based on the starting time) in the ```data``` directory (by default) and then merge that file with the file (<b>FILE_PATH</b>) specified in the ```.env```. <br>
The merging process combines multiple .csv files into a single one and removes possible duplicates (Points data is preserverd)
