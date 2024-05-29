import os
import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数からAPIキーを読み込む
load_dotenv()
api_key = os.getenv('API_KEY')

# APIキーの設定
genai.configure(api_key=api_key)

# プロンプトの読み込み
def read_prompt(file_path='prompt.txt'):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# コンテンツ生成
def generate_content(prompt):
    model_gemini_pro = genai.GenerativeModel('gemini-1.5-flash')
    response = model_gemini_pro.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig()
    )
    return response.text

if __name__ == "__main__":
    prompt = read_prompt()  # 'prompt.txt'からプロンプトを読み込む
    if prompt:
        generated_text = generate_content(prompt)
        print(generated_text)
    else:
        print("プロンプトの読み込みに失敗しました。")
