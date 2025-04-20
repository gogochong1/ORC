import os
from docx import Document
import win32com.client
import pythoncom
import time

# 配置路径
DOC_DIR = "doc"  # 源文档文件夹
PDF_OUTPUT_DIR = "pdf_change"  # PDF输出文件夹

def docx_to_pdf(docx_path, pdf_path):
    """
    将docx文件转换为pdf
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(docx_path):
            print(f"错误：文件不存在 - {docx_path}")
            return False
            
        # 初始化COM
        pythoncom.CoInitialize()
        
        # 创建Word应用程序实例
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        
        # 打开文档
        doc = word.Documents.Open(os.path.abspath(docx_path))
        
        # 保存为PDF
        doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)  # 17代表PDF格式
        
        # 关闭文档和Word应用程序
        doc.Close()
        word.Quit()
        
        return True
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return False
    finally:
        # 确保清理COM对象
        pythoncom.CoUninitialize()

def process_doc_folder():
    """
    处理doc文件夹中的所有docx文件
    """
    # 确保源目录存在
    if not os.path.exists(DOC_DIR):
        print(f"错误：源文件夹不存在 - {DOC_DIR}")
        return
    
    # 确保输出目录存在
    if not os.path.exists(PDF_OUTPUT_DIR):
        os.makedirs(PDF_OUTPUT_DIR)
        print(f"创建输出文件夹: {PDF_OUTPUT_DIR}")
    
    # 获取doc文件夹中的所有docx文件
    for filename in os.listdir(DOC_DIR):
        if filename.endswith('.docx') or filename.endswith('.doc'):
            # 构建完整的文件路径
            docx_path = os.path.join(DOC_DIR, filename)
            pdf_filename = os.path.splitext(filename)[0] + '.pdf'
            pdf_path = os.path.join(PDF_OUTPUT_DIR, pdf_filename)
            
            print(f"正在转换: {filename} -> {pdf_filename}")
            
            # 转换文件
            if docx_to_pdf(docx_path, pdf_path):
                print(f"转换成功: {filename}")
            else:
                print(f"转换失败: {filename}")
            
            # 添加短暂延迟，避免COM对象冲突
            time.sleep(1)

if __name__ == "__main__":
    process_doc_folder() 