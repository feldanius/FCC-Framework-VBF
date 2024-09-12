import json

def read_json(json_file):
    """
    
    Args:
        json_file (str): Rute to JSON file.
    """
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        print(json.dumps(data, indent=4))
    except FileNotFoundError:
        print(f"{json_file} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding file {json_file}.")

# Rute JSON file
procDict = "/cvmfs/fcc.cern.ch/FCCDicts/FCCee_procDict_winter2023_IDEA.json"

# Read and print JSON structure
read_json(procDict)
