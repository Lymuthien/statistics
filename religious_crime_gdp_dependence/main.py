from pathlib import Path
from src import App

if __name__ == "__main__":
    path = Path(__file__).resolve().parent / "data"
    app = App(path)
    app.run()
