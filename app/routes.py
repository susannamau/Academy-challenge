from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint, send_from_directory, jsonify, abort
import json
import random
import string
import os
#from .models import Account
from huggingface_hub import InferenceClient
import pandas as pd
from docx import Document
import pypandoc
import fitz
import magic

with open('/Users/susannamau/Dev/BPER/Challenge/config.json', 'r') as config_file:
    config = json.load(config_file)

main = Blueprint('main', __name__)

@main.route('/')
def welcome():
    return render_template("task_choice.html")



@main.route('/task_choice', methods=['POST', 'GET'])
def task_choice():
    if request.form.get('submit_button') == 'Question answering':
        files = get_files()
        return render_template("quest_ans.html", files=files)
    elif request.form.get('submit_button') == 'Documents differences finder':
        return render_template("doc_diffs.html")
    else:
        print("Error")

@main.route('/quest_ans', methods=['POST', 'GET'])
def quest_ans():
    files = get_files()
    return render_template("quest_ans.html", files=files)


def get_files():
    files = os.listdir(config['UPLOAD_FOLDER'])
    files = [f for f in files if os.path.isfile(os.path.join(config['UPLOAD_FOLDER'], f))]
    return files



def allowed_file(filename):
    if filename.rsplit('.', 1)[1].lower() in config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False
    


@main.route('/upload_qa', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Nessun file selezionato", 400

    file = request.files['file']
    if file.filename == '':
        return "Nome file non valido", 400

    if file and allowed_file(file.filename):
        os.makedirs(config['UPLOAD_FOLDER'], exist_ok=True)
        file_path = os.path.join(config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        files = get_files()
        return render_template("quest_ans.html", files=files)
    
    if allowed_file(file.filename) == False:
        return "Estensione file non valida", 400
    

    
@main.route('/delete_file', methods=['POST'])
def delete_file():
    data = request.get_json()
    filename = data['filename']
    file_path = os.path.join(config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify(success=True)
    return jsonify(success=False)



@main.route('/<filename>', methods=['POST', 'GET'])
def download_file(filename):
    file_path = os.path.join(config['UPLOAD_FOLDER'], filename)

    print(f"Verifica percorso file: {file_path}") 
    if not os.path.exists(file_path):
        print(f"File non trovato: {file_path}")

    return send_from_directory(config['UPLOAD_FOLDER'], filename)



def get_files_content(folder):
    files_content = []
    files = os.listdir(folder)
    for file in [f for f in files if os.path.isfile(os.path.join(folder, f))]:
        print("File: ", f"{folder}/{file}")
        ext = file.rsplit('.', 1)[1].lower()
        if ext == "txt":
            with open(f'{folder}/{file}', 'r') as file:
                content = file.read()
        elif ext == "csv":
            content = list(pd.read_csv(f'{folder}/{file}'))
        elif ext == "docx":
            doc = Document(f'{folder}/{file}')
            content = ""
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"
        elif ext == "doc":
            content = pypandoc.convert_file(f'{folder}/{file}', to="plain")
        elif ext == "pdf":
            pdf_document = fitz.open(f"{folder}/{file}")
            content = ""
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                content += page.get_text()
        else:
            content = magic.Magic(mime=True)
            content = content.from_file(f"{folder}/{file}")
        files_content.append(content)
    return files_content


@main.route('/ask', methods=['POST'])
def ask_question():
    files_content = get_files_content(config['UPLOAD_FOLDER'])

    data = request.get_json()
    question = data.get('question')

    hf_token = config["HF_TOKEN"]
    hf_client = InferenceClient(token=hf_token)
    llm_model = config["LLM"]

    messages=[
    {"role": "system", "content": "Sei un assistente che risponde in Italiano alle domande dell'utente consultando i file a disposizione."},
    {"role": "system", "content": f"Date le seguenti informazioni: {files_content}"},
    {"role": "user", "content": question}
    ]

    completion = hf_client.chat_completion(model=llm_model, messages=messages, max_tokens=500)
    response = completion.choices[0].message.content
    
    if response != None:
        return jsonify({'answer': response})
    else:
        return jsonify({'answer': 'There was an error processing your question.'})

@main.route('/upload_diff', methods=['POST'])
def upload_file_diff():
    if 'file' not in request.files:
        return "Nessun file selezionato", 400

    file = request.files['file']
    if file.filename == '':
        return "Nome file non valido", 400

    if file and allowed_file(file.filename):
        os.makedirs(config['COMP_FOLDER'], exist_ok=True)
        file_path = os.path.join(config['COMP_FOLDER'], file.filename)
        file.save(file_path)
        files = get_files()
        return render_template("doc_diffs.html", files=files)
    
    if allowed_file(file.filename) == False:
        return "Estensione file non valida", 400

@main.route('/doc_diffs', methods=['POST'])
def doc_diffs():
    data = request.get_json()
    filename1 = data['filename1']
    filename2 = data['filename2']
    file_path1 = os.path.join(config['COMP_FOLDER'], filename1)
    file_path2 = os.path.join(config['COMP_FOLDER'], filename2)

    if not os.path.exists(file_path1) or not os.path.exists(file_path2):
        return jsonify({'error': 'One or both files do not exist.'})

    ext1 = filename1.rsplit('.', 1)[1].lower()
    ext2 = filename2.rsplit('.', 1)[1].lower()

    content1 = get_files_content(file_path1)
    content2 = get_files_content(file_path2)

    hf_token = config["HF_TOKEN"]
    hf_client = InferenceClient(token=hf_token)
    llm_model = config["LLM"]

    messages=[
    {"role": "system", "content": "Trova le differenze tra due documenti."},
    {"role": "system", "content": f"Il primo documento è: {content1}"},
    {"role": "system", "content": f"Il secondo documento è: {content2}"},
    {"role": "user", "content": "Restituiscimi una lista ordinata delle differenze tra i due documenti."}
    ]

    completion = hf_client.chat_completion(model=llm_model, messages=messages, max_tokens=500)
    response = completion.choices[0].message.content

    if response:
        return jsonify({'differences': response})
    else:
        return jsonify({'error': 'There was an error processing your request.'})

