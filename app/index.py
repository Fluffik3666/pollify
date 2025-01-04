from app.__init__ import create_app

app = create_app()

# Vercel requires the app to be named 'app'
app.debug = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)