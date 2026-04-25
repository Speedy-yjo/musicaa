import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicaa.settings')
django.setup()

from musicaaApp.generator.factory import get_generator_strategy
from musicaaApp.model.form import Form
from musicaaApp.model.user import User

def run_demonstration():
    print("=========================================")
    print("      Testing Generator Strategy         ")
    print("=========================================")
    
    strategy = get_generator_strategy()
    print(f"Active Strategy: {type(strategy).__name__}\n")
    
    # Create a mock user if one doesn't exist
    user, _ = User.objects.get_or_create(
        name='testuser', 
        email='test@test.com'
    )
    
    # Dummy form using the Form model fields
    form = Form(
        name="Demo Song",
        prompt="A relaxing tune about coding in Python",
        mood="calm",
        genre="pop",
        occasion="party",
        singerIsMale=True,
        lengthInSeconds=120,
        user=user
    )
    
    print(f"Request Form : {form.name}")
    print(f"Prompt       : '{form.prompt}'\n")
    
    try:
        # 1. Initiate Generation
        print(">>> Initiating song generation...")
        task_id = strategy.generate(form)
        print(f"    Received Task ID: {task_id}\n")
        
        # 2. Check Status
        if task_id:
            print(">>> Checking generation status...")
            status = strategy.get_status(task_id)
            print(f"    Status Profile: {status}")
            print("\n    (If you are on Suno Mode and using a real API key, this will return the real status).")
        else:
            print(">>> Error: No Task ID was returned.")
            
    except Exception as e:
        print(f"\n[!] Error during strategy execution: {e}")
        print("Note: If you are seeing a 401 error, you likely need to put your real SUNO_API_KEY into the settings or environment variable.")

if __name__ == "__main__":
    run_demonstration()
