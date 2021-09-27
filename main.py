import logging
logging.basicConfig(level=logging.INFO)
import datetime
import pandas as pd

logger = logging.getLogger(__name__)


def extract(path,slicer,headers):
    '''Retorna un Dataframe con la información de los clientes
        Recibe la ruta del archivo (path) la indendación del mismo (slicer) y los encabezados (headers)'''
    try:
        df = pd.read_csv(path, delimiter='\t',header=None)
        for i in range(len(slicer)-1):
            df.insert(value=df[0].str[slicer[i]:slicer[i+1]], loc=i+1,column=i+1)
        customers = df.drop(axis=1, columns=0)
        customers.columns = headers
        return customers
    except Exception as e:
        logger.error('Ha ocurrido un error al capturar la información del archivo')
        logger.error(e)

def transform(data,strings):
    for string in strings:
        data[string] = data[string].apply(lambda i:data[string].str.upper())

    print(data)



if __name__ == '__main__':
    slicer = [0,7,8,28,53,62,72,82,88,138,168,172,174,224,232,241,242]
    headers = ['rut','dv','nombre','apellido','genero','fecha_nacimiento','fecha_vencimiento','deuda','direccion','ocupacion','altura','peso','correo','estatus_contacto','telefono','prioridad']
    strings = ['nombre','apellido','genero','direccion','ocupacion','correo','estatus_contacto']
    path = input('Introduce la ruta del archivo customers.txt: ')
    logger.info('Iniciando extracción de la data de archivo')
    data = extract(path,slicer,headers)
    print(data)
    logger.info('Se finaliza la extracción de la data del archivo y se inician las transformaciones')
    customers = transform(data, strings)