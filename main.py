from front import *  # Import all components from the 'front' module

# Ensure this script runs only when executed directly, not when imported as a module
if __name__ == "__main__":
    front = Front()  # Instantiate the Front class from the 'front' module
    front.run()      # Execute the primary functionality of the Front instance, initiating the Streamlit app