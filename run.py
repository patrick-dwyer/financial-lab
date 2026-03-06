from app import create_app

print("Attempting to start the server...")

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)