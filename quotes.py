from flask import Flask, jsonify, redirect
from datetime import datetime
import requests

app = Flask(__name__)

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def fetch_random_quote():
    """
    uses quotable api to get random quotes and format as we wish and display them.
    :return: quote content, author and genre
    """
    url = 'http://api.quotable.io/quotes/random'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        quote_data = {
            'content': data[0]['content'],
            'author': data[0]['author'],
            'tags': data[0]['tags']
        }
        return quote_data
    else:
        return None

def split_content(content, max_chars):
    sentences = content.split('. ')
    pieces = []
    current_piece = ''

    for sentence in sentences:
        if len(current_piece) + len(sentence) + 2 <= max_chars:  # Add 2 for the period and space
            current_piece += sentence + '. '
        else:
            pieces.append(current_piece)
            current_piece = sentence + '. '

    if current_piece:
        pieces.append(current_piece)

    return pieces

def render_template(quote):
    """
    render the quote properly
    :param quote:
    :return:
    """
    content = quote['content']
    content_length = len(content) - 4
    author_padding = " " * (content_length - len(quote['author']))
    output = f"{Colors.YELLOW}Quote:{Colors.GREEN}"

    if content_length > 130:
        pieces = split_content(content, 130)
        output += '\n'.join(pieces)
    else:
        output += content

    output += f"\n{author_padding}{Colors.YELLOW}Source - {Colors.GREEN}{quote['author']}\n{Colors.YELLOW}Genre: {', '.join(quote['tags'])}{Colors.END}"
    return output

# Flask application and its routes
@app.route('/quote')
def get_quote():
    quote = fetch_random_quote()
    if quote:
        return jsonify(quote)
    else:
        return jsonify(error="Failed to fetch a random quote."), 500

@app.route('/')
def redirect_to_quote():
    return redirect('/quote')

@app.route('/health')
def health_check():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(status='Application is active and running', datetime=current_time), 200
@app.route('/healthz')
def healthz():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(status='Application is up and running', datetime=current_time), 200

# Running a Flask application with debug mode enabled may allow an attacker to gain access through the Werkzeug debugger.
# By visiting /crash, it is possible to gain access to the debugger, and run arbitrary code through the interactive debugger.
@app.route('/crash')
def crash_exception():
    raise Exception()

# Define a dictionary to store information about available endpoints
endpoint_info = {
    '/quote': 'Get a random quote',
    '/health': 'Check the health of the API',
    '/healthz': 'Check the health of the Application'
}

@app.errorhandler(404)
def not_found(error):
    error_message = {
        'Error': 'Not Found',
        'Message': 'The requested endpoint does not exist.',
        'Available_endpoints': endpoint_info
        }

    return jsonify(error_message), 404

if __name__ == '__main__':
    app.run()
