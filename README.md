# Kanban Application

Hello, this is a mediocre Kanban application, created using React and Flask. 

To run this in your local environment, do the following steps:

### Setting up backend

** macOS ** 
```
cd server
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

cd kanban
python3 app.py
```

** Windows **
```
cd server
python3 -m venv venv
venv\Scripts\activate.bat
pip3 install -r requirements.txt

cd kanban
python3 app.py
```

### Setting up frontend
```
cd client
yarn
yarn start
```

And enjoy!

---
### Testing
```
pytest tests
```

To see coverage:
```
pytest --cov=kanban tests/
```
