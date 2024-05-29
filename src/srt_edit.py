import os
import re

def process_all_srt_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.srt'):
            file_path = os.path.join(directory, filename)
            remove_code_block_lines(file_path)  # 追加
            insert_blank_lines_between_blocks(file_path)

def insert_blank_lines_between_blocks(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin1') as file:
            lines = file.readlines()

    blocks_with_multiple_timestamps = detect_blocks_with_multiple_timestamps(lines)
    offset = 0

    for block in blocks_with_multiple_timestamps:
        for i in range(len(block['timestamps']) - 1):
            # タイムスタンプの2行下に空行を挿入するために [0] を使用し、2を加える
            insert_position = block['timestamps'][i][0] + 2 + offset
            lines.insert(insert_position, '\n')
            offset += 1

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def detect_blocks_with_multiple_timestamps(lines):
    timestamp_pattern = re.compile(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}')
    blocks = []
    current_block = {'text_lines': 0, 'timestamps': []}

    for i, line in enumerate(lines):
        if timestamp_pattern.match(line.strip()):
            current_block['timestamps'].append((i, line.strip()))
        elif line.strip():
            current_block['text_lines'] += 1
        else:
            if current_block['text_lines'] >= 4 and len(current_block['timestamps']) >= 2:
                blocks.append(current_block)
            current_block = {'text_lines': 0, 'timestamps': []}

    # Check last block
    if current_block['text_lines'] >= 4 and len(current_block['timestamps']) >= 2:
        blocks.append(current_block)

    return blocks

def remove_code_block_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin1') as file:
            lines = file.readlines()

    lines = [line for line in lines if not line.strip().startswith('```')]

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

# ディレクトリ内のすべてのsrtファイルに対して処理を適用
process_all_srt_files('/Users/kamehaku/Downloads/srtCOnv 2/processed')