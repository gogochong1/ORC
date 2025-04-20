from rag import Rag

rag = Rag('deepseek-r1:14b', '私人知识库.txt')
rag.stream_chat('请介绍下刘芳')

