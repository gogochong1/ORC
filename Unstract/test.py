from typing import List, Dict, Any
from unstract.llmwhisperer.client import LLMWhispererClient

def main():
    try:
        # 实例化客户端
        client = LLMWhispererClient(
            base_url="https://llmwhisperer-api.unstract.com/v1",
            api_key="2XYoKlXo-7rJwKTXwApPjT5LMy-eMWWFcNaTvELGUpw"
        )
        
        # 调用whisper方法
        file_path = "D:\\QianYi\\ORC\\pdf_test\\test04.pdf"
        response = client.whisper(file_path=file_path)
        
        # 打印响应内容
        print("响应类型:", type(response))
        print("响应内容:", response)
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误详情: {e.__class__.__name__}")

if __name__ == "__main__":
    main()
