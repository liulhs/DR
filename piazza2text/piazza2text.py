import requests
import os

# Define your login function
def login(email, password):
    """Login to the API and return the access token."""
    data = {"email": email, "password": password}
    response = requests.post("http://lax.nonev.win:5500/users/login", json=data)
    if response.status_code == 200:
        # Assuming the API returns a token or a session ID for authenticated requests
        # This part may need to be adjusted based on the actual API response
        return response.json()
    else:
        raise Exception("Login failed!")

# Define the function to get all posts for a course
def get_all_posts_for_course(email, password, course_id):
    """Fetch all posts for a specific course and return the JSON response."""
    auth_token = login(email, password)
    posts_url = f"http://lax.nonev.win:5500/users/{email}/courses/{course_id}/posts/all"
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(posts_url, headers=headers)
    if response.status_code == 200:
        posts = response.json()
        return [post for post in posts if post is not None]
    else:
        raise Exception("Failed to retrieve posts for the course.")

# Define the function to generate text files from posts
def generate_text_files_from_posts(json_response):
    # Define the directory where the text files will be saved
    directory = './txt'
    question_file_path = os.path.join(directory, 'question.txt')
    announcement_file_path = os.path.join(directory, 'announcement.txt')

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Open the files and write the content
    with open(question_file_path, 'w', encoding='utf-8') as question_file, open(announcement_file_path, 'w', encoding='utf-8') as announcement_file:
        for post in json_response:
            if post and post['type'] == 'question':
                # Format the question and its answers
                question_content = f"Question: {post['detail']['content']}\n"
                answers = [f"Answer: {ans['content']}" for ans in post['answers']] if post['answers'] else ["Answer: No answers yet"]
                question_file.write(question_content + "\n".join(answers) + "\n\n")
            elif post and post['type'] == 'note':
                # Write the note content
                announcement_content = f"Announcement: {post['detail']['content']}\n"
                announcement_file.write(announcement_content + "\n\n")
