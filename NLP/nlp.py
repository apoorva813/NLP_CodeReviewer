import os
import spacy
from flake8.api import legacy as flake8
from dotenv import load_dotenv

nlp = spacy.load("en_core_web_sm")

def analyze_code(file_path):
    """Check for syntax/style issues using flake8."""
    style_guide = flake8.get_style_guide()
    report = style_guide.check_files([file_path])
    return report.get_statistics("E")  # Get errors

def review_variable_names(code):
    """Use NLP to flag unclear variable names."""
    doc = nlp(code)
    variables = [token.text for token in doc if token.pos_ == "NOUN"]
    feedback = []
    for var in set(variables):
        if len(var) < 3:  # Example heuristic
            feedback.append(f"⚠️ Short variable name: '{var}' (consider descriptive names)")
    return feedback


def main():
    def main():
    code_dir = "./sample_code"  # Absolute path like "C:/path/to/sample_code" works too
    if not code_dir:
        raise ValueError("CODE_DIR environment variable not set. Check your .env file.")
    
    print(f"Scanning directory: {code_dir}")  # Debug line
    for filename in os.listdir(code_dir):
        if filename.endswith(".py"):
            file_path = os.path.join(code_dir, filename)
            with open(file_path, "r") as f:
                code = f.read()
            
            print(f"\n🔍 Reviewing {filename}:")
            # 1. Run flake8 for syntax/style
            errors = analyze_code(file_path)
            for error in errors:
                print(error)
            
            # 2. NLP variable name check
            feedback = review_variable_names(code)
            for msg in feedback:
                print(msg)
 
if __name__ == "__main__":
    main()

