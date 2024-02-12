import requests
from icecream import ic

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    END = '\033[0m'
def fetch_random_quote():
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


# def render_template(quote):
#     content_length = len(quote['content']) - 3
#     author_padding = " " * (content_length - len(quote['author']))
#     # output = f"Quote: {quote['content']}\n{author_padding}author - {quote['author']}\n\nGenre: {', '.join(quote['tags'])}"
#     output = f"{Colors.GREEN}Quote: {quote['content']}\n{author_padding}author - {Colors.YELLOW}{quote['author']}\nGenre: {', '.join(quote['tags'])}{Colors.END}"
#     return output
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
    content = quote['content']
    content_length = len(content) -4
    author_padding = " " * (content_length - len(quote['author']))
    output = f"{Colors.YELLOW}Quote:{Colors.GREEN}"

    # Check if the content exceeds the character limit
    if content_length > 130:
        # Split the content into pieces based on max_chars
        pieces = split_content(content, 130)
        output += '\n'.join(pieces)
    else:
        output += content

    output += f"\n{author_padding}{Colors.YELLOW}Source - {Colors.GREEN}{quote['author']}\n{Colors.YELLOW}Genre: {', '.join(quote['tags'])}{Colors.END}"
    return output

if __name__ == "__main__":
    quote = fetch_random_quote()
    if quote:
        output = render_template(quote)
        print(output)
        # ic(output)
    else:
        print("Failed to fetch a random quote.")
        # ic("Failed to fetch a random quote.")
