<h1> The AI Generation Application Musicaa </h1>
This application allows users to generate music using AI, manage their generated songs in a private library, and listen to and share songs.


# Setup the application
  ```
  git clone https://github.com/Speedy-yjo/musicaa
  cd musicaa/KUProject
```
# Instruction how to activate virtual environment
  ```
  python3 -m venv venv
source venv/bin/activate  # Window: venv\Scripts\activate
  ```

# Install dependencies (in case of no django or required libraries aren't installed on the machine the clone this repo)
```
pip install django
```

# How to migrate
```
python manage.py migrate
```

# How to create super user
```
python manage.py createsuperuser 
And follow instructions (give your email address and choose a password).
```

# How to run and navigate to admin page
Make sure you are in the directory : KUProject <br/>
Run the following command :  <br/>
```
python manage.py runserver
```
Now that the server’s running, visit http://127.0.0.1:8000/ with your web browser, and http://127.0.0.1:8000/admin/ to reach admin page.
