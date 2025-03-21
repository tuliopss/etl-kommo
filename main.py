from db.config import openConn, closeConn, create_table
import requests #type: ignore
import os
from dotenv import load_dotenv # type: ignore
import sys
sys.stdout.reconfigure(encoding='utf-8')  # Configura o terminal para UTF-8
load_dotenv()

TOKEN = os.getenv("TOKEN")
URL_LEADS = os.getenv("URL_LEADS")
URL_CONTACTS = os.getenv("URL_CONTACTS")
URL_GET_STATUS = os.getenv("URL_GET_STATUS")
URL_LEADS_LOSS_REASON = os.getenv("URL_LEADS_LOSS_REASON")

def get_connection_and_cursor():
    return openConn()


def getStatus():
    try:        
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.get(URL_GET_STATUS, headers=headers)
        if response.status_code == 200:
            data = response.json()  # Converte a resposta em JSON
           
            return data
        else:
                print(f"Erro: {response.status_code} - {response.text}")
                
    except Exception as e:
        print("Error: ", e)
        return e

def saveStatus():
    try:
        data = getStatus()
        connection, cursor = get_connection_and_cursor()

        # Verifica se 'pipelines' é uma lista
        for pipeline in data["_embedded"]["pipelines"]:  # Itera sobre os pipelines
            if "_embedded" in pipeline and "statuses" in pipeline["_embedded"]:
                for status in pipeline["_embedded"]["statuses"]:  # Itera sobre os status
                    query = f"INSERT INTO statususes (id, name, pipeline_id) VALUES ('{status['id']}', '{status['name']}', '{status['pipeline_id']}')"
                    cursor.execute(query)

        connection.commit()
        closeConn(connection, cursor)
    except Exception as e:
        print("Error: ", e)

def savePipelines(): 
    try:
        data = getStatus()
        connection, cursor = get_connection_and_cursor()

        # Verifica se 'pipelines' é uma lista
        for pipeline in data["_embedded"]["pipelines"]:  # Itera sobre os pipelines
            
            query = f"INSERT INTO pipelines (id, name) VALUES ('{pipeline['id']}', '{pipeline['name']}')"                    
            cursor.execute(query)

        connection.commit()
        closeConn(connection, cursor)
    except Exception as e:
        print("Error: ", e)


def get_all_leads():
    url = URL_LEADS
    headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
            
        }
    
    leads = []
    page = 1

    while True:
        response = requests.get(url, headers=headers, params={"page": page, "limit": 250})
        data = response.json()
        if "_embedded" in data and "leads" in data["_embedded"]:
            leads.extend(data["_embedded"]["leads"])
        else:
            break  # Sai do loop se não houver mais registros

        # Verifica se há próxima página
        if "next" in data["_links"]:
            page += 1
        else:
            break

    return leads

def get_loss_reasons():
    url = URL_LEADS_LOSS_REASON
    headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"           
        }
    
    leads = []
    page = 1

    while True:
        response = requests.get(url, headers=headers, params={"page": page, "limit": 250})
        data = response.json()
        
        if "_embedded" in data and "leads" in data["_embedded"]:
            leads.extend(data["_embedded"]["leads"])
        else:
            break  # Sai do loop se não houver mais registros

        # Verifica se há próxima página
        if "next" in data["_links"]:
            page += 1
        else:
            break
    loss_reasons = []
    for lead in leads:
        loss_reason_name = None  

        if "_embedded" in lead and "loss_reason" in lead["_embedded"] and lead["_embedded"]["loss_reason"]:
            loss_reason_name = lead["_embedded"]["loss_reason"][0]["name"]  # Pega o primeiro item da lista
            loss_reasons.append({
                "id": lead["_embedded"]["loss_reason"][0]["id"],
                "lead_id": lead["id"],
                "loss_reason": loss_reason_name
            })

        
    return loss_reasons


def get_all_contacts():
    url = URL_CONTACTS
    headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
    contacts = []
    page = 1

    while True:
        response = requests.get(url, headers=headers, params={"page": page, "limit": 250})
        data = response.json()

        if "_embedded" in data and "contacts" in data["_embedded"]:
            contacts.extend(data["_embedded"]["contacts"])
        else:
            break  # Sai do loop se não houver mais registros

        # Verifica se há próxima página
        if "next" in data["_links"]:
            page += 1
        else:
            break

    return contacts

def saveLeads():
    try:
        leads = get_all_leads()
        connection, cursor = get_connection_and_cursor()
    
        for lead in leads:
            contact_id = None  # Definir um valor padrão caso não haja contatos

            # Verifica se a chave "_embedded" e a lista "contacts" existem e não estão vazias
            if "_embedded" in lead and "contacts" in lead["_embedded"] and lead["_embedded"]["contacts"]:
                contact_id = lead["_embedded"]["contacts"][0]["id"]  # Pega o primeiro contato
            query = """INSERT INTO leads (id, name, status_id, pipeline_id, price, created_at, contact_id, loss_reason_id)
                    VALUES (%s, %s, %s, %s, %s,  FROM_UNIXTIME(%s), %s, %s)
                    ON DUPLICATE KEY UPDATE 
                    name = VALUES(name), status_id = VALUES(status_id), 
                    pipeline_id = VALUES(pipeline_id), price = VALUES(price), contact_id = VALUES(contact_id)"""
            
            values = (lead["id"], lead["name"], lead["status_id"], lead["pipeline_id"], lead["price"], lead["created_at"], contact_id, lead["loss_reason_id"])
            
            cursor.execute(query, values)
        connection.commit()
        closeConn(connection, cursor)

    except Exception as e:
        print("Error: ", e)

def saveContacts():
    try:
        contacts = get_all_contacts()  # Obtém os contatos da API
    
        connection, cursor = get_connection_and_cursor()  # Conexão com o banco

        for contact in contacts:
            
            query = """
                INSERT INTO contacts (id, name, first_name, last_name, created_at)
                VALUES (%s, %s, %s, %s, FROM_UNIXTIME(%s))
                ON DUPLICATE KEY UPDATE 
                first_name = VALUES(first_name), 
                last_name = VALUES(last_name)
            """

            values = (
                contact["id"],
                contact["name"],
                contact["first_name"],
                contact["last_name"],
                contact["created_at"],
            )

            cursor.execute(query, values)
        
        connection.commit()
        closeConn(connection, cursor)
    except Exception as e:
            print("Error: ", e)

def saveLossReasons():
    try:
        loss_reasons = get_loss_reasons()
        connection, cursor = get_connection_and_cursor()

        for reason in loss_reasons:
            query = """
            INSERT INTO loss_reasons (id, lead_id, loss_reason)
            VALUES (%s, %s, %s)
            
            """

            values = (
                reason["id"],
                reason["lead_id"],
                reason["loss_reason"]
             
            )
            cursor.execute(query, values)
        connection.commit()
        closeConn(connection, cursor)
    except Exception as e:
        print("Error: ", e)
# saveLeads()



saveLeads()
# saveStatus()
# savePipelines(    )
# saveLossReasons()
# saveContacts()