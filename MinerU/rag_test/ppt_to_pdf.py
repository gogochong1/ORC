import os
from pptx import Presentation
from pdf2docx import Converter
import comtypes.client
import sys

def ppt_to_pdf(input_path, output_path):
    """
    将PPT文件转换为PDF
    :param input_path: PPT文件路径
    :param output_path: PDF输出路径
    """
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 使用comtypes进行转换
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        powerpoint.Visible = True
        
        # 打开PPT文件
        deck = powerpoint.Presentations.Open(input_path)
        
        # 保存为PDF
        deck.SaveAs(output_path, 32)  # 32 表示PDF格式
        deck.Close()
        
        # 关闭PowerPoint
        powerpoint.Quit()
        
        print(f"成功转换: {input_path} -> {output_path}")
    except Exception as e:
        print(f"转换失败 {input_path}: {str(e)}")

def process_directory(input_dir, output_dir):
    """
    处理目录中的所有PPT文件
    :param input_dir: 输入目录
    :param output_dir: 输出目录
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith(('.ppt', '.pptx')):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + '.pdf'
            output_path = os.path.join(output_dir, output_filename)
            
            ppt_to_pdf(input_path, output_path)

if __name__ == "__main__":
    input_dir = "rag_kj"
    output_dir = "pdf_output"
    
    process_directory(input_dir, output_dir)
    print("所有文件转换完成！") 