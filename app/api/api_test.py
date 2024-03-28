import requests
import json

def query_flask_server(question):
    """Sends a question to the Flask server and returns the response."""
    url = "http://localhost:5000/ask"
    data = {"question": question}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Assuming the server responds with JSON
    else:
        return {"error": f"Request failed with status {response.status_code}"}

def main():
    print("Flask API Tester. Type 'exit' to quit.")
    
    while True:
        # Prompt the user for a question
        user_input = input("Please enter your question: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting...")
            break
        
        # Query the Flask server
        response = query_flask_server(user_input)
        
        # Check if there was an error
        if "error" in response:
            print(response["error"])
        else:
            # Parse and print out the answer
            answer = response.get("answer", "No answer found.")
            print("Answer:", answer)

if __name__ == "__main__":
    main()
