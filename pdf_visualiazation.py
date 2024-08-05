import os
import re
import json
from PyPDF2 import PdfReader

def clean_text(text):
    # Удаление лишних пробелов и переносов строк
    text = re.sub(r'\s+', ' ', text)
    # Удаление номеров страниц (предполагается формат "X Статус документа: Конфиденциально")
    text = re.sub(r'\d+\s+Статус документа: Конфиденциально', '', text)
    # Удаление повторяющихся заголовков (пример)
    text = re.sub(r'(?:©.*?защищены\.)\s*', '', text)
    return text.strip()

def process_pdf(file_path):
    reader = PdfReader(file_path)
    processed_content = []

    for page in reader.pages:
        text = page.extract_text()
        cleaned_text = clean_text(text)
        if cleaned_text:  # Игнорируем пустые страницы
            processed_content.append(cleaned_text)

    return ' '.join(processed_content)

def process_directory(directory_path, output_file):
    processed_documents = []

    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory_path, filename)
            print(f"Обработка файла: {filename}")
            content = process_pdf(file_path)
            processed_documents.append({
                "filename": filename,
                "content": content
            })

    # Сохранение обработанных данных в JSON-файл
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_documents, f, ensure_ascii=False, indent=2)

    print(f"Обработка завершена. Результаты сохранены в {output_file}")

# Использование
input_directory = r'path'
output_file = 'processed_documents.json'
process_directory(input_directory, output_file)
