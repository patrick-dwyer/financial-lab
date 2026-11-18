from app import create_app

print("Attempting to start the server...")

app = create_app()

if __name__ == "__main__":
    debug_mode = app.config.get('DEBUG', True)
    app.run(debug=debug_mode)