from llama_index.core import ServiceContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import set_global_service_context
from llama_index.core import StorageContext, load_index_from_storage

service_context = ServiceContext.from_defaults(
    embed_model="local:intfloat/e5-small-v2"
)
set_global_service_context(service_context)

documents = SimpleDirectoryReader(input_files=["/home/ubuntu/app/indexing/text.txt"]).load_data()
index = VectorStoreIndex.from_documents(documents)

index.storage_context.persist(persist_dir="/home/ubuntu/app/indexing/index")
