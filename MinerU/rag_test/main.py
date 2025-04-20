from student_rag import StudentRag
from kb import Kb
import os
from pathlib import Path

def create_knowledge_base(input_dir, output_file):
    """从输入目录创建知识库文件"""
    print(f"正在从目录 {input_dir} 创建知识库...")
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 遍历目录中的所有文件
        for filename in os.listdir(input_dir):
            filepath = os.path.join(input_dir, filename)
            if not os.path.isfile(filepath):
                continue
                
            print(f"处理文件: {filename}")
            
            # 根据文件类型提取文本
            try:
                if filename.lower().endswith('.pdf'):
                    content = Kb.extract_text_from_pdf(filepath)
                elif filename.lower().endswith('.docx'):
                    content = Kb.extract_text_from_docx(filepath)
                else:
                    print(f"跳过不支持的文件类型: {filename}")
                    continue
                
                # 写入文件名作为标题
                outfile.write(f"\n# {filename}\n\n")
                outfile.write(content)
                outfile.write("\n\n")
                
                print(f"已处理文件: {filename}")
                
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")
                continue

def process_markdown_files(input_dir, output_dir, rag):
    """处理输入目录中的所有markdown文件"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # 确保输出目录存在
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 遍历所有markdown文件
    for md_file in input_path.glob('*.md'):
        print(f"处理文件: {md_file}")
        
        # 读取markdown文件内容
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 处理题目
        answer = rag.process_question(content)
        
        # 生成输出文件路径
        output_file = output_path / f"{md_file.stem}_答案.docx"
        
        # 保存结果
        rag.save_to_docx(content, answer, str(output_file))
        print(f"已生成答案文件: {output_file}")

def main():
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)  # 上一级目录
    
    # 配置参数
    model = "qwq:latest"  # 使用qwq模型
    kb_filepath = os.path.join(current_dir, "knowledge_base.txt")  # 知识库文件路径
    pdf_dir = os.path.join(base_dir, "rag_kj", "pdf_01")  # PDF文件目录
    pdf_output_dir = os.path.join(base_dir, "pdf_output")  # PDF输出目录
    md_output_dir = os.path.join(base_dir, "md_output")    # Markdown输出目录
    
    # 创建知识库文件
    create_knowledge_base(pdf_dir, kb_filepath)
    print(f"知识库文件已创建: {kb_filepath}")
    
    # 初始化RAG系统
    rag = StudentRag(model, kb_filepath)
    
    # 处理所有markdown文件
    process_markdown_files(pdf_output_dir, md_output_dir, rag)

if __name__ == "__main__":
    main() 