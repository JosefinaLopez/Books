import csv
from source import conexion

#Conexion a BD
bd = conexion.conn('localhost', 'postgres','070918','Books')
#Se crea un cursor
cursor = bd.cursor()

#Abre el archivo y lo recorre 
with open('books.csv', 'r') as csvfile:
    #El lector omitira las , y las sustituira por el ""
    lector = csv.reader(csvfile)
    next(lector)
    
    for row in lector:
    #Se ejecuta
     cursor.execute("INSERT INTO Book (Isbn, Title,Author,Year) VALUES (%s,%s,%s,%s)" , row )
    #Se envia a la BD
    bd.commit()
    print("Tarea Completada Exitosamente")
    bd.close()
    cursor.close()


        
