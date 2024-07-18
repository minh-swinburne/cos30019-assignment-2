import os

INPUT_DIR = 'data'
KB_KEYWORD = 'TELL'
QUERY_KEYWORD = 'ASK'

def parse(file_name):
    file_path = os.path.join(INPUT_DIR, file_name)
    with open(file_path, 'r') as file:
        content = file.read()
        tell_index = content.index(KB_KEYWORD)
        ask_index = content.index(QUERY_KEYWORD)
        kb = content[tell_index + len(KB_KEYWORD) : ask_index].strip()
        query = content[ask_index + len(QUERY_KEYWORD):].strip()


if __name__ == '__main__':
    parse('test_HornKB.txt')