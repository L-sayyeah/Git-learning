from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from sentence_transformers import SentenceTransformer
import weaviate
from weaviate.embedded import EmbeddedOptions
from weaviate.classes.query import MetadataQuery
from weaviate.classes.config import Configure, Property, DataType, VectorDistances, VectorFilterStrategy
import logging
logging.basicConfig(
    filename='logs/kb.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

class KnowledgeBase:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # 保持原有的连接方式
        self.client = weaviate.connect_to_custom(
            skip_init_checks=False,
            http_host="127.0.0.1",
            http_port=8080,
            http_secure=False,
            grpc_host="127.0.0.1",
            grpc_port=50051,
            grpc_secure=False,
        )
        
        self.class_name = 'fadasf'  # class的名字
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        try:
            self.client.collections.get(self.class_name)
        except Exception as e:
            # 创建 Weaviate 类（如果不存在）
            self._create_weaviate_class()

    def _create_weaviate_class(self):
        """创建 Weaviate 类（如果不存在）"""
        self.client.collections.create(
            self.class_name,
            vectorizer_config=[
                Configure.NamedVectors.text2vec_transformers(
                    name="query",
                    source_properties=["query"],                        # (Optional) Set the source property(ies)
                    vector_index_config=Configure.VectorIndex.hnsw()    # (Optional) Set vector index options
                ),
                # Set another named vector with the "text2vec-openai" vectorizer
                Configure.NamedVectors.text2vec_transformers(
                    name="query_text",
                    source_properties=["query", "text"],             # (Optional) Set the source property(ies)
                    vector_index_config=Configure.VectorIndex.hnsw()    # (Optional) Set vector index options
                ),
                # Set a named vector for your own uploaded vectors
                Configure.NamedVectors.none(
                    name="custom_vector",
                    vector_index_config=Configure.VectorIndex.hnsw()    # (Optional) Set vector index options
                )
            ],
            properties=[  # Define properties
                Property(name="query", data_type=DataType.TEXT),
                Property(name="text", data_type=DataType.TEXT),
            ],
        )
        self.logger.info(f"client: {self.client}: \n")
        
        

    def add_texts(self, documents, query):
        """将文档拆分为块并添加到 Weaviate"""
        chunks = self.text_splitter.split_documents(documents)
        
        doc = self.client.collections.get(self.class_name)
        self.logger.info(f"get: {doc}\n")
        with doc.batch.fixed_size(batch_size=200) as batch:
            for chunk in chunks:
                embedding = self.embedding_model.encode(chunk.page_content).tolist()
                #print(chunk.page_content)
                data_row = {
                        "query": query,
                        "text": chunk.page_content
                        }
                batch.add_object(
                    properties=data_row,
                )
                if batch.number_errors > 10:
                    print("Batch import stopped due to excessive errors.")
                    break
        return chunks
    def read_all(self):

        collection = self.client.collections.get(self.class_name)
        for item in collection.iterator():
            print(item.uuid, item.properties)
    
    def close(self):
        re = self.client.close()
        self.logger.info("quit\n")

    def retrieve(self, query, k=2):
        """基于查询进行相似度搜索"""
        # 生成查询的嵌入向量
        query_embedding = self.embedding_model.encode(query).tolist()
        doc = self.client.collections.get(self.class_name)
        response = doc.query.near_vector(
                near_vector=query_embedding, # your query vector goes here
                limit=k,
                target_vector="query_text",
                return_metadata=MetadataQuery(distance=True)
        )
        
        # 提取结果
        results = []
        for o in response.objects: 
            # print(o.properties)
            # print(o.metadata.distance)
            results.append(o)
        print("return kb\n")
        return results

if __name__ == "__main__":
    file_path = "search_data.txt"
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    query = "量子计算原理"
    kb = KnowledgeBase()
    kb.add_texts(documents,query)
    #kb.read_all()
    results = kb.retrieve(query)
    kb.close()
