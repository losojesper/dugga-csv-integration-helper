from sys import argv
from urllib.request import Request, urlopen
import json
import requests
from random import randint


DUGGA_INTEGRATION_BASE_URL = 'https://dugga-integrations-prod.azurewebsites.net'
DUGGA_CSV_INTEGRATION_URL = f'{DUGGA_INTEGRATION_BASE_URL}/v1/upload/'


def encoding_ok(file_path):
    encoding_ok = 'no'
    with open(file_path, 'rb') as f:
        all_lines = list(f.readlines())
        print(len(all_lines))
        sample_lines = list()
        i = 0
        while i < 5 and len(all_lines) > 1:
            index = randint(0, len(all_lines) - 1)
            sample_lines.append(all_lines.pop(index))
            i += 1
        
        for line in sample_lines:
            print(line.decode('latin-1'))
        encoding_ok = input('Encoding check. Does this look alright? (yes/no): ')

    if encoding_ok == 'no':
        print('The encoding of the file has to be latin-1. If the output look strange your file might have the wrong encoding.')
        return False
    return True

def upload_file(file_path, token):
    with open(file_path, 'rb') as f:
        resp = requests.post(
            DUGGA_CSV_INTEGRATION_URL,
            files={'file.txt': f},
            headers={
                'Authorization': f'Token {token}',
                'Content-Type': 'multipart/form-data',
                'Content-Disposition': 'attachment; filename="filename.txt"'
            }
        )
        print(resp.text)


def get_argvs():
    try:
        token = argv[1]
        file = argv[2]
        return token, file
    except IndexError as e:
        print('''
This python script requires two inputs.\n
1. Your token that you can get from Dugga support.
2. The path to the CSV file you generated.\n
For example:
    python dugga_integration_helper.py jddsfop8uqtFAKEjwqmn34oipu ./dugga_test.csv\n
If you aren't sure about how the CSV should look like, just create an empty CSV and and use that one.
(Choose 'yes' when you get asked it the output looks ok, this will help you check the files encoding later)
Our backend will provide you with some feedback about the file's format.
        ''')
    return None, None


if __name__ == '__main__':
    token, file = get_argvs()
    
    if file and token:
        ok = encoding_ok(file)
        if ok:
            upload_file(file, token)
