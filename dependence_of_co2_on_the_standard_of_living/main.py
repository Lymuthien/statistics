from pathlib import Path
from src import Pipelane

if __name__ == "__main__":
    path = Path(__file__).resolve().parent / "data"
    app = Pipelane(path)
    app.run()
