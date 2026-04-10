import os

from server.app import main

if __name__ == "__main__":
    os.environ.setdefault("PORT", "7860")
    main()

