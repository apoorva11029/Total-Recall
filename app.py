#!venv/bin/python

app = Flask(__name__)

@app.route('/')
	def index():
