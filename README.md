# GMB_NetComm

## Project:
A final project in "Computer Security" course in HIT.

#### Lecturer
@ Roi Zimon

#### Authors:
@ Boris Mandelblat<br>
@ Galia Shwartz<br>
@ Moshe Gotam

### Requirements:
<ul>
<li>The application requires python3.8 or higher (can create a virtual env https://docs.python.org/3/library/venv.html)</li>
<li>To install the requirements run the following command:</li>
</ul>

```bash
pip install -r <path_to_requirements_file>/requirements.txt
```

### Run the application
####<ul><li>Make sure you have all the requirements</li></ul>

In order to run the application run the following command in the application location:
```bash
python3 manage.py runserver
```

### DB

A MySQL server was installed on AMAZON AWS instance.<br>
The application user have access to a specific database with specific credentials.

### Mail

A dedicated user was created in Gmail in order to satisfy the "forgot password" function reuqirement
<br>commltdhit@gmail.com
 


