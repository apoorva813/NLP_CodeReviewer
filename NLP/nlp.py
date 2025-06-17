import os
import spacy
from flake8.api import legacy as flake8
from dotenv import load_dotenv

nlp = spacy.load("en_core_web_sm")

def analyze_code(file_path):
    """Check for syntax/style issues using flake8."""
    style_guide = flake8.get_style_guide()
    report = style_guide.check_files([file_path])
    return report.get_statistics("E")

def review_variable_names(code):
    """Use NLP to flag unclear variable names with enhanced checks."""
    doc = nlp(code)
    feedback = []
    for token in doc:
        if token.pos_ == "NOUN":
            if len(token.text) < 4:
                feedback.append(f"⚠️ Unclear variable: '{token.text}' (too short)")
            elif token.text.islower() and "_" not in token.text:  # Flags snake_case violations
                feedback.append(f"⚠️ Naming style: '{token.text}' (use snake_case)")
    return feedback

def main():
    load_dotenv()
    code_dir = os.getenv("CODE_DIR", "./sample_code")
    
    if not os.path.exists(code_dir):
        raise FileNotFoundError(f"Directory not found: {code_dir}")
    
    print(f"🔍 Scanning: {code_dir}")
    for filename in os.listdir(code_dir):
        if not filename.endswith(".py"):
            continue
        
        file_path = os.path.join(code_dir, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            
            print(f"\n📄 Reviewing {filename}:")
            for error in analyze_code(file_path):
                print(f"🚨 Flake8: {error}")
            for msg in review_variable_names(code):
                print(f"📝 NLP: {msg}")
                
        except Exception as e:
            print(f"❌ Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main()