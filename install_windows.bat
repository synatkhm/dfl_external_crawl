Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
python -m pip install virtualenv
python -m virtualenv .venv
.\.venv\Scripts\activate      
python -m pip install -r .\requirements.txt