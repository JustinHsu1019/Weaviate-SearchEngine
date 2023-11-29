import re

def clean_html_tags(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 移除 HTML 標籤
    clean_content = re.sub(r'<[^>]+>', '', content)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(clean_content)

def main():
    input_file = 'Data/result.txt'
    output_file = 'Data/clean_output.txt'
    clean_html_tags(input_file, output_file)

if __name__ == "__main__":
    main()
