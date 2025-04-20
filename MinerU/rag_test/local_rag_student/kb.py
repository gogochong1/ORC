import numpy as np
from ollama import Client
import PyPDF2
import docx

class Kb:
    def __init__(self, filepath):
        # 初始化Ollama客户端
        self.client = Client(host='http://localhost:11434')
        # 读取文件内容
        content = self.read_file(filepath)
        # 读取拆分好的数组
        self.chunks = self.split_content(content)
        # 转换成向量
        self.embeds = self.get_embeddings(self.chunks)

    # 读取文件
    def read_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    # 拆分知识库
    @staticmethod
    def split_content(content):
        chunks = content.split('# ')
        # 过滤掉空块
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
        return chunks

    # 字符串转向量(embeddings)
    def get_embedding(self, chunk):
        res = self.client.embeddings(model='nomic-embed-text', prompt=chunk)
        return res['embedding']

    def get_embeddings(self, chunks):
        embeds = []
        for chunk in chunks:
            embed = self.get_embedding(chunk)
            embeds.append(embed)
        return np.array(embeds)

    # 查询相似性向量
    def search(self, text):
        print(f"查询文本: {text}")
        max_similarity = 0
        max_similarity_index = 0
        ask_embed = self.get_embedding(text)
        for kb_embed_index, kb_embed in enumerate(self.embeds):
            similarity = self.similarity(kb_embed, ask_embed)
            if similarity > max_similarity:
                max_similarity = similarity
                max_similarity_index = kb_embed_index
        print(f"最大相似度: {max_similarity}")
        print(f"找到的相关内容: {self.chunks[max_similarity_index]}")
        return self.chunks[max_similarity_index]

    # 相似度
    @staticmethod
    def similarity(A, B):
        # 计算点积
        dot_product = np.dot(A, B)
        # 计算范数
        norm_A = np.linalg.norm(A)
        norm_B = np.linalg.norm(B)
        # 计算余弦相似度
        cosine_sim = dot_product / (norm_A * norm_B)
        return cosine_sim

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """从PDF文件中提取文本"""
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text

    @staticmethod
    def extract_text_from_docx(docx_path):
        """从DOCX文件中提取文本"""
        doc = docx.Document(docx_path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text) 