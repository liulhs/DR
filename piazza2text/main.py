from piazza2text import login, get_all_posts_for_course, generate_text_files_from_posts
# from llama_index.core import ServiceContext, VectorStoreIndex, SimpleDirectoryReader
# from llama_index.core import set_global_service_context
# from llama_index.core import StorageContext, load_index_from_storage



def main():
    # Hardcoded values
    email = ""
    password = ""
    course_id = "llqyd5tpdcq34o"

    # Use the session/token to fetch and process the posts
    try:
        json_response = get_all_posts_for_course(email, password, course_id)
        if json_response is not None:
            generate_text_files_from_posts(json_response)
            print("Text files generated successfully.")
        else:
            print("No posts found for the specified course.")
    except Exception as e:
        print("An error occurred:", e)

    # service_context = ServiceContext.from_defaults(
    # embed_model="local:intfloat/e5-small-v2"
    # )
    # set_global_service_context(service_context)

    # documents = SimpleDirectoryReader(input_files=["/home/ubuntu/app/indexing/text.txt"]).load_data()
    # index = VectorStoreIndex.from_documents(documents)

    # index.storage_context.persist(persist_dir="/home/ubuntu/app/indexing/index")

if __name__ == "__main__":
    main()
