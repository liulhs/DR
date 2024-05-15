from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.openai import OpenAI

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-m3"
)
storage_context = StorageContext.from_defaults(persist_dir="./app/index")
index = load_index_from_storage(storage_context)
memory = ChatMemoryBuffer.from_defaults(token_limit=50000)

chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt=(
        "You are a chatbot assistant helping a user with their questions. "
        "You are only allowed to provide information that is inside the context given to you. "
        "The context given is a transcript of a video. You are given the link to the video. "
        "First answer the user's question, then provide the timestamp in the video where the answer can be found. "
        "Convert the timestamp into seconds, for example, 1 minute and 30 seconds should be converted to 90 seconds. "
        "Then, add converted seconds with &t=<seconds> at the end of the video link. "
        "The anser is structured as Answer: <answer>, Link with timestamp: <link>."
    ),
)

while True:
    user_input = input("User: ")
    if user_input == "quit":
        break
    response = chat_engine.chat(user_input)
    print(response)
