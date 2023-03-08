import csv
from source import conexion
import os
from dotenv import load_dotenv
load_dotenv()

#Conexion a BD

PGHOST = os.environ.get('PGHOST')
PGUSER = os.environ.get('PGUSER')
PGPASSWORD = os.environ.get('PGPASSWORD')
PGDATABASE = os.environ.get('PGDATABASE')
bd = conexion.conn(PGHOST, PGUSER, PGPASSWORD, PGDATABASE)
#Se crea un cursor
cursor = bd.cursor()

#Abre el archivo y lo recorre 
with open('books.csv', 'r') as csvfile:
    #El lector omitira las , y las sustituira por el ""
    lector = csv.reader(csvfile)
    next(lector)
    
    for row in lector:
    #Se ejecuta
     cursor.execute("INSERT INTO books (Isbn, Title,Author,Year) VALUES (%s,%s,%s,%s)" , row )
    #Se envia a la BD
    bd.commit()
    print("Tarea Completada Exitosamente")
    bd.close()
    cursor.close()


        
