import os
from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from magic_pdf.config.enums import SupportedPdfParseMethod
from pathlib import Path

def process_pdf_to_markdown(pdf_path, output_dir):
    """
    处理单个PDF文件并转换为markdown
    """
    # 准备环境
    local_image_dir = os.path.join(output_dir, "images")
    local_md_dir = output_dir
    image_dir = "images"

    # 确保输出目录存在
    os.makedirs(local_image_dir, exist_ok=True)
    os.makedirs(local_md_dir, exist_ok=True)

    # 初始化写入器
    image_writer = FileBasedDataWriter(local_image_dir)
    md_writer = FileBasedDataWriter(local_md_dir)

    # 读取PDF文件
    reader = FileBasedDataReader("")
    pdf_bytes = reader.read(pdf_path)

    # 创建数据集实例
    ds = PymuDocDataset(pdf_bytes)

    # 获取文件名（不含扩展名）
    name_without_suff = os.path.splitext(os.path.basename(pdf_path))[0]

    # 处理PDF
    if ds.classify() == SupportedPdfParseMethod.OCR:
        infer_result = ds.apply(doc_analyze, ocr=True)
        pipe_result = infer_result.pipe_ocr_mode(image_writer)
    else:
        infer_result = ds.apply(doc_analyze, ocr=False)
        pipe_result = infer_result.pipe_txt_mode(image_writer)

    # 生成markdown文件
    md_file_path = os.path.join(local_md_dir, f"{name_without_suff}.md")
    pipe_result.dump_md(md_writer, f"{name_without_suff}.md", image_dir)
    
    return md_file_path

def combine_markdown_files(md_files, output_file):
    """
    合并多个markdown文件到一个文件中
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for md_file in md_files:
            # 添加文件名作为标题
            file_name = os.path.basename(md_file)
            outfile.write(f"\n# {os.path.splitext(file_name)[0]}\n\n")
            
            # 添加文件内容
            with open(md_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
                outfile.write(content)
                outfile.write("\n\n")  # 添加空行分隔不同文件的内容

def main():
    # 设置输入输出目录
    input_dir = "rag_kj/pdf_01"  # PDF文件目录
    temp_output_dir = "pdf_output"  # 临时markdown输出目录
    final_output_file = "local_rag_student/knowledge_base.txt"  # 最终合并后的知识库文件

    # 确保输出目录存在
    os.makedirs(temp_output_dir, exist_ok=True)
    os.makedirs(os.path.dirname(final_output_file), exist_ok=True)

    # 存储所有生成的markdown文件路径
    md_files = []

    # 遍历输入目录中的所有PDF文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            print(f"正在处理文件: {filename}")
            try:
                md_file = process_pdf_to_markdown(pdf_path, temp_output_dir)
                md_files.append(md_file)
                print(f"成功处理文件: {filename}")
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")

    # 合并所有markdown文件到知识库文件
    if md_files:
        print("正在合并markdown文件到知识库...")
        combine_markdown_files(md_files, final_output_file)
        print(f"知识库文件已生成: {final_output_file}")

if __name__ == "__main__":
    main() 