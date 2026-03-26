<h1> The AI Generation Application Musicaa </h1>
This application allows users to generate music using AI, manage their generated songs in a private library, and listen to and share songs.


# Setup the application
<p>
  git clone https://github.com/Speedy-yjo/musicaa
  cd musicaa/KUProject
</p>

# Instruction how to activate virtual environment
<p>
  python3 -m venv venv
  source venv/bin/activate
</p>

# Install dependencies (in case of no django or required libraries aren't installed on the machine the clone this repo)
<p> pip install django </p>

# How to migrate
<p> python manage.py migrate </p>

# How to create super user
<p> python manage.py createsuperuser 
  And follow instructions (give your email address and choose a password).
</p>

# How to run and navigate to admin page
Make sure you are in the directory : KUProject
Run the following command :  
<b> python manage.py runserver </b>
Now that the server’s running, visit http://127.0.0.1:8000/ with your web browser.
