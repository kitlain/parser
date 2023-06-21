import os

def remove_duplicate_lines(filename):
    seen_lines = set()
    temp_filename = filename + '.tmp'

    with open(filename, 'r') as file, open(temp_filename, 'w') as temp_file:
        for line in file:
            line = line.strip()
            if line not in seen_lines:
                seen_lines.add(line)
                temp_file.write(line + '\n')

    os.remove(filename)
    os.rename(temp_filename, filename)

filename = 'links.txt'
remove_duplicate_lines(filename)

print("Повторяющиеся строки удалены.")
