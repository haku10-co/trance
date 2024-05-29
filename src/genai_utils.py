import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
import logging
import json  # 追加

load_dotenv()  # .envファイルから環境変数を読み込む

# ロギングの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def configure_genai():
    try:
        api_key = os.getenv('API_KEY')  # 環境変数からAPIキーを取得
        genai.configure(api_key=api_key)
    except Exception as e:
        logging.error(f'Error in configuring Generative AI: {e}')

def read_prompt():
    try:
        with open('prompt.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        logging.error(f'Error in reading prompt file: {e}')
    return None

def generate_content(prompt, text_content, retries=3, delay=2):
    try:
        combined_prompt = f"{prompt}\n処理するテキストは以下の通り\n{text_content}"
        model_gemini_pro = genai.GenerativeModel('gemini-1.5-pro')
        request_data = {
            "prompt": combined_prompt,
            "generation_config": genai.types.GenerationConfig()
        }
        logging.info(f'Request JSON: {json.dumps(request_data, ensure_ascii=False, indent=2)}')  # JSON形式でログ出力

        for attempt in range(retries):
            try:
                logging.info(f'Attempt {attempt + 1}: Sending content to Gemini API')
                response = model_gemini_pro.generate_content(
                    combined_prompt, generation_config=genai.types.GenerationConfig()
                )
                logging.info(f'Response received: {response.text}')
                return response.text
            except Exception as e:
                logging.error(f'Error in generating content (attempt {attempt + 1}): {e}')
                time.sleep(delay)  # 再試行前に待機
    except Exception as e:
        logging.error(f'Error in generating content: {e}')
    return None