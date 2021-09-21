python -m venv venv
cmd /k "cd /d C:\MSA2060\venv\Scripts & activate & cd /d    C:\MSA2060 & python -m pip install pip --upgrade & cd /d   C:\MSA2060 & pip install -r requirements.txt & cd /d   C:\MSA2060 &  xcopy dist venv\Lib\site-packages\openhtf\output\web_gui\dist /s /e /y & cd /d C:\MSA2060\venv\Scripts & deactivate"


