import logging
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d,%H:%M:%S', format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',)
import pandas as pd
from models import Base, engine, Session, Customer, Email, Phone
from sqlalchemy import exc

logger = logging.getLogger(__name__)


def extract(path,slicer,headers):
  '''Retorna un Dataframe con la información de los clientes
    Recibe la ruta del archivo (path) la indendación del mismo (slicer) y los encabezados (headers)'''
  try:
    df = pd.read_csv(path, delimiter='\t',header=None, dtype='string')
    for i in range(len(slicer)-1):
      df.insert(value=df[0].str[slicer[i]:slicer[i+1]], loc=i+1,column=i+1)
    customers = df.drop(axis=1, columns=0)
    customers.columns = headers
    return customers
  except Exception as e:
    logger.error('Ha ocurrido un error al capturar la información del archivo')
    logger.error(e)


def transform(data,strings):
  '''Retorna un diccionario de Dataframes con los clientes, emails y telefonos transformados'''
  data = to_uppercase(data, strings)
  logger.info('Se inician las trasnformaciones de los clientes')
  customers = customer_transform(data)
  logger.info('Se finalizan las trasnformaciones de los clientes')
  logger.info('Se inician las trasnformaciones de los emails')
  emails = emails_transform(data)
  logger.info('Se finalizan las trasnformaciones de los emails')
  logger.info('Se inician las trasnformaciones de los telefonos')
  phones = phones_transform(data)
  logger.info('Se finalizan las trasnformaciones de los telefonos')
  logger.info('Se inicia exportación de reportes en excel')
  customers.to_excel('./output/customers.xlsx', index = False)
  emails.to_excel('./output/emails.xlsx', index = False)
  phones.to_excel('./output/phones.xlsx', index = False)
  logger.info('Se finaliza exportación de reportes en excel')
  customers_transform = {
    'customers': customers,
    'emails': emails,
    'phones': phones
  }
  return customers_transform
    

def emails_transform(data):
  '''Retorna un Dataframe con los emails validos e invalidos en la data y con la estructura solicitada'''
  data = data[data['correo']!='                                                  ']
  emails = pd.DataFrame()
  emails['fiscal_id'] = data['rut'] + data['dv']
  emails['email'] = data['correo'].apply(lambda correo:correo.strip())
  emails['status'] = data['estatus_contacto'].apply(lambda status:status.strip())
  emails['priority'] = data['prioridad'].astype('int8')
  return emails.reset_index()


def phones_transform(data):
  '''Retorna un Dataframe con los telefonos validos e invalidos en la data y con la estructura solicitada'''  
  data = data[data['telefono']!='         ']
  phones = pd.DataFrame()
  phones['fiscal_id'] = data['rut'] + data['dv']
  phones['phone'] = data['telefono'].apply(lambda string:string.strip())
  phones['status'] = data['estatus_contacto'].apply(lambda status:status.strip())
  phones['priority'] = data['prioridad'].astype('int8')
  return phones.reset_index()


def customer_transform(data):
  '''Retorna un Dataframe con los clientes en la data y con la estructura solicitada'''  
  today = pd.to_datetime('today')
  customers = pd.DataFrame()
  customers['fiscal_id'] = data['rut'] + data['dv']
  customers['first_name'] = data['nombre'].apply(lambda string:string.strip())
  customers['last_name'] = data['apellido'].apply(lambda string:string.strip())
  customers['gender'] = data['genero'].apply(lambda string:string.strip())
  customers['birth_date'] = pd.to_datetime(data['fecha_nacimiento'], errors='coerce')
  customers['age'] = today.year - customers['birth_date'].dt.year.astype('int16')
  customers['age_group'] = customers['age'].apply(lambda age: get_age_group(age)).astype('int8')
  customers['due_date'] = pd.to_datetime(data['fecha_vencimiento'], errors='coerce')
  customers['delinquency'] = (today - customers['due_date']).dt.days.astype('int16')
  customers['due_balance'] = data['deuda'].astype('int32')
  customers['address'] = data['direccion'].apply(lambda string:string.strip())
  customers['ocupation'] = data['ocupacion'].apply(lambda string:string.strip())
  ocupations = pd.DataFrame(data['ocupacion'].drop_duplicates()).reset_index().drop('index', axis=1)
  ocupations['best_contact_ocupation_fiscal_id'] = ocupations['ocupacion'].apply(lambda ocupation:get_best_contact_ocupation(data[data['ocupacion']==ocupation]))
  customers['best_contact_ocupation'] = customers['fiscal_id'].apply(lambda fiscal_id:check_best_contact_ocupation(fiscal_id,ocupations)).astype('int8')
  return customers.drop_duplicates(subset=['fiscal_id']).reset_index().drop(['index'],axis=1)


def check_best_contact_ocupation(fiscal_id,ocupations):
  bco = ocupations[ocupations['best_contact_ocupation_fiscal_id']==fiscal_id]
  return 0 if bco.empty else 1


def get_best_contact_ocupation(data_ocupation):
  data_ocupation = data_ocupation[data_ocupation['estatus_contacto'] == 'VALIDO  ']
  data_ocupation = data_ocupation[data_ocupation['telefono'] != '         ']
  data_ocupation['fiscal_id'] = data_ocupation['rut'] + data_ocupation['dv']
  best_contact_counter = data_ocupation.groupby('fiscal_id')['telefono'].count().reset_index()
  best_contact_counter = best_contact_counter.sort_values(by=['telefono'], ascending=False)
  return best_contact_counter['fiscal_id'].iloc[0]


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


def load(data):
  Base.metadata.create_all(engine)
  session = Session()
  
  for index, row in data['customers'].iterrows():
    customer = Customer(row['fiscal_id'],
                        row['first_name'],
                        row['last_name'],
                        row['gender'],
                        row['birth_date'],
                        row['age'],
                        row['age_group'],
                        row['due_date'],
                        row['delinquency'],
                        row['due_balance'],
                        row['address'],
                        row['ocupation'],
                        row['best_contact_ocupation'])
    session.add(customer)
  try:
    session.commit()
  except Exception as e:
    logger.error(e)
  
  for index, row in data['emails'].iterrows():
    email = Email(row['fiscal_id'],
                        row['email'],
                        row['status'],
                        row['priority']
                        )
    session.add(email)
  try:
    session.commit()
  except Exception as e:
    logger.error(e)
  
  for index, row in data['phones'].iterrows():
    phone = Phone(row['fiscal_id'],
                    row['phone'],
                    row['status'],
                    row['priority']
                    )
    session.add(phone)
  try:
    session.commit()
  except Exception as e:
    logger.error(e)
  
  session.close()


if __name__ == '__main__':
  slicer = [0,7,8,28,53,62,72,82,88,138,168,172,174,224,232,241,242]
  headers = ['rut','dv','nombre','apellido','genero','fecha_nacimiento','fecha_vencimiento','deuda','direccion','ocupacion','altura','peso','correo','estatus_contacto','telefono','prioridad']
  strings = ['nombre','apellido','genero','direccion','ocupacion','correo','estatus_contacto']
  path = input('Introduce la ruta del archivo customers.txt: ')
  logger.info('Iniciando extracción de la data de archivo')
  data = extract(path,slicer,headers)
  logger.info('Se finaliza la extracción de la data del archivo y se inician las transformaciones')
  transformed_data = transform(data, strings)
  logger.info('Se finalizan todas las transformaciones y se inicia el cargue a la base de datos.')
  load(transformed_data)
  logger.info('Se finaliza el cargue de la información a la base de datos')
