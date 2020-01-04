import sys
from app1.app1_initializer.app1_initializer import app1_initializer 
if __name__ == "__main__":
    initializer = app1_initializer(sys.argv)
    initializer.run_app()