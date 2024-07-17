from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core import Document


def create_index(txt_file_path, index_folder):
    with open(txt_file_path, 'r') as file:
        # Read the content of the file into a string
        file_content = file.read()
        document = Document(
            text=file_content,
            metadata={"filename": txt_file_path},
        )
        index = VectorStoreIndex.from_documents([document])
        index.storage_context.persist(persist_dir=index_folder)