#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse
import mysql.connector
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

import pymysql
pd.options.mode.chained_assignment = None  # default='warn'

# In[3]:

parser = argparse.ArgumentParser(description='Tables clear')
parser.add_argument('db_name', metavar='database_name', type=str, nargs='+',
                    help='database name')
parser.add_argument('db_pw', metavar='database_password', type=str, nargs='+',default='',
                    help='database password')
parser.add_argument('usr_name', metavar='user_name', type=str, nargs='+', default='root',
                    help='database user name')


args = parser.parse_args()

# In[4]:

db_name = ', '.join(args.db_name)
db_pw = ','.join(args.db_pw)
usr_name = ', '.join(args.usr_name)



# In[10]:


mydb = mysql.connector.connect(
    host="127.0.0.1",
    user=usr_name,
    database=db_name,
    password=db_pw
)


# In[11]:


mycursor = mydb.cursor()
clearcursor = mydb.cursor()
dropcursor = mydb.cursor()
viewcursor = mydb.cursor()
inicrecursor = mydb.cursor()




# In[12]:



mycursor.execute("SHOW TABLES")

table_names = [x[0] for x in mycursor]


#clearcursor.execute("DELETE FROM alldevices")
#clearcursor.execute("DROP VIEW alldevices")
#clearcursor.execute("TRUNCATE TABLE init_tb")

if "init_tb" not in table_names:
	inicrecursor.execute("CREATE TABLE init_tb (id int AUTO_INCREMENT PRIMARY KEY, time bigint, device_id int, operation varchar(255), detail varchar(255), duty_cycle varchar(255), UNIQUE KEY (time, operation, detail))")

if "device_tb1" not in table_names:
	inicrecursor.execute("CREATE TABLE device_tb1 (id int AUTO_INCREMENT PRIMARY KEY, time bigint, device_id int, operation varchar(255), detail varchar(255), duty_cycle varchar(255), UNIQUE KEY (time, operation, detail))")

# In[ ]: create the view


query = ("SELECT table_name FROM information_schema.tables WHERE table_schema = '"+db_name+"' AND table_name LIKE '%_tb%'")

viewcursor.execute(query)
union_all_query = "SELECT * FROM ("

for (table_name,) in viewcursor:
    union_all_query += f"SELECT * FROM {table_name} UNION ALL "
    
union_all_query = union_all_query[:-10]
    
union_all_query += ") AS alldevices"

create_view_query ="CREATE OR REPLACE VIEW alldevices AS " + union_all_query

viewcursor.execute(create_view_query)

# commit and close
mydb.commit()
mycursor.close()
inicrecursor.close()
viewcursor.close()
mydb.close()


# In[ ]:




