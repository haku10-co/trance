import os
import time
from genai_utils import configure_genai, read_prompt, generate_content
from srt_edit import process_all_srt_files  # 追加

def process_text_files(update_progress=None):
    configure_genai()
    prompt = read_prompt()

    if prompt:
        preprocess_folder = 'preprocess'
        output_folder = 'processed'

        os.makedirs(preprocess_folder, exist_ok=True)
        txt_files = [file for file in os.listdir(preprocess_folder) if file.endswith('.srt')]

        output_file_paths = []  # 出力ファイルのパスを保存するリスト

        for txt_file in txt_files:
            input_file_path = os.path.join(preprocess_folder, txt_file)
            try:
                with open(input_file_path, 'r', encoding='utf-8') as file:
                    text_lines = file.readlines()
            except UnicodeDecodeError:
                try:
                    with open(input_file_path, 'r', encoding='latin1') as file:
                        text_lines = file.readlines()
                except Exception as e:
                    print(f'Error reading file {input_file_path}: {e}')
                    continue
            except Exception as e:
                print(f'Error processing file {input_file_path}: {e}')
                continue

            chunk_size = 100
            text_chunks = [text_lines[i:i + chunk_size] for i in range(0, len(text_lines), chunk_size)]

            generated_content = ""
            for i, chunk in enumerate(text_chunks, start=1):
                chunk_content = "".join(chunk)
                generated_chunk = generate_content_with_timeout(prompt, chunk_content)
                if generated_chunk:
                    generated_content += generated_chunk + "\n"
                    print(f'処理成功: {txt_file} - {i}ループ目')
                    if update_progress:
                        update_progress((i / len(text_chunks)) * 100)  # 進捗を更新
                else:
                    print(f'処理失敗: {txt_file} - {i}ループ目')
                    generated_chunk = generate_content_with_timeout(prompt, chunk_content)  # 再試行
                    if generated_chunk:
                        generated_content += generated_chunk + "\n"
                        print(f'再試行成功: {txt_file} - {i}ループ目')
                    else:
                        print(f'再試行失敗: {txt_file} - {i}ループ目')

            if generated_content:
                os.makedirs(output_folder, exist_ok=True)
                output_file_name = f'{os.path.splitext(txt_file)[0]}_processed.srt'
                output_file_path = os.path.join(output_folder, output_file_name)
                output_file_path = os.path.abspath(output_file_path)  # 絶対パスに変換
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(generated_content)
                output_file_paths.append(output_file_path)
                print(f'Generated content written to {output_file_path}')

            # 処理が完了した元のファイルを削除
            os.remove(input_file_path)
            print(f'{input_file_path} が削除されました。')

        # すべてのループが完了した後に SRT 編集処理を実行
        process_all_srt_files(output_folder)

        return output_file_paths

def generate_content_with_timeout(prompt, text_content, retries=3, delay=2, timeout=60):
    for attempt in range(retries):
        try:
            start_time = time.time()
            response = generate_content(prompt, text_content)
            while response is None and (time.time() - start_time) < timeout:
                time.sleep(1)
                response = generate_content(prompt, text_content)
            if response:
                return response
            else:
                print(f'応答なし: {attempt + 1}回目の試行')
        except Exception as e:
            print(f'Error in generating content (attempt {attempt + 1}): {e}')
            time.sleep(delay)
    return None