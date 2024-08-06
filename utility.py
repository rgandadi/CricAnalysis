import json

def read_file_if_exists(filepath):
  try:
    with open(filepath, 'r') as file:
      content = file.read()
      return json.loads(content)
  except Exception as e:
    log (f"Exception {e} reading "+ filepath)
    return None

from datetime import datetime 
def get_iso_time():
  return datetime.datetime.now().isoformat()


def log(text):
  timestamp=get_iso_time()
  print(f'{timestamp} : '+text)
 
import datetime
import json
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") 
def create_json_file(file_path, content, append_timestamp=True):
    if (append_timestamp):
       file_path = file_path+ "_"+current_time
    
    if not file_path.endswith(".json"):
      file_path=file_path+".json"
    with open(file_path, "w") as outfile:
        json.dump(content, outfile, indent=4)
        print("Created "+file_path)

import os
def read_all_files(directory):
    master_data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if '.json' in file:
                file_path = os.path.join(root, file)
                print(file_path)
                with open(file_path, 'r') as f:
                    contents = json.load(f)
                    master_data[file.replace('.json','')]=contents

    return master_data

def read_all_files_and_save(directory, save_to_file=None):
    print(directory)
    master_data = read_all_files(directory)
    if save_to_file:
       create_json_file(save_to_file,master_data,False)

    return master_data



def create_json_file(file_path, content, append_timestamp=True):
    if (append_timestamp):
       file_path = file_path+ "_"+current_time
    
    if not file_path.endswith(".json"):
      file_path=file_path+".json"
    with open(file_path, "w") as outfile:
        json.dump(content, outfile, indent=4)
        print("Created "+file_path)


def get_config():
  config = read_file_if_exists("config/config.json")
  return config
