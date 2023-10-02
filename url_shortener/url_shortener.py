from flask import Flask, request, redirect, render_template
import string
import random

app = Flask(__name__)

# Dictionary to store URL mappings (short to long)
url_mappings = {}

# Function to generate a random short URL alias
def generate_alias():
    alias_length = 6  # You can adjust the desired length
    characters = string.ascii_letters + string.digits
    return ''.join(
        random.choice(characters) 
        for _ in range(alias_length))

@app.route('/')
def index():
    return render_template('index.html', short_url=None)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['url']
    if long_url:
        alias = generate_alias()
        url_mappings[alias] = long_url
        short_url = f"{request.url_root}{alias}"
        return render_template(
            'index.html', 
            short_url=short_url)
    else:
        return render_template(
            'index.html', 
            short_url=None)

@app.route('/<alias>')
def redirect_to_url(alias):
    if alias in url_mappings:
        long_url = url_mappings[alias]
        return redirect(long_url)
    else:
        return "Alias not found"

if __name__ == '__main__':
    app.run()
