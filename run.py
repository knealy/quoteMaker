import os
import subprocess
import sys

def main():
    # Create fonts directory if it doesn't exist
    os.makedirs('fonts', exist_ok=True)
    
    # Check if the virtual environment is activated
    in_venv = sys.prefix != sys.base_prefix
    
    if not in_venv:
        print("Please activate the virtual environment before running this script.")
        print("Run: source venv/bin/activate  (or venv\\Scripts\\activate on Windows)")
        sys.exit(1)
    
    # Download Roboto font if it doesn't exist
    font_path = os.path.join('fonts', 'Roboto-Bold.ttf')
    if not os.path.exists(font_path):
        try:
            import requests
            print("Downloading Roboto font...")
            font_url = "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Bold.ttf"
            response = requests.get(font_url)
            with open(font_path, 'wb') as f:
                f.write(response.content)
            print("Font downloaded successfully!")
        except Exception as e:
            print(f"Could not download font: {str(e)}")
            print("The application will use the default system font instead.")
    
    # Run the Streamlit app
    print("Starting Finance Quote Generator...")
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    main() 