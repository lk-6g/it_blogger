python -m venv ll_env
copy ll_env\Scripts\activate.bat
echo python manage.py runserver>>activate.bat
rename activate.bat 运行本地服务器.bat
pause