import json
import os

def load_json(filepath):
    """Opens file and returns JSON data"""

    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def basename(filename):
    """Strips the path and file extension(s) from a filename.

        Python's standard basename() retains the extension.
    """
    try:
        start = filename.rindex('/') + 1
    except ValueError:
        start = 0

    try:
        end = filename.index('.')
    except ValueError:
        end = None

    return filename[start:end]

def loop_json_genomes(data, test):

    i = 0
    
    while True:
        try:
            strain = data["Results"][i]["Strain"]
            genes = data["Results"][i]["TestResults"][test]
            
            yield strain, genes
            
            i += 1
        
        except IndexError:
            break

def get_jsons(json_dirs):

    jsons = []
    
    for path in json_dirs:

        if '.json' in path:
            jsons.append(os.path.abspath(path))

        else:
        
            jpaths = [os.path.join(path, x) for x in
                        os.listdir(path) if '.json' in x]

            jsons.extend(jpaths)

    return jsons