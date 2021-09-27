import logging
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d,%H:%M:%S', format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',)
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
  logger.info('Se inicia la conversion de strings en Mayuscula')
  data = to_uppercase(data, strings)
  logger.info('Se finaliza la conversion de strings en Mayuscula')
  customers = customer_transform(data)
    

def customer_transform(data):
  today = pd.to_datetime('today')

  customers = pd.DataFrame()
  customers['fiscal_id'] = data['rut'] + ' ' + data['dv']
  customers['first_name'] = data['nombre']
  customers['last_name'] = data['apellido']
  customers['gender'] = data['genero']
  customers['birth_date'] = pd.to_datetime(data['fecha_nacimiento'], errors='coerce')
  customers['age'] = today.year - customers['birth_date'].dt.year
  customers['age_group'] = customers['age'].apply(lambda age: get_age_group(age))
  customers['due_date'] = pd.to_datetime(data['fecha_vencimiento'], errors='coerce')
  customers['delinquency'] = (today - customers['due_date']).dt.days
  customers['due_balance'] = data['deuda']
  customers['address'] = data['direccion']
  customers['ocupation'] = data['ocupacion']
  ocupations = pd.DataFrame(data['ocupacion'].drop_duplicates()).reset_index().drop('index', axis=1)
  print(ocupations['ocupacion'])
  print(data['ocupacion'])
  ocupations['best_contact_ocupation_fiscal_id'] = ocupations['ocupacion'].apply(lambda ocupation:get_best_contact_ocupation(data[data['ocupacion']==ocupation]))

  #print(customers)
  return customers


def get_best_contact_ocupation(data_ocupation):
    data_ocupation = data_ocupation[data_ocupation['estatus_contacto'] == 'Valido  ']
    #print(data_ocupation)


def get_age_group(age):
  if age <= 20:
    return 1
  elif age >= 21 and age <= 30:
    return 2
  elif age >= 31 and age <= 40:
    return 3
  elif age >= 41 and age <= 50:
    return 4
  elif age >= 51 and age <= 60:
    return 5
  elif age >= 61:
    return 6


def to_uppercase(data, strings):
  for string in strings:
    data[string] = data[string].str.upper()
  return data


if __name__ == '__main__':
  slicer = [0,7,8,28,53,62,72,82,88,138,168,172,174,224,232,241,242]
  headers = ['rut','dv','nombre','apellido','genero','fecha_nacimiento','fecha_vencimiento','deuda','direccion','ocupacion','altura','peso','correo','estatus_contacto','telefono','prioridad']
  strings = ['nombre','apellido','genero','direccion','ocupacion','correo','estatus_contacto']
  path = input('Introduce la ruta del archivo customers.txt: ')
  logger.info('Iniciando extracción de la data de archivo')
  data = extract(path,slicer,headers)
  logger.info('Se finaliza la extracción de la data del archivo y se inician las transformaciones')
  customers = transform(data, strings)
