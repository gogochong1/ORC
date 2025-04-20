import os
import re

def process_questions(input_file, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分割题目
    questions = re.split(r'\n\s*\d+、', content)[1:]  # 跳过第一个空元素
    
    # 创建单个输出文件
    output_file = os.path.join(output_dir, 'all_questions.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        # 处理每个题目
        for i, question in enumerate(questions, 1):
            # 提取题目内容和选项
            lines = question.strip().split('\n')
            question_text = lines[0].strip()
            options = []
            answer = None
            
            # 判断题目类型
            if '（' in question_text and '）' in question_text:  # 选择题
                # 处理选项和答案
                for line in lines[1:]:
                    line = line.strip()
                    if not line:
                        continue
                    if 'A、' in line:
                        options.append(line)
                    # 提取答案
                    match = re.search(r'（\s*([A-D])\s*）', question_text)
                    if match:
                        answer = match.group(1)
                
                # 写入选择题
                f.write(f"第{i}题：\n")
                f.write("题目：\n")
                f.write(f"{question_text}\n\n")
                for option in options:
                    f.write(f"{option}\n")
                f.write(f"选项：{answer}\n")
            
            elif '___' in question_text:  # 填空题
                # 写入填空题
                f.write(f"第{i}题：\n")
                f.write("题目：\n")
                f.write(f"{question_text}\n\n")
            
            else:  # 简答题
                # 写入简答题
                f.write(f"第{i}题：\n")
                f.write("题目：\n")
                f.write(f"{question_text}\n\n")
            
            f.write("\n" + "="*30 + "\n\n")

if __name__ == "__main__":
    input_file = "pdf_output/2240231108 向毅 1概述.md"
    output_dir = "text_output"
    process_questions(input_file, output_dir) 