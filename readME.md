#### To run the program: 
You can run the app by the following steps:
1) Open 2019400231_2019400147 folder and app folder.
2) Create a virtual environment .venv with:
python3 -m venv .venv  
3) Activate the virtual environment with:
. ./venv/bin/activate
4) Install the necessary requirements with:
pip install -r requirements.txt
5) If you want to work with another server, you should change conn in line-5 checkDB.py file in MovieDBApp, else you can continue with our server
6) Run the django app with:
python3 .\manage.py runserver 
7) You can click the link after run it succesfully, which is http://127.0.0.1:8000
