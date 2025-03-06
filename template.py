from pathlib import Path
import logging
import os

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: - %(message)s')

# file_name = [
#     'src/__init__.py',
#     'src/tsp/__init__.py',
#     'src/vrp/__init__.py',
#     'src/matrix/__init__.py',
#     'requirements.txt',
#     'setup.py',
#     'app.py',
#     'demo.py',
# ]

file_name = [
    'frontend/main.py',
    'frontend/config.py',
    'frontend/pages/upload_data.py',
    'frontend/pages/update_vehicles.py',
    'frontend/pages/update_shops.py',
    'frontend/pages/restricted_paths.py',
    'frontend/pages/solve_vrp.py',
    'frontend/pages/solve_tsp.py',
    'frontend/pages/view_data.py',
    'frontend/pages/rest_data.py',
    'frontend/utils/api_helper.py',
    'frontend/utils/ui_helper.py',
    'frontend/__init__.py',
    'frontend/pages/__init__.py'
    'frontend/utils/__init__.py'
    
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