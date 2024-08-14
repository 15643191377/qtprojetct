import chardet

with open('file.csv', 'rb') as f:
    result = chardet.detect(f.read())
    print(result['encoding'])
# 假设原始文件编码为GBK
with open('file.csv', 'r', encoding='GBK') as f:
    content = f.read()

# 将文件内容重新保存为UTF-8编码
with open('file_utf8.csv', 'w', encoding='UTF-8') as f:
    f.write(content)
