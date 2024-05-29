def get_timestamps_with_empty_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    timestamps_with_empty_text = []
    for i in range(len(lines)):
        if '-->' in lines[i]:
            timestamp = lines[i].strip()
            if i + 1 < len(lines) and lines[i + 1].strip() == '':
                if i - 1 >= 0 and lines[i - 1].strip().isdigit():
                    number = lines[i - 1].strip()
                    timestamps_with_empty_text.append((number, timestamp))

    return timestamps_with_empty_text

timestamps_with_empty_text = get_timestamps_with_empty_text('processed/merged_Racu vs Wyxi - ACW 1vs1 Tournament - Game 2_processed.srt')
print(timestamps_with_empty_text)