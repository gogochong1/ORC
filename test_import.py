try:
    from unstract.llmwhisperer.client import LLMWhispererClient
    print("模块导入成功！")
except ImportError as e:
    print(f"导入失败: {str(e)}")
    print("请尝试运行: pip install unstract") 