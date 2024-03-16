from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_chat', methods=['POST'])
def generate_chat():
    if request.method == 'POST':
        manuscript = request.form['manuscript']
        conversation = parse_manuscript(manuscript)
        return render_template('chat.html', conversation=conversation)
    return 'Invalid Request'

def parse_manuscript(manuscript):
    conversation = []
    lines = manuscript.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            user, message = line.split(': ', 1)
            conversation.append({'user': user, 'message': message})
    return conversation

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5777)
