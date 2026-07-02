"""
最小 RAG demo
功能：把 data/knowledge_points/ 和 data/error_patterns/ 下的 markdown 文件
     embedding 后存入 Chroma，然后接受查询返回最相关的 3 条
"""

import os
import glob
import time
from pathlib import Path
import chromadb
from dotenv import load_dotenv
import dashscope
from dashscope import TextEmbedding

load_dotenv()
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
BASE_DIR = Path(__file__).parent.parent.parent  # hot100_AI-Native/
CHROMA_PATH = os.getenv("CHROMA_PATH", str(BASE_DIR / "chroma_db"))

# ============ Step 1: 加载所有 markdown 数据 ============
def load_documents():
    """返回 list of dict: [{id, content, source}]"""
    docs = []
    for folder in ["data/knowledge_points", "data/error_patterns","data/pedagogical_principles"]:
        for filepath in glob.glob(str(BASE_DIR / folder / "*.md")):
            # 跳过 README
            if "README" in filepath:
                continue
            filename = Path(filepath).stem  # 例如 "KP-001_two-pointers"
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            docs.append({
                "id": filename,
                "content": content,
                "source": folder
            })
    return docs

# ============ Step 2: Embedding 模型 ============
def embed_texts(texts, max_retries=3):
    """
    用阿里云 text-embedding-v3 给一批文本做 embedding
    每次最多 25 条，需要分批
    """
    all_embeddings = []
    batch_size = 10
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        for attempt in range(max_retries):
            try:
                resp = TextEmbedding.call(
                    model=TextEmbedding.Models.text_embedding_v3,
                    input=batch,
                    dimension=1024,
                )
                if resp.status_code != 200:
                    raise Exception(f"Embedding failed: {resp.message}")
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                print(f"Embedding 请求失败（第{attempt+1}次），2秒后重试: {e}")
                time.sleep(2)
        embeddings = [item['embedding'] for item in resp.output['embeddings']]
        all_embeddings.extend(embeddings)
    return all_embeddings

# ============ Step 3: 存入 Chroma ============
_chroma_client = None
_collection = None

def _get_collection():
    global _chroma_client, _collection
    if _collection is not None:
        return _collection

    _chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    docs = load_documents()
    doc_ids = [d["id"] for d in docs]

    existing = _chroma_client.list_collections()
    existing_names = [c.name for c in existing]

    if "hot100_kp_ep" in existing_names:
        col = _chroma_client.get_collection("hot100_kp_ep")
        # 如果文档数量一致则直接复用，否则重建
        if col.count() == len(docs):
            _collection = col
            return _collection
        _chroma_client.delete_collection("hot100_kp_ep")

    col = _chroma_client.create_collection(
        name="hot100_kp_ep",
        metadata={"hnsw:space": "cosine"}
    )
    embeddings = embed_texts([d["content"] for d in docs])
    col.add(
        ids=doc_ids,
        embeddings=embeddings,
        documents=[d["content"] for d in docs],
        metadatas=[{"source": d["source"]} for d in docs]
    )
    _collection = col
    return _collection

# ============ Step 4: 查询接口 ============
def retrieve(query, n=3):
    """给定查询，返回最相关的 n 条文档，格式为 [{"id": ..., "content": ...}]"""
    query_emb = embed_texts([query])
    results = _get_collection().query(
        query_embeddings=query_emb,
        n_results=n
    )
    return [
        {"id": doc_id, "content": content}
        for doc_id, content in zip(results["ids"][0], results["documents"][0])
    ]

# ============ Step 5: 测试 ============
if __name__ == "__main__":
    test_queries = [
        "我做二分查找老是边界写错",
        "什么时候用堆",
        "链表删除节点要不要加哨兵",
        "滑动窗口和双指针的区别",
        "为什么单调栈能 O(n)",
    ]
    for q in test_queries:
        print(f"\n查询: {q}")
        results = retrieve(q, n=3)
        for i, item in enumerate(results):
            print(f"  [{i+1}] {item['id']}")