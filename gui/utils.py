from typing import List
import streamlit as st
import pandas as pd
import json
import requests
import os
from tqdm import tqdm
from urllib.parse import urlencode

with open('interface.json') as f:
    config = json.load(f)

    
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    # Get the total file size from the response headers
    file_size = int(response.headers.get('Content-Length', 100))

    # Create a progress bar with the total file size
    progress_bar = st.progress(0)
    status_text = st.empty()

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

                # Update the progress bar
                progress_bar.progress(int(f.tell() / file_size))
                
                # Update the status text
                status_text.text(f"Downloaded {f.tell() / (1024*1024):.2f} MB out of {file_size / (1024*1024):.2f} MB")

def url_or_file(path):
    if path.startswith(('http://', 'https://', 'ftp://')):
        return 'URL'
    elif os.path.isfile(path):
        return 'File'
    else:
        return 'Unknown'

def load_to_df(path:str, file_format:str) -> pd.DataFrame:
    if file_format == ".csv":
        data = pd.read_csv(path)
    elif file_format == ".parquet":
        data = pd.read_parquet(path)
    else:
        st.sidebar.warning(f"{file_format} is not expected")
    return data


def upload_form(name:str, columns:List[str], file_format:str='.csv') -> pd.DataFrame:
    user_query = st.text_input(label=f"{config['welcome_page_text_prefix']} {name.lower()}", key=f"{name}_form")
    if st.button('Search', key=f"{name}_button"):
        if user_query:
            link_type = url_or_file(user_query)
            if link_type == "File":
                data = load_to_df(user_query, file_format)
            elif link_type == "URL":
            
                # download_file(user_query, name+file_format)
                if not os.path.isdir(config["download_folder"]):
                    os.mkdir(config["download_folder"])

                download_file_from_google_drive(
                    user_query, os.path.join(config["download_folder"], name+file_format)
                    )
                
                data = load_to_df(os.path.join(config["download_folder"], name+file_format), file_format)
            else: 
                st.sidebar.warning(f"wrong link")
                return
            
            if set(data.columns) == set(columns):
                st.sidebar.success(f"{name} {config['emojies']['done']}")
            else:
                st.sidebar.warning(f"{name} {config['warning']['wrong_columns_warning_p1']} {config['required_columns'][name]} {'wrong_columns_warning_p1'} {list(data.columns)} ")
        
def load_from_url(url:str, path:str) -> None:
    r = requests.get(url, allow_redirects=True)
    open(path, 'wb').write(r.content)


def empty_page():
    st.title(config["missing_data_message"])