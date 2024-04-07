# Smart-dashboard
smart dashboard group project. My roles focus on user requirements analysis/ data collection/processing/shell programming.

iot.war is the whole project.

## data collection

read the IoT sensor data and store it to MySQL database

## environment
python 3.8.2

## Ubuntu
Ubuntu 18.04 

## libs (import first)
* argparse
* mysql.connector
* pandas
* sqlalchemy
* pymysql


## how to run 

### shell file
`./script.sh`

* at the current file which including 'cooja.sh', 'shell_view.py', 'table_fk.py'

* the output file will be created automatically

* the interval is 60 seconds

* the shell can automatically insert into the dataset

* if the user want to change the arugments about database, please read the Python file section

* Include commands running the data application, and 2 Python files

* DO NOT forget to change the arugments about database

#### data application (do not need to run individually)

`sudo bash cooja.sh`

* just creating the data

* the data application can be started in the shell file

* do not need to run individually


#### Python files (do not need to run individually)

1. `python3 shell_view.py -h`

* to check the arguments

* results: 

  usage: shellDemoSep.py [-h]<br>
                       file_address [file_address ...] database_name<br>
                       [database_name ...] database_password<br>
                       [database_password ...] user_name [user_name ...]<br>

  Process data collection

  positional arguments:<br>
    file_address       a data file address<br>
    database_name      database name<br>
    database_password  database password<br>
    user_name          database user name<br>

  optional arguments:<br>
    -h, --help         show this help message and exit

2.  `python3 shell_view.py [argument_list]`

    example in Jupyter Notebook: <br>
    
    `%run shell_view.py cooja.testlog database password user`

3.  ` python3 table_fk.py [argument list]`

    create a empty table and a empty view in the database

## *ATTENTION*


* use 

```
innodb_lock_wait_timeout = 120
```

to set the time

* use 

```
pd.options.mode.chained_assignment = None
```

to avoid *SettingWithCopyWarning*


## table - example

id - auto_increment primary key

time, operation, detail - unique key

table names: init_tb, device_tb1, device_tb2, ...

view name: alldevices

| id | time | device_id | operation | detail | duty_cycle |
| --- | --- | --- | --- | --- | --- |
| 1 | 610240| 1 | RecvData | 002001 | NULL |
| 2 | 610840 | 1 | RecvData | 002002 | NULL |
| 3 | 611321 | 1 | RecvData | 002003 | NULL |





