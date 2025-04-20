import ollama
import re
import os
import time
import socket
from urllib.parse import urlparse

def verify_ollama_connection():
    """深度验证Ollama连接"""
    # 检测端口是否开放
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('127.0.0.1', 11434))
        if result != 0:
            raise ConnectionError(f"Ollama端口未开放 (错误代码: {result})")
    finally:
        sock.close()

    # 验证模型API
    try:
        model_list = ollama.list()
        if 'llama3.2-vision:latest' not in [m['name'] for m in model_list.get('models', [])]:
            raise ConnectionError("模型 llama3.2-vision:latest 未找到")
    except Exception as e:
        raise ConnectionError(f"模型验证失败: {str(e)}")

def extract_questions_answers(md_content):
    """优化版题目提取"""
    questions = []
    answers = []
    
    # 增强型正则匹配
    patterns = [
        (r'(\d+)[\.．]\s*(.*?)\n\s*答案[:：]?\s*([A-FTF])', 'all'),  # 兼容中英文标点
    ]
    
    for pattern, _ in patterns:
        for match in re.finditer(pattern, md_content, re.MULTILINE):
            num, question, answer = match.groups()
            questions.append(f"{num}. {question.strip()}")
            answers.append(answer.upper())
    
    return questions, answers

def call_vision_model(prompt, max_retries=3):
    """专用视觉模型调用函数"""
    for attempt in range(max_retries):
        try:
            response = ollama.generate(
                model='llama3.2-vision:latest',
                prompt=prompt,
                options={
                    'temperature': 0.1,
                    'num_ctx': 2048,
                    'timeout': 600  # 视觉模型需要更长时间
                },
                stream=False  # 确保完整响应
            )
            return response
        except ollama.ResponseError as e:
            if "context length" in str(e):
                raise RuntimeError("上下文长度不足，请减少题目数量或增大num_ctx")
            if attempt == max_retries - 1:
                raise
            time.sleep(5 * (attempt + 1))
        except Exception as e:
            raise RuntimeError(f"模型调用异常: {str(e)}")

def main():
    print("="*60)
    print("Ollama 视觉模型测评工具 (llama3.2-vision:latest)")
    print("="*60)
    
    # 1. 文件检查
    try:
        md_file = os.path.abspath(r"./output/pdf_change/01.md")
        if not os.path.exists(md_file):
            raise FileNotFoundError(f"文件路径不存在: {md_file}")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        print(f"\n[文件错误] {str(e)}")
        print("解决方案:")
        print(f"1. 检查文件路径: {os.path.abspath('.')}")
        print("2. 确认文件编码: file --mime-encoding your_file.md")
        return

    # 2. 连接验证
    try:
        print("\n[1/4] 验证Ollama连接...")
        verify_ollama_connection()
        print("✓ 服务验证通过")
    except ConnectionError as e:
        print(f"\n[连接错误] {str(e)}")
        print("\n修复步骤:")
        print("1. 启动服务: ollama serve --verbose")
        print("2. 下载模型: ollama pull llama3.2-vision")
        print("3. 检查端口: netstat -ano | findstr 11434")
        return

    # 3. 数据准备
    print("\n[2/4] 解析题目...")
    questions, correct_answers = extract_questions_answers(md_content)
    if not questions:
        print("⚠ 未发现有效题目，请检查:")
        print("1. 题目格式示例: '1. 问题内容...\\n答案: A'")
        print("2. 支持中英文标点(．或.)")
        return
    print(f"✓ 找到 {len(questions)} 道题目")

    # 4. 模型调用
    print("\n[3/4] 调用视觉模型...")
    try:
        prompt = (
            "你是一个专业考试助手，请严格按以下格式回答：\n"
            "1. 答案字母\n2. 答案字母\n...\n\n"
            "题目列表：\n" + "\n".join(questions)
        )
        
        start_time = time.time()
        response = call_vision_model(prompt)
        elapsed = time.time() - start_time
        
        print(f"✓ 生成成功 (耗时: {elapsed:.1f}s)")
        print("\n" + "="*30 + " 原始回答 " + "="*30)
        print(response['response'])
        print("="*70 + "\n")

        # 5. 结果评估
        print("[4/4] 评估结果...")
        model_answers = re.findall(r'(\d+)\.\s*([A-FTF])', response['response'])
        if not model_answers:
            raise RuntimeError("无法解析模型回答格式")
            
        results = []
        model_dict = {int(num): ans for num, ans in model_answers}
        for idx, (q, a) in enumerate(zip(questions, correct_answers), 1):
            user_ans = model_dict.get(idx, 'N/A')
            results.append({
                "序号": idx,
                "题目": q.split('.', 1)[1][:50] + "..." if len(q) > 50 else q,
                "正确答案": a,
                "模型答案": user_ans,
                "结果": "✓" if user_ans == a else "✗"
            })
        
        # 打印表格结果
        from tabulate import tabulate
        print(tabulate(results, headers="keys", tablefmt="grid"))
        
        accuracy = sum(1 for r in results if r["结果"] == "✓") / len(results) * 100
        print(f"\n最终正确率: {accuracy:.1f}%")
        
    except Exception as e:
        print(f"\n[模型错误] {str(e)}")
        print("\n调试建议:")
        print("1. 检查模型内存: ollama ps")
        print("2. 降低负载: 减少题目数量")
        print("3. 查看日志: ollama serve --verbose 2> ollama.log")

if __name__ == "__main__":
    main()