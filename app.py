from flask import Flask

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/')
        def home():
            return "歡迎來到 Flask 應用!"

        @self.app.route('/about')
        def about():
            return "這是關於頁面！"
    
    def run(self, host="0.0.0.0", port=5000):
            self.app.run(host = host, port = port)

if __name__ == '__main__':
    app = FlaskApp()
    app.run()