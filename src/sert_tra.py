import re

def get_english_blocks(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    english_blocks = []
    block_number = None
    english_pattern = re.compile(r'[a-zA-Z]')

    for i in range(len(lines)):
        if lines[i].strip().isdigit():
            block_number = lines[i].strip()
        elif '-->' in lines[i]:
            continue
        elif english_pattern.search(lines[i]):
            if block_number is not None:
                english_blocks.append(block_number)
                block_number = None

    return english_blocks

english_blocks = get_english_blocks('processed/merged_Racu vs Wyxi - ACW 1vs1 Tournament - Game 2_processed.srt')
print(english_blocks)
