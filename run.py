from web import app
if __name__ == "__main__":
  app.secret_key = 'super secret key'
  app.debug = True
  app.run(host='0.0.0.0')
