from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/api/incoming/<token>', methods=['POST'])
def handler(token):
    try:
        # Note: Token authorization can be added here in the future

        # Log the incoming request along with the token
        print(f"Incoming request with token: {token}")
        print(f"Request data: {request.json}")

        # Your processing logic goes here
        
        return jsonify({"data": "Request received successfully"}), 200

    except Exception as e:
        print("Error in /incoming endpoint:", e)
        return jsonify({"error": "An error occurred while processing the request."}), 500

if __name__ == '__main__':
  app.run(port=5000)
