from package import create_app


# calling the flask app
app = create_app()

if __name__ == "__main__":
    app.run(port=8080)