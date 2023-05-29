#### To run the program: 
You can run the app by the following steps:
1) Open 2019400231_2019400147 folder and MovieDBProject folder.
2) Create a virtual environment myenv with:
python3 -m venv myenv  
3) Activate the virtual environment with:
- For windows: myenv/Scripts/activate
- For macOS source myenv/bin/activate
4) Install the necessary requirements with:
pip install django
pip install psycopg2-binary
pip install -r requirements.txt
5) If you want to work with another server, you should change conn in line-5 checkDB.py file in MovieDBApp, else you can continue with our server
6) Run the django app with:
python3 manage.py runserver 
7) You can click the link after run it succesfully, which is http://127.0.0.1:8000
