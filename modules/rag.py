from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.logger import log


class RAG:

    def __init__(self):

        self.vectorstore = None

        self.embeddings = OpenAIEmbeddings()

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

    def load_documents(self, filepath):

        log(f"Loading documents from {filepath}")

        loader = TextLoader(filepath)

        docs = loader.load()

        chunks = self.splitter.split_documents(docs)

        log(f"Created {len(chunks)} chunks")

        self.vectorstore = FAISS.from_documents(
            chunks,
            self.embeddings
        )

        log("Vector store initialized")

    def search(self, query, k=4):

        if not self.vectorstore:

            log("Vector store empty")

            return []

        log("Running similarity search")

        docs = self.vectorstore.similarity_search(query, k=k)

        return [d.page_content for d in docs]