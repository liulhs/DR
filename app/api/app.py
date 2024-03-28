from flask import Flask, request, jsonify
from llama_index.core import StorageContext, load_index_from_storage, set_global_service_context, ServiceContext, VectorStoreIndex

# Initialize Flask app
app = Flask(__name__)

# Setup the llama-index service context
service_context = ServiceContext.from_defaults(
    embed_model="local:intfloat/e5-small-v2"
)
set_global_service_context(service_context)

# Load the index from storage
storage_context = StorageContext.from_defaults(persist_dir="/home/ubuntu/app/indexing/index")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()

@app.route('/ask', methods=['POST'])
def ask_question():
    # Extract question from the request
    data = request.get_json(force=True)
    user_question = data.get('question', '')

    # Use the query engine to get a response
    response_object = query_engine.query(user_question)
    
    # Convert the response object to a string (if it's not already)
    # This step depends on the structure of your 'NodeWithScore' object and how you want to format the response
    # Here, we're assuming the response object can be converted directly or has an attribute that can be used
    response = str(response_object)  # Adjust this line as necessary based on the actual response structure

    # Return the response as a JSON response
    return jsonify({'question': user_question, 'answer': response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
