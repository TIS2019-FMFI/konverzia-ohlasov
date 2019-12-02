import sys
from app2.app2_initializer.app2_initializer import app2_initializer 
if __name__ == "__main__":
    initializer = app2_initializer(sys.argv)
    initializer.run_app()