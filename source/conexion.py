import psycopg2

def conn(host , usser, pasw, data):
    cn = psycopg2.connect(
       host = host,
       user = usser,
       password = pasw,
       database = data,
    ) 
    cn.set_session(autocommit=True)
    return cn
    