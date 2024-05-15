from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core import Document


def create_index(txt_file_path, index_folder, youtube_url, model_name="BAAI/bge-m3"):
    with open(txt_file_path, 'r') as file:
        # Read the content of the file into a string
        file_content = file.read()
        Settings.embed_model = HuggingFaceEmbedding(model_name=model_name)
        document = Document(
            text=file_content,
            metadata={
                "title": txt_file_path,
                "category": "Video Transcription",
                "URL": youtube_url,
                "Link": youtube_url
            },
        )
        index = VectorStoreIndex.from_documents([document])
        index.storage_context.persist(persist_dir=index_folder)