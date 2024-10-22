from flask import Flask, Response
import os
import random
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
version = os.environ.get('VERSION', 'v3')
app_color = os.environ.get('APP_COLOR', 'yellow')
welcome_message = os.environ.get('WELCOME_MESSAGE', 'Welcome! You are currently viewing Upcommerce.com')

request_count = Counter('http_requests_total', 'Total HTTP Requests', ['version'])

@app.route('/')
def hello():
    request_count.labels(version=version).inc()
    
    # Simulate errors (0.1% of the time)
    if random.random() < 0.001:
        return "Internal Server Error", 500

    return f"""
    <html>
    <body style="background-color: {app_color};">
    <h1>{welcome_message}</h1>
    <p>Hello from version {version}!</p>
    </body>
    </html>
    """

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
