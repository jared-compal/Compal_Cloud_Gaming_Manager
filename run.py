import sys
from manager import create_app

if len(sys.argv) > 1 and sys.argv[1] == 'dev':
    app = create_app(2)
else:
    app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
