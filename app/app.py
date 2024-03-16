from flask import Flask, render_template, request, redirect, url_for
import bleach

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_chat', methods=['POST', 'GET'])
def generate_chat():
    if request.method == 'POST':
        manuscript = request.form['manuscript']
        sanitized_manuscript = bleach.clean(manuscript)
        conversation, error_message = parse_manuscript(sanitized_manuscript)

        if error_message:
            # Handle the error message, for example, print it or return an error response
            print("Error:", error_message)
        else:
            # Proceed with the conversation data
            for message in conversation:
                print(message)

        return render_template('chat.html', conversation=conversation, error_message=error_message)

    return redirect(url_for('index'))

def parse_manuscript(manuscript):
    conversation = []
    users = set()
    error_message = None
    
    lines = manuscript.split('\n')
    for line_number, line in enumerate(lines, start=1):
        line = line.strip()
        if line:
            if ':' not in line:
                line = f"B: {line}"
            
            user, message = line.split(': ', 1)
            users.add(user)
            
            if len(users) > 2:
                error_message = f"Invalid format: More than two users found in the conversation (line {line_number})."
                break
            
            conversation.append({'user': user, 'message': message})
    
    if len(users) != 2:
        error_message = "Invalid format: Exactly two users are required in the conversation."
    
    return conversation, error_message


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5777)
