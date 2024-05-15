from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core import Document
from pathlib import Path


# def create_index(txt_file_path, index_folder, youtube_url, model_name="BAAI/bge-m3"):
#     with open(txt_file_path, 'r') as file:
#         # Read the content of the file into a string
#         file_content = file.read()
#         Settings.embed_model = HuggingFaceEmbedding(model_name=model_name)
#         document = Document(
#             text=file_content,
#             metadata={
#                 "title": txt_file_path,
#                 "category": "Video Transcription",
#                 "URL": youtube_url,
#                 "Link": youtube_url
#             },
#         )
#         index = VectorStoreIndex.from_documents([document])
#         index.storage_context.persist(persist_dir=index_folder)


def create_index(txt_file_path, index_folder, youtube_url, model_name="BAAI/bge-m3"):
    # Read the content of the file into a string
    with open(txt_file_path, 'r') as file:
        file_content = file.read()
    
    # Set the embedding model
    Settings.embed_model = HuggingFaceEmbedding(model_name=model_name)
    
    # Create the Document object
    document = Document(
        text=file_content,
        metadata={
            "title": txt_file_path,
            "category": "Video Transcription",
            "URL": youtube_url,
            "Link": youtube_url
        },
    )
    
    # Path to the index's metadata file
    docstore_path = Path(index_folder) / "docstore.json"
    
    if docstore_path.exists():
        # Load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=index_folder)
        index = load_index_from_storage(storage_context)
        
        # Insert the new document
        index.insert(document)
    else:
        # Create a new index
        index = VectorStoreIndex.from_documents([document])
    
    # Persist the index
    index.storage_context.persist(persist_dir=index_folder)