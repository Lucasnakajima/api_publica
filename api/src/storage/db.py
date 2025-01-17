from typing import List
import json
import requests
import pandas as pd

import mysql.connector

from models import *

from .queries import Queries
import uuid
import io
import boto3
import os

from datetime import datetime

secret_arn = os.environ['SECRET_ARN']
secrets_manager = boto3.client('secretsmanager', region_name="sa-east-1")

def upload_image(contents):
    s3_client = boto3.client("s3")
    image_name = str(uuid.uuid4()) + '.jpg'

    temp_file = io.BytesIO()
    temp_file.write(contents)
    temp_file.seek(0)
    s3_client.upload_fileobj(temp_file, 'sejusc-pcd-ciptea-images', image_name)
    
    s3_client.put_object_acl(
        ACL='public-read',
        Bucket='sejusc-pcd-ciptea-images',
        Key=image_name
    )

    temp_file.close()

    return image_name

def get_db_credentials():
    secret = secrets_manager.get_secret_value(SecretId=secret_arn)

    return {
        "host": 'rds-pcd-prod.cluster-c4irymq85uhb.sa-east-1.rds.amazonaws.com',
        "user": json.loads(secret['SecretString'])['username'],
        "password": json.loads(secret['SecretString'])['password'],
    }

def get_conn():
    credentials = get_db_credentials()
    
    return mysql.connector.connect(
        host=credentials['host'],
        user=credentials['user'],
        password=credentials['password'],
        database="pcd"
    )


def get_last_solicitations(limit) -> List[LastSolicitations]:
    query = Queries.get_last_solicitations
    params = [limit]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    requests = cursor.fetchall()

    return [LastSolicitations(*req) for req in requests]

def get_requests(limit=100, offset=0) -> List[DocumentRequest]:
  query = Queries.get_request
  params = (limit, offset)

  conn = get_conn()
  cursor = conn.cursor()
  cursor.execute(query, params)
  requests = cursor.fetchall()

  return [DocumentRequest(*req) for req in requests]

def get_total_by_project() -> List[Projetos]:
    query = Queries.count_by_project

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query)
    requests = cursor.fetchall()

    return [Projetos(*req) for req in requests]


def get_total_by_municipio() -> List[Municipios]:
    query = Queries.count_by_municipio

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query)
    requests = cursor.fetchall()

    return [Municipios(*req) for req in requests]
def get_historico(filters: dict) -> List[HistoryRequest]:

    query = Queries.get_historico
    params = []
    order = filters['order']
    condition = ''
    if filters.get('cpf'):
        condition += " h.cpf like %s"
        params.append(filters['cpf'])
    if filters.get('alert_id'):
        condition += ' and h.alert_id=%s'
        params.append(filters['alert_id'])
    if filters.get('nome'):
        condition += " and lower(h.nome) like %s"
        params.append('%'+filters['nome']+'%')
    if filters.get('start_date'):
        condition += " and cast(h.created_at as date) >= from_unixtime(%s/1000) "
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition += " and cast(h.created_at as date) <= from_unixtime(%s/1000)"
        params.append(filters['end_date'])
    if filters.get('statusId'):
        condition += " and h.statusId = %s"
        params.append(filters['statusId'])

    params.append(filters['fim'])
    params.append(filters['inicio'])
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition, order=order), params)
    requests = cursor.fetchall()

    return [HistoryRequest(*req) for req in requests]

def get_historico_by_cpf(cpf: str) -> List[HistoryByCPF]:
    query = Queries.get_historico_by_cpf
    params = [cpf]
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute(query, params)
    requests = cursor.fetchall()

    return [HistoryByCPF(*req) for req in requests]        
  
def get_recepcao(filters:dict) -> List[SolicitationRecepcao]:
    query = Queries.get_informations_recepcao
    order = filters['order']
    params = []
    condition = ''
    if filters.get('cpf'):
        condition += "and benef_cpf = %s"
        params.append(filters['cpf'])
    if filters.get('alert_id'):
        condition += "and alert_id = %s"
        params.append(filters['alert_id'])
    if filters.get('nome'):
        condition += "and benef_nome like %s"
        params.append('%'+filters['nome']+'%')
    
    params.append(filters['fim'])
    params.append(filters['inicio'])

    conn = get_conn()
    cursor = conn.cursor()
        
    cursor.execute(query.format(conditions=condition, order=order), params)
    requests = cursor.fetchall()

    return [SolicitationRecepcao(*req) for req in requests]        

def get_count_recepcao(filters:dict) -> List[SolicitationRecepcao]:
    query = Queries.get_count_recepcao
    params = []
    condition = ''
    if filters.get('cpf'):
        condition += "and benef_cpf = %s"
        params.append(filters['cpf'])
    if filters.get('alert_id'):
        condition += "and alert_id = %s"
        params.append(filters['alert_id'])
    if filters.get('nome'):
        condition += "and benef_nome like %s"
        params.append('%'+filters['nome']+'%')

    conn = get_conn()
    cursor = conn.cursor()
        
    cursor.execute(query.format(conditions=condition), params)
    requests = cursor.fetchall()

    return [CountRecepcao(*req) for req in requests]

def get_alert_events_by_cpf(cpf: str) -> List[AlertEventsBYCPF]:
    query = Queries.get_alert_events_by_cpf
    params = [cpf]
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute(query, params)
    requests = cursor.fetchall()

    return [AlertEventsBYCPF(*req) for req in requests]        
  

def get_solicitacao_by_hashId(hashId:str) -> List[SolicitationByhashId]:
    query = Queries.get_solicitation_by_hashId
    params = [hashId]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    requests = cursor.fetchall()

    return [SolicitationByhashId(*req) for req in requests]

def get_historic_by_alertd_id(alert_id:int) -> List[HistoryByAlertId]:
    query = Queries.get_historico_by_alert_id
    params = [alert_id]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    requests = cursor.fetchall()

    return [HistoryByAlertId(*req) for req in requests]

def get_historico_modified_by_alert_id(alert_id:int) -> List[HistoryModifiedByAlertId]:
    query = Queries.get_historico_modified_by_alert_id
    params = [alert_id]
    conn= get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    requests = cursor.fetchall()

    return [HistoryModifiedByAlertId(*req) for req in requests]

def get_solicitation_by_alert_id(alert_id:int)-> List[SolicitationByAlertId]:
    query = Queries.get_solicitation_by_alert_id
    params = [alert_id]
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    requests = cursor.fetchall()

    return [SolicitationByAlertId(*req) for req in requests]

def get_hash(filters: dict) -> List[HashRequest]:

    query = Queries.get_cpf_hash
    params = []
    order = filters['order']
    condition = ''
    condition_group = ''
    
    if filters.get('view'):
        view = filters['view']
        if view == 'solicitacao':
            condition += "statusId in (2, 21)"
        else:
            condition += "statusId in (6, 25)"
    if filters.get('nome'):
        condition += " and lower(benef_nome) like %s"
        params.append('%' + filters['nome'] + '%')
    if filters.get('nome_responsavel'):
        condition += 'and lower(resp_nome) like %s'
        params.append('%'+ filters['nome_responsavel'] + '%')
    if filters.get('cid'):
        condition += 'and lower(cid) like %s'
        params.append('%'+ filters['cid'] + '%')
    if filters.get('cpf'):
        condition += " and benef_cpf like %s"
        params.append(filters['cpf'])
    if filters.get('alert_id'):
        condition += "and alert_id in (%s)"
        params.append(filters['alert_id'])
    if filters.get('projeto'):
        projeto = filters['projeto']
        if projeto == 'PCD':
            condition += "and (channelId like '%4495%' or channelId like '%4499%' or channelId like '%12836%')"
        elif projeto == 'CIPTEA':
            condition += "and (channelId like '%6744%' or channelId like '%6790%' or channelId like '%12837%')"
        else:
            condition += 'null'
    if filters.get('via'):
        condition += " and tipo_carteira=%s "
        params.append(filters['via'])
    if filters.get('municipio_realizado_cadastro'):
        condition += 'and lower(municipio_realizado_cadastro_meta) like %s'
        params.append('%'+ filters['municipio_realizado_cadastro'] + '%')
    if filters.get('local_de_retirada'):
        condition += 'and lower(local_de_retirada_meta) like %s'
        params.append('%'+ filters['local_de_retirada'] + '%')
    if filters.get('deficiencia'):
        condition += 'and lower(TRIM(tipo_da_deficiencia_meta)) like %s'
        params.append('%'+ filters['deficiencia'] + '%') 
    if filters.get('start_date'):
        condition_group += " and MAX(DATE(CONVERT_TZ(created_at, '+00:00', '-04:00'))) >= %s "
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition_group += " and MAX(DATE(CONVERT_TZ(created_at, '+00:00', '-04:00'))) <= %s "
        params.append(filters['end_date'])
    if filters.get('especific_date'):
        condition_group += " and MAX(DATE(CONVERT_TZ(created_at, '+00:00', '-04:00'))) = %s "
        params.append(filters['especific_date'])

    params.append(filters['fim'])
    params.append(filters['inicio'])
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition ,conditions_group=condition_group ,order=order), params)
    requests = cursor.fetchall()

    return [HashRequest(*req) for req in requests]

def get_count_cpf_hash(filters: dict) -> List[CountHashRequest]:

    query = Queries.get_count_cpf_hash
    condition = ''
    params = []

    if filters.get('view'):
        view = filters['view']
        if view == 'solicitacao':
            condition += "statusId in (2, 21)"
        else:
            condition += "statusId in (6, 25)"
    if filters.get('nome'):
        condition += " and lower(benef_nome) like %s"
        params.append('%' + filters['nome'] + '%')
    if filters.get('nome_responsavel'):
        condition += " and lower(resp_nome) like %s"
        params.append('%' + filters['nome_responsavel'] + '%')
    if filters.get('cpf'):
        condition += " and benef_cpf like %s"
        params.append(filters['cpf'])
    if filters.get('alert_id'):
        condition += "and alert_id in (%s)"
        params.append(filters['alert_id'])
    if filters.get('projeto'):
        projeto = filters['projeto']
        if projeto == 'PCD':
            condition += "and (channelId like '%4495%' or channelId like '%4499%' or channelId like '%12836%')"
        elif projeto == 'CIPTEA':
            condition += "and (channelId like '%6744%' or channelId like '%6790%' or channelId like '%12837%')"
        else:
            condition += 'null'
    if filters.get('via'):
        condition += " and tipo_carteira=%s "
        params.append(filters['via'])
    if filters.get('municipio_realizado_cadastro'):
        condition += 'and lower(municipio_realizado_cadastro_meta) like %s'
        params.append('%'+ filters['municipio_realizado_cadastro'] + '%')
    if filters.get('local_de_retirada'):
        condition += 'and lower(local_de_retirada_meta) like %s'
        params.append('%'+ filters['local_de_retirada'] + '%')
    if filters.get('cid'):
        condition += 'and lower(cid) like %s'
        params.append('%'+ filters['cid'] + '%')
    if filters.get('deficiencia'):
        condition += 'and lower(TRIM(tipo_da_deficiencia_meta)) like %s'
        params.append('%'+ filters['deficiencia'] + '%')
    if filters.get('start_date'):
        condition += " and DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) >= %s "
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition += " and DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) <= %s "
        params.append(filters['end_date'])
    if filters.get('especific_date'):
        condition += " and DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) = %s "
        params.append(filters['especific_date'])

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition), params)
    requests = cursor.fetchall()

    return [CountHashRequest(*req) for req in requests]

def get_arquivados(filters: dict) -> List[HashRequest]:

    query = Queries.get_arquivados
    params = []
    order = filters['order']
    condition = ''
    condition_group = ''
    status_condition = ''
    
    if filters.get('status'):
        status_condition = "({})".format(", ".join(["%s"] * len(filters['status'])))
        params.extend(filters['status'])
    if filters.get('nome'):
        condition += " and lower(s.benef_nome) like %s"
        params.append('%' + filters['nome'] + '%')
    if filters.get('nome_responsavel'):
        condition += 'and lower(s.resp_nome) like %s'
        params.append('%'+ filters['nome_responsavel'] + '%')
    if filters.get('cid'):
        condition += 'and lower(s.cid) like %s'
        params.append('%'+ filters['s.cid'] + '%')
    if filters.get('cpf'):
        condition += " and s.benef_cpf like %s"
        params.append(filters['cpf'])
    if filters.get('alert_id'):
        condition += "and s.alert_id in (%s)"
        params.append(filters['alert_id'])
    if filters.get('projeto'):
        projeto = filters['projeto']
        if projeto == 'PCD':
            condition += "and (s.channelId like '%4495%' or s.channelId like '%4499%' or s.channelId like '%12836%')"
        elif projeto == 'CIPTEA':
            condition += "and (s.channelId like '%6744%' or s.channelId like '%6790%' or s.channelId like '%12837%')"
        else:
            condition += 'null'
    if filters.get('via'):
        condition += " and s.tipo_carteira=%s "
        params.append(filters['via'])
    if filters.get('municipio_realizado_cadastro'):
        condition += 'and lower(s.municipio_realizado_cadastro_meta) like %s'
        params.append('%'+ filters['municipio_realizado_cadastro'] + '%')
    if filters.get('local_de_retirada'):
        condition += 'and lower(s.local_de_retirada_meta) like %s'
        params.append('%'+ filters['local_de_retirada'] + '%')
    if filters.get('deficiencia'):
        condition += 'and lower(s.tipo_da_deficiencia_meta) like %s'
        params.append('%'+ filters['deficiencia'] + '%') 
    if filters.get('start_date'):
        condition_group += " and MAX(DATE(CONVERT_TZ(s.created_at, '+00:00', '-04:00'))) >= %s "
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition_group += " and MAX(DATE(CONVERT_TZ(s.created_at, '+00:00', '-04:00'))) <= %s "
        params.append(filters['end_date'])
    if filters.get('especific_date'):
        condition_group += " and MAX(DATE(CONVERT_TZ(s.created_at, '+00:00', '-04:00'))) = %s "
        params.append(filters['especific_date'])

    params.append(filters['fim'])
    params.append(filters['inicio'])
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(status_condition=status_condition, conditions=condition ,conditions_group=condition_group ,order=order), params)
    requests = cursor.fetchall()

    return [HashRequestArquivados(*req) for req in requests]

def get_count_arquivados(filters: dict) -> List[CountHashRequest]:

    query = Queries.get_count_cpf_hash
    condition = ''
    params = []

    if filters.get('status'):
        condition += "statusId in ({})".format(", ".join(["%s"] * len(filters.get('status'))))
        for i in filters.get('status'):
            params.append(i)
    if filters.get('nome'):
        condition += " and lower(benef_nome) like %s"
        params.append('%' + filters['nome'] + '%')
    if filters.get('nome_responsavel'):
        condition += " and lower(resp_nome) like %s"
        params.append('%' + filters['nome_responsavel'] + '%')
    if filters.get('cpf'):
        condition += " and benef_cpf like %s"
        params.append(filters['cpf'])
    if filters.get('alert_id'):
        condition += "and alert_id in (%s)"
        params.append(filters['alert_id'])
    if filters.get('projeto'):
        projeto = filters['projeto']
        if projeto == 'PCD':
            condition += "and (channelId like '%4495%' or channelId like '%4499%' or channelId like '%12836%')"
        elif projeto == 'CIPTEA':
            condition += "and (channelId like '%6744%' or channelId like '%6790%' or channelId like '%12837%')"
        else:
            condition += 'null'
    if filters.get('via'):
        condition += " and tipo_carteira=%s "
        params.append(filters['via'])
    if filters.get('municipio_realizado_cadastro'):
        condition += 'and lower(municipio_realizado_cadastro_meta) like %s'
        params.append('%'+ filters['municipio_realizado_cadastro'] + '%')
    if filters.get('local_de_retirada'):
        condition += 'and lower(local_de_retirada_meta) like %s'
        params.append('%'+ filters['local_de_retirada'] + '%')
    if filters.get('deficiencia'):
        condition += 'and lower(TRIM(tipo_da_deficiencia_meta)) like %s'
        params.append('%'+ filters['deficiencia'] + '%')
    if filters.get('start_date'):
        condition += " and DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) >= %s "
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition += " and DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) <= %s "
        params.append(filters['end_date'])
    if filters.get('especific_date'):
        condition += " and DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) = %s "
        params.append(filters['especific_date'])

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition), params)
    requests = cursor.fetchall()

    return [CountHashRequest(*req) for req in requests]

def get_consulta_geral(filters: dict) -> List[ConsultaGeralRequest]:

    query = Queries.get_consulta_geral
    params = []
    order = filters['order']
    condition = ''

    if filters.get('filtro'):
        filtro = filters['filtro']
        if filtro == 'alert_id':
            condition += "alert_id in (%s)"
            params.append(filters['alert_id'])
        elif filtro == 'benef_cpf':
            condition += "benef_cpf like %s"
            params.append(filters['benef_cpf'])
        elif filtro == 'benef_nome':
            condition += "lower(benef_nome) like %s"
            params.append('%' + filters['benef_nome'] + '%')
        elif filtro == 'cid':
            condition+= "cid like %s"
            params.append('%'+filters['cid']+'%')
        else:
            condition += 'null'


    params.append(filters['fim'])
    params.append(filters['inicio'])
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition, order=order), params)
    requests = cursor.fetchall()

    return [ConsultaGeralRequest(*req) for req in requests]

def get_count_consulta_geral(filters: dict) -> List[CountConsultaGeralRequest]:

    query = Queries.get_count_consulta_geral
    params = []
    condition = ''

    if filters.get('filtro'):
        filtro = filters['filtro']
        if filtro == 'alert_id':
            condition += "alert_id in (%s)"
            params.append(filters['alert_id'])
        elif filtro == 'benef_cpf':
            condition += "benef_cpf like %s"
            params.append(filters['benef_cpf'])
        elif filtro == 'benef_nome':
            condition += "lower(benef_nome) like %s"
            params.append('%' + filters['benef_nome'] + '%')
        elif filtro == 'cid':
            condition += 'cid like %s'
            params.append('%'+filters['cid'+'%'])
        else:
            condition += 'null'

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition), params)
    requests = cursor.fetchall()

    return [CountConsultaGeralRequest(*req) for req in requests]


def get_solicitation_hashid(benef_cpf: str) -> List[SolicitationHashId]:

    query = Queries.get_solicitacao_hashid
    params = [benef_cpf]
    # benef_cpf = 'benef_cpf'

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    requests = cursor.fetchall()

    return [SolicitationHashId(*req) for req in requests]

def get_aprovados_alert_id(hash_id: str):
    query = Queries.get_aprovados_ciptea_alert_id
    params = [hash_id]

    conn = get_conn()
    cursor= conn.cursor()
    cursor.execute(query, params)
    requests = cursor.fetchall()
    return [AprovadoAlertId(*req) for req in requests]

def get_solicitacoes(filters: dict) -> List[SolicitationRequest]:

    query = Queries.get_solicitacoes
    condition = ''
    params = []
    order = filters.get('order')

    if filters.get('status'):
        condition += " and statusId in ({})".format(", ".join(["%s"] * len(filters.get('status'))))
        for i in filters.get('status'):
            params.append(i)
    if filters.get('alert_id'):
        condition += ' and alert_id=%s'
        params.append(filters['alert_id'])
    if filters.get('cpf'):
        condition += " and benef_cpf like %s"
        params.append(filters['cpf'])
    if filters.get('hashId'):
        condition += " and hashId=%s "
        params.append(filters['hashId'])
    if filters.get('nome'):
        condition += " and lower(benef_nome) like %s"
        params.append('%'+filters['nome']+'%')
    if filters.get('nome_responsavel'):
        condition += " and lower(resp_nome) like %s"
        params.append('%'+filters['nome_responsavel']+'%')
    if filters.get('cid'):
        condition += " and lower(cid) like %s"
        params.append('%'+filters['cid']+'%')
    if filters.get('deficiencia'):
        condition += " and lower(TRIM(tipo_da_deficiencia_meta)) like %s"
        params.append('%'+filters['deficiencia']+'%')
    if filters.get('local_retirada'):
        condition += " and lower(local_de_retirada_meta) like %s"
        params.append('%'+filters['local_retirada']+'%')
    if filters.get('municipio'):
        condition += " and lower(municipios_endereco_beneficiario_meta) like %s"
        params.append('%'+filters['municipio']+'%')
    if filters.get('projeto'):
        projeto = filters['projeto']
        if projeto == 'PCD':
            condition += " and channelId in (12836, 4499, 4495)"
        else:
            condition += " and channelId in (12837, 6790, 6744)"
    if filters.get('start_date'):
        condition += f" and DATE(CONVERT_TZ({filters['orientation_date']}, '+00:00', '-04:00')) >= %s"
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition += f" and DATE(CONVERT_TZ({filters['orientation_date']}, '+00:00', '-04:00')) <= %s"
        params.append(filters['end_date'])
    
    params.append(filters['fim'])
    params.append(filters['inicio'])
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition, order=order), params)
    requests = cursor.fetchall()

    return [SolicitationRequest(*req) for req in requests]


def get_solicitacao_alert(filters: dict) -> List[SolicitationAlertRequest]:

    query = Queries.get_solicitacao_alert
    condition = ''
    params = []

    if filters.get('hashId'):
        condition += "hashId = %s"
        params.append(filters['hashId'])
    if filters.get('alert_id'):
        condition += ' and alert_id=%s'
        params.append(filters['alert_id'])

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition), params)
    requests = cursor.fetchall()

    return [SolicitationAlertRequest(*req) for req in requests]

def get_solicitation_meta_by_alert_id(alert_id: int):
    query = Queries.get_solicitation_meta_by_alert_id
    params = [alert_id]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    requests = cursor.fetchall()

    return [SolicitationMetaByAlertId(*req) for req in requests]

def get_solicitation_old_by_cpf(cpf: str) -> List[SolicitationOldByCPF]:
    query = Queries.get_solicitation_old_by_cpf
    params = [cpf]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    requests = cursor.fetchall()

    return [SolicitationOldByCPF(*req) for req in requests]

def get_count_solicitacoes(filters: dict) -> List[CountSolicitationRequest]:

    query = Queries.get_count_solicitacoes
    condition = ''
    params = []

    if filters.get('status'):
        condition += " and statusId in ({})".format(", ".join(["%s"] * len(filters.get('status'))))
        for i in filters.get('status'):
            params.append(i)
    if filters.get('alert_id'):
        condition += ' and alert_id=%s'
        params.append(filters['alert_id'])
    if filters.get('cpf'):
        condition += " and benef_cpf like %s"
        params.append(filters['cpf'])
    if filters.get('hashId'):
        condition += " and hashId=%s "
        params.append(filters['hashId'])
    if filters.get('nome'):
        condition += " and lower(benef_nome) like %s"
        params.append('%'+filters['nome']+'%')
    if filters.get('cid'):
        condition += " and lower(cid) like %s"
        params.append('%'+filters['cid']+'%')
    if filters.get('deficiencia'):
        condition += " and lower(TRIM(tipo_da_deficiencia_meta)) like %s"
        params.append('%'+filters['deficiencia']+'%')
    if filters.get('local_retirada'):
        condition += " and lower(local_de_retirada_meta) like %s"
        params.append('%'+filters['local_retirada']+'%')
    if filters.get('municipio'):
        condition += " and lower(municipios_endereco_beneficiario_meta) like %s"
        params.append('%'+filters['municipio']+'%')
    if filters.get('projeto'):
        projeto = filters['projeto']
        if projeto == 'PCD':
            condition += " and channelId in (12836, 4499, 4495)"
        else:
            condition += " and channelId in (12837, 6790, 6744)"
    if filters.get('start_date'):
        condition += f" and DATE(CONVERT_TZ({filters['orientation_date']}, '+00:00', '-04:00')) >= %s"
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition += f" and DATE(CONVERT_TZ({filters['orientation_date']}, '+00:00', '-04:00')) <= %s"
        params.append(filters['end_date'])

    params.append(filters['fim'])
    params.append(filters['inicio'])
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition), params)
    requests = cursor.fetchall()

    return [CountSolicitationRequest(*req) for req in requests]

def get_aprovados_pcd(filters: dict) -> List[ApprovedRequest]:

    query = Queries.get_aprovados
    params = []
    order = filters['order']
    condition = ''

    if filters.get('status'):
        condition += "a.statusId in ({})".format(", ".join(["%s"] * len(filters.get('status'))))
        for i in filters.get('status'):
            params.append(i)
    if filters.get('alert_id'):
        condition += ' and a.alert_id=%s'
        params.append(filters['alert_id'])
    if filters.get('cpf'):
        condition += " and a.cpf like %s"
        params.append(filters['cpf'])
    if filters.get('nome'):
        condition += " and lower(a.nome) like %s"
        params.append('%'+filters['nome']+'%')
    if filters.get('municipio'):
        condition += " AND LOWER(a.municipios_beneficiario_meta) LIKE %s"
        params.append("%" + filters['municipio'].lower() + "%")
    if filters.get('local_de_retirada'):
        condition += " AND LOWER(s.local_de_retirada_meta) LIKE %s"
        params.append("%" + filters['local_de_retirada'].lower() + "%")
    if filters.get('carteira'):
        condition += " and a.numero_carteira = %s"
        params.append(filters['carteira'])
    if filters.get('start_date'):
        condition += f" and DATE(CONVERT_TZ(a.{filters['orientation_date']}, '+00:00', '-04:00')) >= %s"
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition += f" and DATE(CONVERT_TZ(a.{filters['orientation_date']}, '+00:00', '-04:00')) <= %s"
        params.append(filters['end_date'])

    params.append(filters['fim'])
    params.append(filters['inicio'])
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(projeto='aprovados_pcd', order=order, conditions=condition), params)
    requests = cursor.fetchall()
    return [ApprovedRequest(*req) for req in requests]

def get_aprovados_ciptea(filters: dict) -> List[ApprovedRequest]:

    query = Queries.get_aprovados
    params = []
    order = filters['order']
    condition = ''

    if filters.get('status'):
        condition += "a.statusId in ({})".format(", ".join(["%s"] * len(filters.get('status'))))
        for i in filters.get('status'):
            params.append(i)
    if filters.get('alert_id'):
        condition += ' and a.alert_id=%s'
        params.append(filters['alert_id'])
    if filters.get('cpf'):
        condition += " and a.cpf like %s"
        params.append(filters['cpf'])
    if filters.get('nome'):
        condition += " and lower(a.nome) like %s"
        params.append('%'+filters['nome']+'%')
    if filters.get('municipio'):
        condition += " AND LOWER(a.municipios_beneficiario_meta) LIKE %s"
        params.append("%" + filters['municipio'].lower() + "%")
    if filters.get('local_de_retirada'):
        condition += " AND LOWER(s.local_de_retirada_meta) LIKE %s"
        params.append("%" + filters['local_de_retirada'].lower() + "%")
    if filters.get('carteira'):
        condition += " and a.numero_carteira = %s"
        params.append(filters['carteira'])
    if filters.get('start_date'):
        condition += f" and DATE(CONVERT_TZ(a.{filters['orientation_date']}, '+00:00', '-04:00')) >= %s"
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition += f" and DATE(CONVERT_TZ(a.{filters['orientation_date']}, '+00:00', '-04:00')) <= %s"
        params.append(filters['end_date'])
        
    params.append(filters['fim'])
    params.append(filters['inicio'])
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(projeto='aprovados_ciptea', order=order, conditions=condition), params)
    requests = cursor.fetchall()
    return [ApprovedRequest(*req) for req in requests]

def get_count_aprovados_pcd(filters: dict) -> List[CountApprovedRequest]:

    query = Queries.get_count_aprovados
    params = []
    condition = ''

    if filters.get('status'):
        condition += "a.statusId in ({})".format(", ".join(["%s"] * len(filters.get('status'))))
        for i in filters.get('status'):
            params.append(i)
    if filters.get('alert_id'):
        condition += ' and a.alert_id=%s'
        params.append(filters['alert_id'])
    if filters.get('cpf'):
        condition += " and a.cpf like %s"
        params.append(filters['cpf'])
    if filters.get('nome'):
        condition += " and lower(a.nome) like %s"
        params.append('%'+filters['nome']+'%')
    if filters.get('carteira'):
        condition += " and a.numero_carteira = %s"
        params.append(filters['carteira'])
    if filters.get('municipio'):
        condition += " AND LOWER(a.municipios_beneficiario_meta) LIKE %s"
        params.append("%" + filters['municipio'].lower() + "%")
    if filters.get('local_de_retirada'):
        condition += " AND LOWER(s.local_de_retirada_meta) LIKE %s"
        params.append("%" + filters['local_de_retirada'].lower() + "%")
    if filters.get('start_date'):
        condition += f" and DATE(CONVERT_TZ(a.{filters['orientation_date']}, '+00:00', '-04:00')) >= %s"
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition += f" and DATE(CONVERT_TZ(a.{filters['orientation_date']}, '+00:00', '-04:00')) <= %s"
        params.append(filters['end_date'])
    if filters.get('id'):
        condition += " and a.id > %s"
        params.append(filters['id'])

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(projeto='aprovados_pcd', conditions=condition), params)
    requests = cursor.fetchall()
    return [CountApprovedRequest(*req) for req in requests]

def get_lote(filters: dict) -> List[LoteRequest]:

    query = Queries.get_lotes
    params = []
    order = filters['order']
    condition = ''

    if filters.get('projeto'):
        projeto = filters['projeto']
        if projeto == 'PCD':
            projeto = 'aprovados_pcd'
        else:
            projeto = 'aprovados_ciptea'
    if filters.get('lote'):
        condition += " and lote = %s"
        params.append(filters['lote'])
    if filters.get('nome'):
        condition += " and lower(nome) like %s"
        params.append('%' + filters['nome'] + '%')
    if filters.get('cpf'):
        condition += " and cpf like %s"
        params.append(filters['cpf'])
    if filters.get('alert_id'):
        condition += " and alert_id = %s"
        params.append(filters['alert_id'])
    if filters.get('statusId'):
        condition += " and statusId = %s"
        params.append(filters['statusId'])

    params.append(filters['fim'])
    params.append(filters['inicio'])
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(projeto=projeto, conditions=condition, order=order), params)
    requests = cursor.fetchall()

    return [LoteRequest(*req) for req in requests]

def get_count_lote(filters: dict) -> List[CountLote]:

    query = Queries.get_count_lotes
    params = []
    condition = ''

    if filters.get('projeto'):
        projeto = filters['projeto']
        if projeto == 'PCD':
            projeto = 'aprovados_pcd'
        else:
            projeto = 'aprovados_ciptea'
    if filters.get('lote'):
        condition += " and lote = %s"
        params.append(filters['lote'])
    if filters.get('nome'):
        condition += " and lower(nome) like %s"
        params.append('%' + filters['nome'] + '%')
    if filters.get('cpf'):
        condition += " and cpf like %s"
        params.append(filters['cpf'])
    if filters.get('alert_id'):
        condition += " and alert_id = %s"
        params.append(filters['alert_id'])
    if filters.get('statusId'):
        condition += " and statusId = %s"
        params.append(filters['statusId'])

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition, projeto=projeto), params)
    requests = cursor.fetchall()

    return [CountLote(*req) for req in requests]

def get_lote_alert(filters: dict) -> List[LoteAlertsRequest]:

    query = Queries.get_lote_alerts
    params = []
    condition = ''

    if filters.get('projeto'):
        projeto = filters['projeto']
        if projeto == 'PCD':
            projeto = 'aprovados_pcd'
        else:
            projeto = 'aprovados_ciptea'
    if filters.get('lote'):
        condition += " and lote = %s"
        params.append(filters['lote'])
    if filters.get('nome'):
        condition += " and lower(nome) like %s"
        params.append('%' + filters['nome'] + '%')
    if filters.get('cpf'):
        condition += " and cpf like %s"
        params.append(filters['cpf'])
    if filters.get('alert_id'):
        condition += " and alert_id = %s"
        params.append(filters['alert_id'])

    params.append(filters['fim'])
    params.append(filters['inicio'])
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition, projeto=projeto), params)
    requests = cursor.fetchall()

    return [LoteAlertsRequest(*req) for req in requests]

def get_last_lote (projeto: str)-> List[LastNumberLote]:

    query = Queries.get_last_lote
    params = []
    if projeto == 'PCD':
        projeto = 'aprovados_pcd'
    else:
        projeto = 'aprovados_ciptea'
    # projeto = 'aprovados_pcd' if projeto == 'PCD' else 'aprovados_ciptea'

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(projeto=projeto), params)
    requests = cursor.fetchall()
    return [LastNumberLote(*req) for req in requests]

def get_lote_xlsx(lote:int):
    query = Queries.get_lote_xlsx
    params = [lote]
    
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()

    df = pd.DataFrame(result)

    df.columns = [
            'Número carteira', 'Lote', 'Nome do beneficiário', 'CPF', 'RG', 'CID', 'Data de nascimento', 
            'Telefone beneficiário', 'Tipo sanguíneo', 'Naturalidade', 'Municipio', 'Data de expedição', 'Data de validade', 
            'Endereço do beneficiário', 'Filiação Mãe', 'Filiação Pai', 'Nome do responsável', 'RG do responsável', 
            'Telefone responsável', 'Endereço do responsável', 'Foto 3X4', 'Foto digital', 'URL do QRCODE', 'Via', 'E-mail'
        ]

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    buffer.seek(0)

    return buffer

def solicitacoes_xlsx(filters:dict):
    query = Queries.get_solicitacoes_xlsx
    params = []
    condition = ''  # Nova variável para condições do histórico

    if filters.get('status'):
        condition += " and statusId in ({})".format(", ".join(["%s"] * len(filters.get('status'))))
        for i in filters.get('status'):
            params.append(i)
    if filters.get('carteira') and len(filters['carteira'].split(',')) != 2:
        condition += "and channelId = %s"
        if(filters['carteira'] == 'PCD'):
            params.append(12836)
        else:
            params.append(12837)
    if filters.get('cid'):
        cids = filters['cid'].split(',')
        condition += " AND (" + " OR ".join([f'cid LIKE %s' for _ in cids]) + ")"
        params.extend([f'%{cid.strip()}%' for cid in cids])
    if filters.get('start_date'):
        condition += " and DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) >= %s"
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition += " and DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) <= %s"
        params.append(filters['end_date'])

    # Condições restantes para a variável condition
    if filters.get('naturalidade'):
        condition += " and municipios_naturalidade_meta LIKE %s"
        params.append('%' + filters['naturalidade'] + '%')
    if filters.get('deficiencia'):
        deficiencias = filters['deficiencia'].split(',')
        deficiencias = [d.strip() for d in deficiencias]
        condition += " and TRIM(tipo_da_deficiencia_meta) IN ({})".format(", ".join(["%s"] * len(deficiencias)))
        params.extend(deficiencias)
    if filters.get('municipio'):
        condition += " and municipios_endereco_beneficiario_meta LIKE %s"
        params.append('%' + filters['municipio'] + '%')
    
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition), params)
    result = cursor.fetchall()
    df = pd.DataFrame(result)

    df.columns = [
            'Protocolo', 'CPF do Beneficiario', 'Nome do Beneficiário', 'RG do Beneficiário', 'CID do Beneficiário', 'Deficiência do Beneficiário', 'Naturalidade do Beneficiário', 'Nome da Mãe', 
            'Nome do Pai', 'Tipo Sanguíneo', 'Data de Nascimento', 'Genêro do Beneficiário', 'Estado Civil', 
            'Nacionalidade', 'Orgão Expedidor', 'Município', 'Tipo Carteira', 'Motivo da 2ª via', 
            'Local de Retirada', 'Endereço do Beneficiário', 'Nome do Responsável', 'CPF do Responsável', 'RG do Responsável', 'Email do Responsável', 'Endereço do Responsável',
            'Status', 'Canal', 'Recebido', 'Última Modificação']
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    buffer.seek(0)

    return buffer
def visual_export(filters: dict) -> List[VisualExportResponse]:
    query = Queries.get_visual_export
    params = []
    condition = ''  # Nova variável para condições do histórico

    if filters.get('status'):
        condition += " and statusId in ({})".format(", ".join(["%s"] * len(filters.get('status'))))
        for i in filters.get('status'):
            params.append(i)
    if filters.get('carteira') and len(filters['carteira'].split(',')) != 2:
        condition += "and channelId = %s"
        if(filters['carteira'] == 'PCD'):
            params.append(12836)
        else:
            params.append(12837)
    if filters.get('cid'):
        cids = filters['cid'].split(',')
        condition += " AND (" + " OR ".join([f'cid LIKE %s' for _ in cids]) + ")"
        params.extend([f'%{cid.strip()}%' for cid in cids])
    if filters.get('start_date'):
        condition += " and DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) >= %s"
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition += " and DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) <= %s"
        params.append(filters['end_date'])

    # Condições restantes para a variável condition
    if filters.get('naturalidade'):
        condition += " and municipios_naturalidade_meta LIKE %s"
        params.append('%' + filters['naturalidade'] + '%')
    if filters.get('deficiencia'):
        deficiencias = filters['deficiencia'].split(',')
        deficiencias = [d.strip() for d in deficiencias]
        condition += " and TRIM(tipo_da_deficiencia_meta) IN ({})".format(", ".join(["%s"] * len(deficiencias)))
        params.extend(deficiencias)
    if filters.get('municipio'):
        condition += " and municipios_endereco_beneficiario_meta LIKE %s"
        params.append('%' + filters['municipio'] + '%')

    params.append(filters['fim'])
    params.append(filters['inicio'])
    
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition), params)
    requests = cursor.fetchall()

    # Convertendo tuplas em instâncias de VisualExportResponse
    return [VisualExportResponse(*req) for req in requests]  # Certifique-se de que VisualExportResponse tenha os atributos corretos

def count_visual_export(filters: dict) -> int:
    query = Queries.get_count_visual_export
    params = []
    condition = ''  # Nova variável para condições do histórico

    if filters.get('status'):
        condition += " and statusId in ({})".format(", ".join(["%s"] * len(filters.get('status'))))
        for i in filters.get('status'):
            params.append(i)
    if filters.get('carteira') and len(filters['carteira'].split(',')) != 2:
        condition += "and channelId = %s"
        if(filters['carteira'] == 'PCD'):
            params.append(12836)
        else:
            params.append(12837)
    if filters.get('cid'):
        cids = filters['cid'].split(',')
        condition += " AND (" + " OR ".join([f'cid LIKE %s' for _ in cids]) + ")"
        params.extend([f'%{cid.strip()}%' for cid in cids])
    if filters.get('start_date'):
        condition += " and DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) >= %s"
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition += " and DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) <= %s"
        params.append(filters['end_date'])

    # Condições restantes para a variável condition
    if filters.get('naturalidade'):
        condition += " and municipios_naturalidade_meta LIKE %s"
        params.append('%' + filters['naturalidade'] + '%')
    if filters.get('deficiencia'):
        deficiencias = filters['deficiencia'].split(',')
        deficiencias = [d.strip() for d in deficiencias]
        condition += " and TRIM(tipo_da_deficiencia_meta) IN ({})".format(", ".join(["%s"] * len(deficiencias)))
        params.extend(deficiencias)
    if filters.get('municipio'):
        condition += " and municipios_endereco_beneficiario_meta LIKE %s"
        params.append('%' + filters['municipio'] + '%')
    
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition), params)
    count = cursor.fetchall()

    return [CountVisualExportResponse(*req) for req in count]
    

def validar_campos_carteira(hashId: str)-> List[ValidarCarteiraHashId]:
    query = Queries.get_valida_carteira
    params = [hashId]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()

    return[ValidarCarteiraHashId(*res) for res in result]

def get_carteira_virtual(filters: dict) -> List[CarteiraRequest]:

    query = Queries.get_carteira_virtual
    params = []
    condition = ''

    if filters['projeto'] == 'PCD':
        projeto = 'aprovados_pcd'
    else:
        projeto = 'aprovados_ciptea'
    if filters.get('hashId'):
        condition += " hashId = %s"
        params.append(filters['hashId'])

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(projeto=projeto, conditions=condition), params)
    requests = cursor.fetchall()

    return [CarteiraRequest(*req) for req in requests]

def get_last_number_pcd ()-> List[LastNumberApproved]:

    query = Queries.get_last_number
    params = []

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(projeto='aprovados_pcd'), params)
    requests = cursor.fetchall()
    return [LastNumberApproved(*req) for req in requests]

def get_last_number_ciptea ()-> List[LastNumberApproved]:

    query = Queries.get_last_number
    params = []

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(projeto='aprovados_ciptea'), params)
    requests = cursor.fetchall()
    return [LastNumberApproved(*req) for req in requests]

# teste rere
def get_informations_carteirinha(alert_id: int, tipo_carteirinha:str):
    if tipo_carteirinha.upper() == 'PCD':
        query = Queries.get_informations_carteirinha_pcd
        params = [alert_id]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(query, params)
        requests = cursor.fetchall()

        informations_dict = InformationsCarteirinhaPCD.serialize_pessoas(requests)
    
    elif tipo_carteirinha.upper() == 'CIPTEA':
        query = Queries.get_informations_carteirinha_ciptea
        params = [alert_id]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(query, params)
        requests = cursor.fetchall()

        informations_dict = InformationsCarteirinhaCIPTEA.serialize_pessoas(requests)


    return informations_dict


def get_aproved_ciptea(alert_id: int):
    query = Queries.get_aproved_ciptea
    params = [alert_id]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    requests = cursor.fetchall()
    conn.close()

    return [AprovedCIPTEA(*req) for req in requests]

def get_attachments_alert_id(alert_id: int):
    query = Queries.get_attachments
    params = [alert_id]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
   
    
    attachments_json = result[0]
    attachments_data = json.loads(attachments_json)


    chaves_base = ['doc_foto_3_x_4_beneficiario_anexo', 'doc_foto_3x_4_beneficiario_anexo', 'doc_rg_do_beneficiario_frente_anexo', 'doc_rg_beneficiario_frente_anexo',
              'doc_rg_beneficiario_verso_anexo', 'doc_cpf_do_beneficiario_anexo', 'doc_cpf_beneficiario_anexo']
    
    chaves_validas = []
    for chave in chaves_base:
        if chave in attachments_data:
            chaves_validas.append(attachments_data[chave])

        flattened = [item for sublist in chaves_validas for item in sublist]
        lista_imagens = []
        extensions_images = ['jpg', 'png', 'jpeg']
        url_base = 'https://sa-east-1-uploads.s3.amazonaws.com/100760000427/attachments/image/{uuid}.{extension}'  
        for flat in flattened:
            for extension in extensions_images:
                url = url_base.format(uuid=flat, extension=extension)
                r = requests.head(url)
                if r.status_code == 200:
                    lista_imagens.append(url)
                    break
    return lista_imagens


def get_count_aprovados_ciptea(filters: dict) -> List[CountApprovedRequest]:

    query = Queries.get_count_aprovados
    params = []
    condition = ''

    if filters.get('status'):
        condition += "a.statusId in ({})".format(", ".join(["%s"] * len(filters.get('status'))))
        for i in filters.get('status'):
            params.append(i)
    if filters.get('alert_id'):
        condition += ' and a.alert_id=%s'
        params.append(filters['alert_id'])
    if filters.get('cpf'):
        condition += " and a.cpf like %s"
        params.append(filters['cpf'])
    if filters.get('nome'):
        condition += " and lower(a.nome) like %s"
        params.append('%'+filters['nome']+'%')
    if filters.get('carteira'):
        condition += " and a.numero_carteira = %s"
        params.append(filters['carteira'])
    if filters.get('municipio'):
        condition += " AND LOWER(a.municipios_beneficiario_meta) LIKE %s"
        params.append("%" + filters['municipio'].lower() + "%")
    if filters.get('local_de_retirada'):
        condition += " AND LOWER(s.local_de_retirada_meta) LIKE %s"
        params.append("%" + filters['local_de_retirada'].lower() + "%")
    if filters.get('start_date'):
        condition += f" and DATE(CONVERT_TZ(a.{filters['orientation_date']}, '+00:00', '-04:00')) >= %s"
        params.append(filters['start_date'])
    if filters.get('end_date'):
        condition += f" and DATE(CONVERT_TZ(a.{filters['orientation_date']}, '+00:00', '-04:00')) <= %s"
        params.append(filters['end_date'])
    if filters.get('id'):
        condition += " and a.id > %s"
        params.append(filters['id'])


    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(projeto='aprovados_ciptea', conditions=condition), params)
    requests = cursor.fetchall()
    return [CountApprovedRequest(*req) for req in requests]


def update_aprovados(
        projeto: str,
        parameters: dict,
        alert_ids: int):

    query = Queries.updates_aprovados
    params = []

    condition = ''
    if parameters.get('foto_3x4'):
        condition += ' foto_3x4 = %s,'
        params.append(parameters['foto_3x4'])
    if parameters.get('foto_digital'):
        condition += ' foto_digital = %s,'
        params.append(parameters['foto_digital'])
    if parameters.get('vencimento'):
        try: 
            data = datetime.strptime(parameters.get('vencimento'), '%Y-%m-%d %H:%M:%S')
            condition += ' vencimento = %s,'
            params.append(data)
        except: 
            pass
    if parameters.get('expedicao'):
        try: 
            data = datetime.strptime(parameters.get('expedicao'), '%Y-%m-%d %H:%M:%S')
            condition += ' expedicao = %s,'
            params.append(data)
        except: 
            pass
    if parameters.get('lote'):
        condition += ' lote = %s,'
        params.append(parameters['lote'])
    if parameters.get('nome'):
        condition += ' nome = %s,'
        params.append(parameters['nome'])
    if parameters.get('statusId'):
        condition += ' statusId = %s'
        params.append(parameters['statusId'])

    params.append(alert_ids)

    if projeto == 'PCD':
        query = query.format(projeto='aprovados_pcd', conditions=condition)
    else:
        query = query.format(projeto='aprovados_ciptea', conditions=condition)

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    return {"success": True}
    
def update_solicitacoes(alert_id: int, statusId: int, parameters: dict):

    query = Queries.update_solicitacoes
    condition = ''
    params = []

    condition += 'statusId = %s'
    params.append(statusId)

    if parameters.get('meta'):
        condition += ', meta = %s'
        params.append(json.dumps(parameters['meta']))
    if parameters.get('benef_rg'):
        condition += ', benef_rg = %s'
        params.append(parameters['benef_rg'])
    if parameters.get('benef_data_nasc'):
        condition += ', benef_data_nasc = %s'
        params.append(parameters['benef_data_nasc'])
    if parameters.get('benef_nome'):
        condition += ', benef_nome = %s'
        params.append(parameters['benef_nome'])
    if parameters.get('cid'):
        condition += ', cid = %s'
        params.append(parameters['cid'])
    if parameters.get('fator_rh'):
        condition += ', fator_rh = %s'
        params.append(parameters['fator_rh'])
    if parameters.get('resp_nome'):
        condition += ', resp_nome = %s'
        params.append(parameters['resp_nome'])
    if parameters.get('resp_rg'):
        condition += ', resp_rg = %s'
        params.append(parameters['resp_rg'])

    params.append(alert_id)

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition), params)
    conn.commit()
    return {"success": True}

def update_solicitacoes_teste(alert_id: int, statusId: int, auditor: str, motivo_reprovado: str, comentario_beneficiario: str, parameters: dict):
    
    # Esta parte serve para buscar as chaves que existem dentro do meta do alert no database
    requests = get_solicitation_meta_by_alert_id(alert_id)
    data = SolicitationMetaByAlertId.serialize_meta(requests=requests)
    keys_validates = json.loads(data[0]['meta']).keys()
    
    query = Queries.update_solicitacoes_teste
    condition = ""
    params = []
    params.append(statusId)
    params.append(auditor)
    
    # Esta parte serve para atualizar os campos que estão fora do meta
    if statusId == 33:
        condition+= '''tag_recurso = TRUE, '''

    if motivo_reprovado:
        condition+= '''motivo_reprovado = %s ,'''
        params.append(motivo_reprovado)

    if comentario_beneficiario:
            condition+= '''comentario_beneficiario = %s ,'''
            params.append(comentario_beneficiario)

    if "nome_do_beneficiario" in parameters.keys():
        condition+= '''benef_nome = %s ,'''
        params.append(parameters.get('nome_do_beneficiario'))

    if "rg_beneficiario" in parameters.keys():
        condition+= '''benef_rg = %s ,'''
        params.append(parameters.get('rg_beneficiario'))

    if "data_de_nascimento_beneficiario" in parameters.keys():
        condition+= '''benef_data_nasc = %s ,'''
        params.append(datetime.strptime(parameters.get('data_de_nascimento_beneficiario'), '%d/%m/%Y').date().isoformat())

    if "cid_beneficiario" in parameters.keys():
         condition+= '''cid = %s ,'''
         params.append(parameters.get('cid_beneficiario'))

    if "tipo_sanguineo_beneficiario" in parameters.keys():
        condition+='''fator_rh = %s,'''
        params.append(parameters.get('tipo_sanguineo_beneficiario'))

    if "nome_do_responsavel_legal_beneficiario" or "nome_responsavel_legal_do_beneficiario" in parameters.keys():
        condition+='''resp_nome = %s,'''
        if 'nome_do_responsavel_legal_beneficiario' in parameters.keys():
            params.append(parameters.get('nome_do_responsavel_legal_beneficiario'))
        else:
            params.append(parameters.get('nome_responsavel_legal_do_beneficiario'))

    if "rg_responsavel" in parameters.keys():
        condition+='''resp_rg = %s,'''
        params.append(parameters.get('rg_responsavel'))

    # Esta parte serve para verificar o que existe dentro do meta e fazer o update dos campos que existem
    keys_used = []
    index_used = []
    for index, key in enumerate(parameters.keys()):
        if key in keys_validates:
            keys_used.append(key)
            index_used.append(index)
    for chave in keys_used:
        condition+= '''meta = JSON_SET(meta, '$.{}', %s) ,'''.format(chave)
    for indexf, value in enumerate(parameters.values()):
        if indexf in index_used:
            params.append(value)

    params.append(alert_id)

    condition_strip = condition.strip(',')    
    
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition_strip),params)
    conn.commit()
    return {"success": True}

def insert_historicos(
        alert_id: int,
        nome: str,
        cpf: str,
        carteira: str,
        meta: dict,
        modified: dict,
        auditor: str,
        statusId: int,
        comentario:str):

    query = Queries.insert_historico
    params = [alert_id, nome, cpf, carteira, json.dumps(meta), json.dumps(modified), auditor, statusId, comentario]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    return {"success": True}

def insert_aprovados(
        projeto: str,
        alert_id: int,
        numero_carteira: int,
        nome: str,
        cpf: str,
        hashId: str,
        auditor: str,
        statusId: int,
        meta: dict):

    query = Queries.insert_aprovados_pcd if projeto == 'PCD' else Queries.insert_aprovados_ciptea
    params = [alert_id, numero_carteira, nome, cpf, hashId, auditor, statusId, json.dumps(meta)]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    return {"success": True}

def insert_num_carteiras(projeto: str, cpf: str, alert_id: int, via: int):
    
    params = [cpf, alert_id, via]
    params_2_via = [alert_id, cpf]

  
    if via == 2 and projeto.upper() == 'CIPTEA':
        query = Queries.insert_num_carteira_2_via_ciptea
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(query, params_2_via)
        conn.commit()
        return {"success": True}
    
    elif via == 2 and projeto.upper() == 'PCD':
        query = Queries.insert_num_carteira_2_via_pcd
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(query, params_2_via)
        conn.commit()
        return {"success": True}
    
    else:
        if projeto.upper() == 'PCD':
            query = Queries.insert_num_carteira_pcd
        elif projeto.upper() == 'CIPTEA':
            query = Queries.insert_num_carteira_ciptea
        else:
            return {'fail': 'não foi possível concluir a operação'}

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return {"success": True}

def get_request(alert_id) -> DocumentRequest | None:
  query = ""
  params = [alert_id]

  conn = get_conn()
  cursor = conn.cursor()
  cursor.execute(query, params)
  request = cursor.fetchone()

  if request is None:
    return None

  return DocumentRequest(*request)

def update_request(request: DocumentRequest):
  data = {
    "data": request.data,
    "attachments": request.attachments,
    "comments": request.comments,
  }

  query = Queries.update_request
  params = (json.dumps(data), request.status, request.external_id)

  print(request.status)
  print(request.external_id)

  conn = get_conn()
  cursor = conn.cursor()
  cursor.execute(query, params)
  conn.commit()

def get_produtividade(filters: dict) -> List[Produtividade]:
    query = Queries.get_produtividade
    condition = ''
    condition_date = ''
    params = []

    if filters['is_dev']:  # Verifica se é ambiente de desenvolvimento
        condition += 'auditor is not null'
    else:  # Se não for ambiente dev, estamos em produção
        condition += 'auditor NOT IN ("CLEUZIANE","GABRIEL MARTINS", "RAFAEL", "RAFAEL BRAGA", "", "THIAGO ROQUE")'
    
    if filters.get('auditor'):
        condition += ' AND auditor = %s'
        params.append(filters['auditor'])
    
    if filters.get('range_date'):
        condition_date += " AND DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) >= %s"
        condition_date += " AND DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) <= %s"
        for date in filters['range_date'].split(','):
            params.append(date)
    if filters.get('especific_date'):
        condition_date += " AND DATE(CONVERT_TZ(created_at, '+00:00', '-04:00')) = %s "
        params.append(filters['especific_date'])

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query.format(conditions=condition, conditions_date=condition_date), params)
    requests = cursor.fetchall()
    return [Produtividade(*req) for req in requests]

def getStatus_solicitacao(cpf: str, data_nascimento: str, projeto: str):
    channelIds = ''
    if projeto == 'PCD':
        channelIds = 'AND channelId IN (12836, 4499, 4495, 14057)'
    else:
        channelIds = 'AND channelId IN (12837, 6790, 6744, 13800)'

    # Converte a data de nascimento para o formato do banco de dados
    try:
        data_nascimento_formatada = datetime.strptime(data_nascimento, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        raise ValueError("Formato de data de nascimento inválido. Use dd/mm/aaaa.")
    
    condition = 'benef_cpf = %s AND benef_data_nasc = %s'

    # Consulta para buscar todas as solicitações do beneficiário
    query = Queries.get_status_solicitacao.format(conditions=condition, conditions_channel_ids=channelIds)
    params = [cpf, data_nascimento_formatada]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    solicitacoes = cursor.fetchall()

    # Verifica se há solicitações e seleciona a de maior prioridade
    if not solicitacoes:
        return None

    # Dicionário de prioridade dos statusId
    prioridade_status = {
        10: 0, 19: 0, 17: 0, 24: 1, 7: 1, 18: 1, 29: 1,
        9: 2, 23: 3, 27: 4, 22: 5, 5: 6, 31: 7, 3: 8, 13: 8,
        20: 8, 1: 9, 26: 10, 21: 11, 2: 12, 33: 13, 34: 14, 35: 15,
        32: 16, 6: 17, 25: 18, 28: 19, 4: 20, 8: 21
    }

    # Função para obter a prioridade do statusId
    def obter_prioridade(statusId):
        return prioridade_status.get(statusId, len(prioridade_status))

    # Modifique para retornar apenas um registro
    solicitacoes = [StatusSolicitacao(*solicitacao) for solicitacao in solicitacoes]

    # Ordena as solicitações pela prioridade do statusId
    solicitacoes.sort(key=lambda x: obter_prioridade(x.statusId))

    # Retorna a solicitação com maior prioridade
    return solicitacoes[0] if solicitacoes else None



