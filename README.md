<h1> The AI Generation Application Musicaa </h1>
This application allows users to generate music using AI, manage their generated songs in a private library, and listen to and share songs.

**Prerequisites:** Be sure you have installed the `requests` library which is used by our Suno API strategy wrapper.
```powershell
pip install requests
```



<h1> Running the application </h1>
Make sure you are in the directory : KUProject
Run the following command :  
<b> python manage.py runserver </b>
Now that the server’s running, visit http://127.0.0.1:8000/ with your web browser.

<div style="background-color: #f9f9fc; padding: 20px; border-radius: 8px; color: #333; font-family: sans-serif;">
<h2 style="color: #6366f1;">Song Generation Strategies</h2>

This project supports two different strategies for song generation using the Strategy Design Pattern:
- **Mock Strategy**: Simulates the API without making network requests. Great for local development.
- **Suno API Strategy**: Uses the actual `SunoApi.org` integration to generate songs.

<h3 style="color: #6366f1;">How to run Mock Mode</h3>
To run the server in Mock mode, ensure the `GENERATOR_STRATEGY` environment variable is set to `mock` (which is the default in `settings.py`). 
**Windows (PowerShell):**
```powershell
$env:GENERATOR_STRATEGY="mock"
python manage.py runserver
```

<h3 style="color: #6366f1;">How to run Suno Mode & Setting the API Key</h3>
To use the Suno API strategy, you need to set the strategy environment variable to `suno`. You also need to obtain a Suno API Key and specify it as an environment variable to ensure it is **NEVER committed to git**.

**Windows (PowerShell):**
```powershell
$env:GENERATOR_STRATEGY="suno"
$env:SUNO_API_KEY="your_actual_suno_api_key_here"
python manage.py runserver
```
</div>
