import os
from PyPDF2 import PdfReader
from docx import Document

def read_pdf(file_path):
    """
    读取PDF文件并返回文本内容
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"读取PDF文件时出错: {str(e)}"

def read_docx(file_path):
    """
    读取Word文档并返回文本内容
    """
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"读取Word文档时出错: {str(e)}"

def read_document(file_path):
    """
    根据文件扩展名自动选择读取方法
    """
    if not os.path.exists(file_path):
        return "文件不存在"
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.pdf':
        return read_pdf(file_path)
    elif file_ext in ['.docx', '.doc']:
        return read_docx(file_path)
    else:
        return "不支持的文件格式"

if __name__ == "__main__":
    # 设置基础目录
    base_dir = r"D:\QianYi\ORC"
    
    # 获取目录下的所有文件
    files = os.listdir(base_dir)
    
    # 显示可用的文档
    print("可用的文档：")
    for i, file in enumerate(files, 1):
        if file.lower().endswith(('.pdf', '.doc', '.docx')):
            print(f"{i}. {file}")
    
    # 让用户选择要读取的文件
    try:
        choice = int(input("\n请输入要读取的文件编号: "))
        if 1 <= choice <= len(files):
            selected_file = files[choice-1]
            file_path = os.path.join(base_dir, selected_file)
            print(f"\n正在读取文件: {selected_file}")
            content = read_document(file_path)
            print("\n文档内容:")
            print(content)
        else:
            print("无效的选择")
    except ValueError:
        print("请输入有效的数字") 