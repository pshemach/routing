from pathlib import Path
import logging
import os

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: - %(message)s')

file_name = [
    'src/__init__.py',
    'src/tsp/__init__.py',
    'src/vrp/__init__.py',
    'src/matrix/__init__.py',
    'requirements.txt',
    'setup.py',
    'app.py',
    'demo.py',
]

for file in file_name:
    
    file_path = Path(file)
    filedir, filename = os.path.split(file_path)
    
    if filedir != '':
        os.makedirs(filedir, exist_ok=True)
        logging.info(f'Created Directory - {filedir}')
        
    if not os.path.exists(file_path) or os.path.getsize(file_path)==0:
        with open(file_path, "w") as f:
            logging.info(f'Created File - {file_path}')       
    else:
        logging.info(f"File Already exists - {file_path}")