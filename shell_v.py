#!/usr/bin/env python
# coding: utf-8

# In[2]:


import argparse
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

import pymysql
pd.options.mode.chained_assignment = None  # default='warn'


# In[3]:


parser = argparse.ArgumentParser(description='Process data collection')
parser.add_argument('address', metavar='file_address', type=str, nargs='+',default='cooja.testlog',
                    help='a data file address')
parser.add_argument('db_name', metavar='database_name', type=str, nargs='+',
                    help='database name')
parser.add_argument('db_pw', metavar='database_password', type=str, nargs='+',default='',
                    help='database password')
parser.add_argument('usr_name', metavar='user_name', type=str, nargs='+', default='root',
                    help='database user name')


args = parser.parse_args()


# In[4]:


address = ', '.join(args.address)
db_name = ', '.join(args.db_name)
db_pw = ','.join(args.db_pw)
usr_name = ', '.join(args.usr_name)


# In[ ]:


file=open(address,'r')
s= file.read()
lines = s.split('\n')


array = [l.split() for l in lines]

log_df = pd.DataFrame(array)
log_df.head()


# In[5]:


df = log_df.iloc[:, 0:4]


# In[ ]:


df.columns = ['time','device_id', 'operation', 'detail' ]


# In[ ]:


df['device_id'] = df['device_id'].str.replace('ID:','')


# In[ ]:


def extract_digits_from_column(df, column_name, new_column_name):
    # select the number in the columu and generate the new column
    df[new_column_name] = df[column_name].str.extract('(\d+)', expand=False)

    # return new DataFrame
    return df

new_df = extract_digits_from_column(df, 'operation', 'duty_cycle')


# In[ ]:


new_df['operation'] = new_df['operation'].str.extract(r'([^0-9:]+)', expand=False)


# In[ ]: process NaN


new_df.fillna('NULL', inplace=True)


# In[ ]: initialization data

init_data = new_df[new_df['operation'].str.contains('start')]
init_data = new_df[new_df['detail'].str.contains('sending')]


# In[ ]: runtime data


dele_data = new_df[new_df['operation'].str.contains('Data|drop|Packets|duty|parent')]


# In[ ]: data type


dele_data['device_id']=dele_data['device_id'].astype(int)
dele_data['time']=dele_data['time'].astype(int)

# In[ ]:

init_data['device_id']=init_data['device_id'].astype(int)
init_data['time']=init_data['time'].astype(int)



# In[ ]: database connection 


mydb = mysql.connector.connect(
    host="127.0.0.1",
    user=usr_name,
    database=db_name,
    password=db_pw
)
mycursor = mydb.cursor()
createcursor = mydb.cursor()
insertcursor = mydb.cursor()
showcursor = mydb.cursor()
viewcursor = mydb.cursor()
initcursor = mydb.cursor()
inicrecursor = mydb.cursor()

# In[ ]: seperate tables


groups = dele_data.groupby('device_id')
mycursor.execute("SHOW TABLES")
innodb_lock_wait_timeout = 120

table_names = [x[0] for x in mycursor]

if "init_tb" not in table_names:
    inicrecursor.execute("CREATE TABLE init_tb (id int AUTO_INCREMENT PRIMARY KEY, time bigint, device_id int, operation varchar(255), detail varchar(255), duty_cycle varchar(255), UNIQUE KEY (time, operation, detail))")

if not init_data.empty:
    initcursor.execute("TRUNCATE TABLE init_tb")
    init_cols = ",".join([str(i) for i in init_data.columns.tolist()])
    for i,row in init_data.iterrows():
        sql = "INSERT INTO init_tb (" +init_cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
        initcursor.execute(sql, tuple(row))
        mydb.commit()
    

for group_name, group_data in groups:
    tb_name = f"device_tb{group_name}"
    if tb_name not in table_names:
        createcursor.execute("CREATE TABLE "+tb_name +" (id int AUTO_INCREMENT PRIMARY KEY, time bigint, device_id int, operation varchar(255), detail varchar(255), duty_cycle varchar(255), UNIQUE KEY (time, operation, detail))")
    
    cols = ",".join([str(i) for i in group_data.columns.tolist()]) 
    for i,row in group_data.iterrows():
        sql = "INSERT IGNORE INTO device_tb"+str(group_name)+" (" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
        insertcursor.execute(sql, tuple(row))
        mydb.commit()
    
    #tb_name=f"Group{group_name}"
    #group_data.to_sql(name=tb_name, con=mydb, if_exists='append', index=False)

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

mydb.commit()
viewcursor.close()
