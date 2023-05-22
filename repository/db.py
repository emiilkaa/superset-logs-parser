import os.path

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
with open(config_path, encoding='utf-8') as config_file:
    config = yaml.safe_load(config_file)

hostname = config['hostname']
username = config['username']
password = config['password']
db_name = config['db_name']
url = f'postgresql://{username}:{password}@{hostname}/{db_name}'

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()
