import sys
import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)
from resourses.code.main import main

if __name__ == "__main__":
    main()
