import requests

def fetch_and_save_content(url, output_file):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content.decode('utf-8')
        content = content.replace("\r\n", "")
        content = content.replace("\n", "")
        content = content.replace("\r", "")
        content = content.replace(" ", "")
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write("此案網址: " + url + "\n" + content + "\nI_am_so_handsome\n")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(f"Error fetching {url}\nI_am_so_handsome\n")

def main():
    input_file = 'Data/output.txt'
    output_file = 'Data/result.txt'

    with open(input_file, 'r', encoding='utf-8') as file:
        urls = file.readlines()

    for url in urls:
        fetch_and_save_content(url.strip(), output_file)

if __name__ == "__main__":
    main()
