import os
import re

def detect_and_merge_short_blocks(srt_file):
    with open(srt_file, 'r', encoding='utf-8') as file:
        content = file.read()

    blocks = re.split(r'\n\n', content)
    merged_blocks = []
    i = 0
    block_number = 1

    while i < len(blocks) - 1:
        current_block = blocks[i].strip().split('\n')
        next_block = blocks[i + 1].strip().split('\n')

        if len(current_block) >= 3 and len(next_block) >= 3:
            current_timestamps = current_block[1]
            next_timestamps = next_block[1]
            current_start, current_end = re.findall(r'(\d+:\d+:\d+,\d+)', current_timestamps)
            next_start, next_end = re.findall(r'(\d+:\d+:\d+,\d+)', next_timestamps)
            current_duration = convert_to_seconds(current_end) - convert_to_seconds(current_start)

            if current_duration < 2:
                current_subtitle_text = ' '.join(current_block[2:])
                next_subtitle_text = ' '.join(next_block[2:])
                merged_subtitle_text = current_subtitle_text + ' ' + next_subtitle_text
                merged_block = [str(block_number), f"{current_start} --> {next_end}", merged_subtitle_text]
                merged_blocks.append('\n'.join(merged_block))
                block_number += 1
                i += 2
            else:
                current_block[0] = str(block_number)
                merged_blocks.append('\n'.join(current_block))
                block_number += 1
                i += 1
        else:
            current_block[0] = str(block_number)
            merged_blocks.append('\n'.join(current_block))
            block_number += 1
            i += 1

    if i == len(blocks) - 1:
        last_block = blocks[i].strip().split('\n')
        last_block[0] = str(block_number)
        merged_blocks.append('\n'.join(last_block))

    return '\n\n'.join(merged_blocks)

def convert_to_seconds(timestamp):
    parts = timestamp.replace(',', ':').split(':')
    if len(parts) == 4:
        hours, minutes, seconds, milliseconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + float(milliseconds) / 1000
    elif len(parts) == 3:
        hours, minutes, seconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    else:
        raise ValueError(f"Invalid timestamp format: {timestamp}")

def process_srt_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    prepreprocess_dir = os.path.join(script_dir, "..", "prepreprocess")
    preprocess_dir = os.path.join(script_dir, "..", "preprocess")

    # prepreprocessディレクトリが存在しない場合は作成
    os.makedirs(prepreprocess_dir, exist_ok=True)
    os.makedirs(preprocess_dir, exist_ok=True)

    for srt_file in os.listdir(prepreprocess_dir):
        if srt_file.endswith(".srt"):
            srt_file_path = os.path.join(prepreprocess_dir, srt_file)
            merged_srt = detect_and_merge_short_blocks(srt_file_path)
            output_file = os.path.join(preprocess_dir, f"merged_{srt_file}")
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(merged_srt)
            print(f"結合されたSRTファイル {srt_file} が生成されました。")
            os.remove(srt_file_path)  # 処理が完了したファイルを削除