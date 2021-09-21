
1.	Ensure the PC has access to the 192.168.234.0 subnet and can ping 192.168.234.25, 192.168.234.167 and 192.168.234.50
2.	Verify that python 3 (preferably 3.7 or higher) is installed (64 bit version, not 32)
3.	Install git https://git-scm.com/download/win (64 bit version, 2.31.0 or later) – use common sense for installation settings, use command prompt instead of bash, notepad for editor, etc.
4.	Open a NON-ADMINISTRATOR cmd prompt and CD \
6.	Enter the command git clone http://192.168.234.25:8880/kpulley/msa2060.git
7.	Cd C:\MSA2060
8.	Enter python -m venv venv
9.	Enter venv\scripts\activate
10.	You should now have a (venv) prompt
11.	Enter python -m pip install  --upgrade pip  (note, the email hides it but that’s two dashes for –upgrade) 
13.	Enter pip install -r requirements.txt
15.	Using Explorer copy the directory dist from  C:\MSA2060 to C:\MSA2060\venv\Lib\site-packages\openhtf\output\web_gui (overwrite all files)
16.	Make a short cut and copy the file SAN_test.bat to the Desktop
17.	Close the command prompt
18.	Cross your fingers
19.	Run the Desktop short cut. It should launch the command window and the browser window.
20.	Run through a test to make sure it works.
21. After the test has completed goto C:\MSA2060\Reports and verify it logged the result 



If the station needs updating in the future for new version of the test

1.	Open a NON-ADMIN cmd prompt. 
2.	Cd \MSA2060
3.	Enter command git pull


