import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.postgres import PGVectorStore
from .text_extraction import ExtractText

load_dotenv(override=True)


class QueryEngine:
    def __init__(self):
        self.documents = []
        self.index = None

    def get_vector_store(self):
        url = urlparse(os.getenv("DATABASE_URL"))
        return PGVectorStore.from_params(
            host=url.hostname,
            port=url.port or 5432,
            database=url.path.lstrip("/"),
            user=url.username,
            password=url.password,
            table_name="documents",
            embed_dim=1536,
        )

    def build_index(self, file_paths):
        if isinstance(file_paths, str):
            file_paths = [file_paths]

        vector_store = self.get_vector_store()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")

        all_docs = []
        for file_path in file_paths:
            docs = self.build_docs(file_path)
            all_docs.extend(docs)

        index = VectorStoreIndex.from_documents(
            all_docs,
            storage_context=storage_context,
            embed_model=embed_model,
        )

        return index

    def load_index(self):
        vector_store = self.get_vector_store()
        embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            embed_model=embed_model,
        )
        return index

    def build_query_engine(self, index):
        return CitationQueryEngine.from_args(index, similarity_top_k=3)

    def build_docs(self, file_path):
        extractor = ExtractText()
        text = extractor.read_document(file_path=file_path)
        doc = Document(
            text=text,
            metadata={"filename": os.path.basename(file_path)},
        )
        return [doc]
