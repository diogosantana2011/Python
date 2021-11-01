## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#script-setup)

   -[Mongo](#mongo)
   
   -[Python](#python)

6. [Running Scripts](#running-scripts)
7. [Collaboration](#collaboration)
8. [FAQs](#faqs)

### General Info
***
Metrics Scripts created to pull information from MP API using Python. Can be applied to any other url which returns data in JSON format. 
Allows User input of date in format of DD-MM-YYYY and will save file to local created directoy(extracted-json-data).
Prints information on total logins for selected dates, as well as individual login by company name.
WIP
### A little funny (the guy who made it mispelled 'paste' too) meme to start us off!
![Image text](https://tse1.mm.bing.net/th?id=OIP.95Qw7RnpPEl6HXuuTpozRwHaHY&pid=Api&P=0&w=300&h=300)
## Technologies
***
A list of technologies used within the project:
* [Python 3.9.7] (https://www.python.org/): Version 3.9.7
* [Mongo 4.2] (https://www.mongodb.com/try/download/compass) Version 4.2 
* [Python Libraries - requests/json/os] (https://packaging.python.org/tutorials/installing-packages/)

# Script-setup

If you do not want to set up Mongo, that is fine. You can simply comment out pymongo's import and all related mongo db checks and writes of logged information.
Any libraries you use on your machine will be required to have the modules installed. You can explore this on the link above.

# Mongo
On windows, Mongo image will need to be manually downloaded from the mongo website listed above. 
Once downloaded, on your C:/ drive, create a 'data/db' directory. So you should that following path exists: 'C:/data/db'
You can install the Compass shell, as well as starting Mongo server.
The server needs to be started prior so that shell picks up connection created.
Open CMD, or cygwin (whichever shell you are using on windows that works).
Navigate ('cd' command) to 'C:/program files/mongodb/server/{version_downloaded}/bin.
Run 'mongod' -> This will initiate mongo connection and confirm towards bottom of screen 'Listening on port 127.0.0.1' which is the default port. 

# Python
Please bear in mind that if certain Python Modules (such as: requests, json, os, logging, datetime, pymongo etc.) are not installed on your machine, scripts will fail. 
To install modules please follow above link.
This can be done via shell using 'pip'. To see currently installed version of python please use 'python --version'.
To see the installed modules you can use command 'pip list'. 

Something similar to the below will display:
```
Package            Version
------------------ ---------
certifi            2021.5.30
charset-normalizer 2.0.6
idna               3.2
numpy              1.21.2
pip                21.2.3
pymongo            3.12.0
requests           2.26.0
setuptools         57.4.0
urllib3            1.26.7
```
***
## Running-scripts
***
Please bear in mind pre-installation guide information prior to running scripts, as otherwise errors will be encountered (TODO/fix). 
```
$ git clone https://github.com/diogosantana2011/diogosantana2011.git
$ cd ../path/to/the/file
$ python OR python3 specfile.py
```

## Running Scripts - Note

Calling python will vary from OS. On my windows I call python {script_name} and on my mac I call it via python3 {script_name}.
Best way to figure which one is to simply navigate to folder where its install (C:\Python3.9) and from here you will see application file.
Running it, will show you Pythons IDE, which you can use if you want. The IDE file path will display an .exe file, such as 'C:/python3.9/python.exe'
Therefore to start python you'd use 'python {script_name}'.

## Collaboration

If you want to use any script to obtain extracted data from any JSON returning API; be my guest =D.
You can push it to your own repo, but if you can also push a copy here, it be awesome. 
If you push a script through please add an extra folder with descriptive names to the script. You can do this directly to master, no worries.
Additionally, and IMPORTANT :-> If you make changes to one of my existing scripts; please create new branch and PR within describing so I can see before you merge changes to master. I'd like to keep up to date on those! 
Also, this way I can see how it can be better, or fixed and hopefully even learn something new.
Thanks for collaboration if you do <3
## Questions

Any questions, please reach out to diegsan20@gmail.com
