from typing import List
from typing import Annotated
from datetime import datetime
import io
import os

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.params import Body

from storage import *

from typing import Optional
from fastapi import FastAPI, HTTPException, Query, File, UploadFile, Request
from fastapi.responses import StreamingResponse

import json

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="Validador API - Swagger UI",
        oauth2_redirect_url='/docs/oauth2-redirect',
        init_oauth=None,
        swagger_ui_parameters=None
    )


def serialize_requests(requests):
    return [{
        "beneficiario_nome": r.name,
        "beneficiario_nome_mae": r.mother_name,
        "status_solicitacao": r.status,
        "data_solicitacao": r.created_at,
        "beneficiario_cid": r.cid,
        "beneficiario_cpf": r.cpf,
        "beneficiario_data_nascimento": r.birthdate,
        "protocolo_id": r.external_id,
        "total_anexos": r.total_attachments,
    } for r in requests]

def serialize_hash(requests):
    return [{
        'cpf': r.benef_cpf,
        'hashId': r.hashId,
        'nome': r.benef_nome,
        'nome_responsavel': r.resp_nome,
        'cid': r.cid,
        'deficiencia': r.tipo_da_deficiencia_meta,
        'municipio': r.municipio,
        'naturalidade': r.naturalidade,
        'idade': r.idade,
        'telefone_beneficiario': r.benef_telefone,
        'local_de_retirada': r.local_de_retirada,
        'alert_id': r.alert_id,
        'channelId': r.channelId,
        'last_created': r.last_created,
        'last_updated': r.last_updated,
        'count': r.total,
        'curatela_tutela': r.curatela_tutela
    } for r in requests]

def serialize_hash_arquivados(requests):
    return [{
        'cpf': r.benef_cpf,
        'hashId': r.hashId,
        'nome': r.benef_nome,
        'nome_responsavel': r.resp_nome,
        'cid': r.cid,
        'deficiencia': r.tipo_da_deficiencia_meta,
        'municipio': r.municipio,
        'auditor': r.auditor_arquivado,
        'naturalidade': r.naturalidade,
        'idade': r.idade,
        'telefone_beneficiario': r.benef_telefone,
        'local_de_retirada': r.local_de_retirada,
        'alert_id': r.alert_id,
        'channelId': r.channelId,
        'last_created': r.last_created,
        'last_updated': r.last_updated,
        'count': r.total,
        'curatela_tutela': r.curatela_tutela
    } for r in requests]

def serialize_count_hash(requests):
    return [{
        'count': r.count
    } for r in requests]

def serialize_consulta_geral(requests):
    return [{
        'benef_cpf': r.benef_cpf,
        'hashId': r.hashId,
        'benef_nome': r.benef_nome,
        'alert_id': r.alert_id,
        'deficiencia': r.deficiencia,
        'telefone': r.telefone,
        'local_de_retirada': r.local_de_retirada,
        'municipio': r.municipio,
        'cid': r.cid,
        'channelIds': r.channelIds,
        'last_created': r.last_created,
        'last_updated': r.last_updated,
        'count': r.total
    } for r in requests]

def serialize_count_consulta_geral(requests):
    return [{
        'count': r.count
    } for r in requests]

def serialize_history_requests(requests):
    return [{
        "id": r.id,
        "alert_id": r.alert_id,
        "carteira": r.carteira,
        "auditor": r.auditor,
        "meta": r.meta,
        "modified": r.modified,
        "status_id": r.statusId,
        "via": r.via,
        "created_at": r.created_at
    } for r in requests]


def serialize_approved_requests(requests):
    return [{
        "id": r.id,
        "alert_id": r.alert_id,
        "numero_carteira": r.numero_carteira,
        "nome": r.nome,
        "municipio_beneficiario": r.municipio_beneficiario,
        "cpf": r.cpf,
        "cid": r.cid, 
        "status": r.status,
        "deficiencia": r.deficiencia,
        "municipio": r.municipio,
        "local_de_retirada": r.local_de_retirada,
        "foto_3x4": r.foto_3x4,
        "foto_digital": r.foto_digital,
        "hashId": r.hashId,
        "vencimento": r.vencimento,
        "expedicao": r.expedicao,
        "lote": r.lote,
        "auditor": r.auditor,
        "statusId": r.statusId,
        "meta": r.meta,
        "via": r.via,
        "created_at": r.created_at,
        "updated_at": r.updated_at
    } for r in requests]

def serialize_count_approved_requests(requests):
    return [{
        'count': r.count
    } for r in requests]

def serialize_lote(requests):
    return [{
        "lote": r.lote,
        "total": r.total,
        "updated_at": r.updated_at,
        "statusId": r.statusId,
        "alert_id": r.alert_id,
        "numero_carteira": r.numero_carteira
    } for r in requests]

def serialize_count_lote(requests):
    return [{
        'count': r.count
    } for r in requests]

def serialize_count_project(requests):
    return [{
        'projeto': r.projeto,
        'total': r.total
    } for r in requests]

def serialize_count_municipio(requests):
    return [{
        'municipio': r.cad_municipio,
        'total': r.total
    } for r in requests]

def serialize_lote_alerts(requests):
    return [{
        "lote": r.lote,
        "nome": r.nome,
        "cpf": r.cpf,
        "alert_id": r.alert_id,
        "numero_carteira": r.numero_carteira,
        "foto_3x4": r.foto_3x4,
        "foto_digital": r.foto_digital,
        "hashId": r.hashId,
        "vencimento": r.vencimento,
        "expedicao": r.expedicao,
        "via": r.via_meta,
        "meta": r.meta,
        "created_at": r.created_at,
        "updated_at": r.updated_at,
        "email": r.email
    } for r in requests]

def serialize_validar_carteira(requests):
    return [{
        "numero_carteira": r.numero_carteira,
        "nome": r.nome,
        "cpf": r.cpf,
        "rg_beneficiario": r.rg_beneficiario_meta,
        "cid_beneficiario": r.cid_beneficiario_meta,
        "data_de_nascimento": r.data_de_nascimento,
        "telefone_beneficiario": r.telefone_beneficiario_meta,
        "tipo_sanguineo_beneficiario": r.tipo_sanguineo_beneficiario_meta,
        "naturalidade_beneficiario": r.naturalidade_beneficiario_meta,
        "expedicao": r.expedicao,
        "vencimento": r.vencimento,
        "endereco_beneficiario": r.endereco_beneficiario,
        "nome_da_mae": r.nome_da_mae_meta,
        "nome_do_pai": r.nome_do_pai_meta,
        "nome_responsavel_legal_do_beneficiario": r.nome_responsavel_legal_do_beneficiario_meta,
        "rg_responsavel": r.rg_responsavel_meta,
        "telefone_responsavel": r.telefone_responsavel_meta,
        "endereco_responsavel": r.endereco_responsavel,
        "foto_3x4": r.foto_3x4,
        "foto_digital": r.foto_digital,
        "url_qr_code": r.url_qr_code,
        "via": r.via_meta,
        "email": r.email_meta
    } for r in requests]


def serialize_last_number_approved(requests):
    return [{
        'last_number': r.last_number
    } for r in requests]

def serialize_last_number_lote(requests):
    return [{
        'last_lote': r.last_lote
    } for r in requests]

def serialize_carteira(requests):
    return [{
        "id": r.id,
        "alert_id": r.alert_id,
        "numero_carteira": r.numero_carteira,
        "nome": r.nome,
        "cpf": r.cpf,
        "foto_3x4": r.foto_3x4,
        "foto_digital": r.foto_digital,
        "hashId": r.hashId,
        "vencimento": r.vencimento,
        "expedicao": r.expedicao,
        "lote": r.lote,
        "auditor": r.auditor,
        "statusId": r.statusId,
        "meta": r.meta,
        "created_at": r.created_at,
        "updated_at": r.updated_at
    } for r in requests]

def serialize_solicitation_requests(requests):
    return [{
        "id": r.id,
        "alert_id": r.alert_id,
        "auditor": r.auditor,
        "nome_responsavel": r.resp_nome,
        "idade": r.idade,
        "cid": r.cid,
        "deficiencia": r.deficiencia,
        "local_retirada": r.local_retirada,
        "municipio_naturalidade": r.municipio_naturalidade,
        "municipios_endereco": r.municipios_endereco,
        "meta": r.meta,
        "attachments": r.attachments,
        "status_id": r.statusId,
        "channelId": r.channelId,
        "via": r.via,
        "external_id": r.external_id,
        "motivo_reprovado": r.motivo_reprovado,
        "comentario_beneficiario": r.comentario_beneficiario,
        "created_at": r.created_at,
        "updated_at": r.updated_at
    } for r in requests]

def serialize_solicitation_hashid(requests):
    return [{
        "hashId": r.hashId
    } for r in requests]

def serialize_aprovados_alert_id(requests):
    return[{
        "alert_id": r.alert_id
    }for r in requests]

def serialize_solicitation_alert_requests(requests):
    return [{
        "id": r.id,
        "alert_id": r.alert_id,
        "benef_cpf": r.benef_cpf,
        "meta": r.meta,
        "attachments": r.attachments,
        "status_id": r.statusId,
        "channelId": r.channelId,
        "via": r.via,
        "updated_at": r.updated_at,
        "created_at": r.created_at
    } for r in requests]

def serialize_visual_export(requests):
    return [{
        "alert_id": r.alert_id,
        "benef_nome": r.benef_nome,
        "municipio": r.municipios_endereco_beneficiario_meta,
        "deficiencia": r.tipo_da_deficiencia_meta,
        "statusId": r.statusId,
        "channelId": r.channelId,
        "updated_at": r.updated_at
    } for r in requests]

def serialize_count_visual_export(requests):
    return [{
        'count': r.count
    } for r in requests]

def serialize_last_solicitations(requests):
    return [{
        "alert_id": r.alert_id,
        "benef_nome": r.benef_nome,
        "cid": r.cid,
        "fator_rh": r.fator_rh,
        "projeto": r.channelId,
        "created_at": r.created_at
    } for r in requests]

def serialize_count_solicitation_requests(requests):
    return [{
        'count': r.count
    } for r in requests]


def serialize_attachements(attachments):
    atts = []
    for name, att_list in attachments.items():
        for idx in range(len(att_list)):
            atts.append({
                "name": name + "_" + str(idx),
                "attachment": att_list[idx],
            })
    return atts


def serialize_full_requests(requests):
    return [{
        "status_solicitacao": r.status,
        "data_solicitacao": r.created_at,
        "protocolo_id": r.external_id,
        "total_anexos": r.total_attachments,
        "data": r.data,
        "attachments": serialize_attachements(r.attachments),
        "comments": r.comments,
    } for r in requests]

def serialize_history_by_cpf(requests):
    return [{
        "alert_id": r.alert_id,
        "status_Id": r.statusId,
        "channelId": r.channelId,
        "tipo_carteira": r.tipo_carteira,
        "created_at": r.created_at,
        "auditor": r.auditor,
        "motivo_reprovado": r.motivo_reprovado,
        "comentario": r.comentario
    } for r in requests]

def serialize_alert_events_by_cpf(requests):
    return [{
        "alert_id": r.alert_id,
        "carteira": r.carteira,
        "status_meta": r.status_meta,
        "comment_meta": r.comment_meta,
        "name": r.name_author,
        "created_at": r.createdAt
    } for r in requests]

def serialize_solicitation_by_hashId(requests):
    return [{
       "alert_id": r.alert_id,
       "benef_cpf": r.benef_cpf,
       "benef_nome": r.benef_nome,
       "benef_rg": r.benef_rg,
       "benef_data_nasc": r.benef_data_nasc,
       "cid": r.cid,
       "fator_rh": r.fator_rh,
       "resp_nome": r.resp_nome,
       "resp_rg": r.resp_rg,
       "benef_telefone": r.benef_telefone,
       "resp_telefone": r.resp_telefone,
       "local_de_retirada": r.local_de_retirada,
       "naturalidade": r.naturalidade,
       "nome_da_mae": r.nome_da_mae,
       "nome_do_pai": r.nome_do_pai,
       "responsavel_legal_do_beneficiario_menor": r.responsavel_legal_do_beneficiario_menor,
       "cpf_responsavel": r.cpf_responsavel,
       "responsavel_legal_do_beneficiario": r.responsavel_legal_do_beneficiario,
       "cep_beneficiario": r.cep_beneficiario,
       "municipios_endereco_beneficiario": r.municipios_endereco_beneficiario,
       "bairro_beneficiario": r.bairro_beneficiario,
       "avenida_rua_beneficiario": r.avenida_rua_beneficiario,
       "numero_beneficiario": r.numero_beneficiario,
       "municipios_naturalidade": r.municipios_naturalidade_meta,
       "tipo_da_deficiencia": r.tipo_da_deficiencia_meta,
       "external_id": r.external_id,
       "created_at": r.created_at,
       "maioridade": r.maioridade,
       "tipo_carteira": r.tipo_carteira,
       "descricao_motivo_2via": r.descricao_motivo_2via,
       "statusId": r.statusId,
       "channelId": r.channelId,
       "cep_responsavel": r.cep_responsavel, 
       "bairro_responsavel": r.bairro_responsavel, 
       "numero_responsavel": r.numero_responsavel, 
       "municipio_responsavel": r.municipio_responsavel,
       "rua_avenida_responsavel": r.rua_avenida_responsavel,
       "endereco_do_responsavel": r.endereco_do_responsavel,
       "doc_cid_laudo": r.doc_cid_laudo,
       "anexo_comprovacao_2via": r.anexo_comprovacao_2via,
       "doc_cpf_do_beneficiario_anexo": r.doc_cpf_do_beneficiario_anexo,
       "doc_rg_beneficiario_verso_anexo": r.doc_rg_beneficiario_verso_anexo,
       "doc_comprovante_de_endereco_anexo": r.doc_comprovante_de_endereco_anexo,
       "doc_foto_3_x_4_beneficiario_anexo": r.doc_foto_3_x_4_beneficiario_anexo,
       "doc_rg_do_beneficiario_frente_anexo": r.doc_rg_do_beneficiario_frente_anexo,
       "doc_curatela_anexo": r.doc_curatela_anexo,
       "doc_cpf_responsavel_legal_anexo": r.doc_cpf_responsavel_legal_anexo, 
       "doc_rg_responsavel_legal_verso_anexo": r.doc_rg_responsavel_legal_verso_anexo, 
       "doc_rg_responsavel_legal_frente_anexo": r.doc_rg_responsavel_legal_frente_anexo, 
       "doc_comprovante_endereco_responsavel_legal_anexo": r.doc_comprovante_endereco_responsavel_legal_anexo,
       "biometria_do_beneficiario": r.biometria_do_beneficiario,
       "resp_email": r.resp_email,
       "sexo_beneficiario": r.sexo_beneficiario
    }for r in requests]

def serialize_history_by_alert_id(requests):
    return [{
    "alert_id": r.alert_id,
    "nome": r.nome,
    "cpf": r.cpf,
    "carteira": r.carteira,
    "maioridade": r.maioridade_meta,
    "nome_da_mae": r.nome_da_mae_meta,
    "nome_do_pai": r.nome_do_pai_meta,
    "bairro_beneficiario_meta": r.bairro_beneficiario_meta,
    "tipo_carteira": r.tipo_carteira_meta,
    "rg_responsavel": r.rg_responsavel_meta,
    "cep_responsavel": r.cep_responsavel_meta,
    "cpf_responsavel": r.cpf_responsavel_meta,
    "rg_beneficiario": r.rg_beneficiario_meta,
    "cep_beneficiario": r.cep_beneficiario_meta,
    "cid_beneficiario": r.cid_beneficiario_meta,
    "municipios_naturalidade": r.municipios_naturalidade_meta,
    "cid2_beneficiario": r.cid2_beneficiario_meta,
    "local_de_retirada": r.local_de_retirada_meta,
    "bairro_responsavel": r.bairro_responsavel_meta,
    "numero_responsavel": r.numero_responsavel_meta,
    "para_quem_cadastro": r.para_quem_cadastro_meta,
    "numero_beneficiario": r.numero_beneficiario_meta,
    "motivo_2_via": r.motivo_2_via_meta,
    "nome_do_beneficiario": r.nome_do_beneficiario_meta,
    "municipio_responsavel": r.municipio_responsavel_meta,
    "endereco_do_responsavel": r.endereco_do_responsavel_meta,
    "municipios_beneficiario": r.municipios_beneficiario_meta,
    "rua_avenida_responsavel": r.rua_avenida_responsavel_meta,
    "telefone_1_beneficiario": r.telefone_1_beneficiario_meta,
    "telefone_2_beneficiario": r.telefone_2_beneficiario_meta,
    "avenida_rua_beneficiario": r.avenida_rua_beneficiario_meta,
    "sexo_genero_beneficiario": r.sexo_genero_beneficiario_meta,
    "estado_civil_beneficiario": r.estado_civil_beneficiario_meta,
    "naturalidade_beneficiario": r.naturalidade_beneficiario_meta,
    "nacionalidade_beneficiario": r.nacionalidade_beneficiario_meta,
    "tipo_sanguineo_beneficiario": r.tipo_sanguineo_beneficiario_meta,
    "municipio_realizado_cadastro": r.municipio_realizado_cadastro_meta,
    "orgao_expedidor_beneficiario": r.orgao_expedidor_beneficiario_meta,
    "data_de_nascimento_beneficiario": r.data_de_nascimento_beneficiario_meta,
    "tipo_da_deficiencia_beneficiario": r.tipo_da_deficiencia_beneficiario_meta,
    "nome_responsavel_legal_do_beneficiario": r.nome_responsavel_legal_do_beneficiario_meta,
    "responsavel_legal_do_beneficiario": r.responsavel_legal_do_beneficiario_meta,
    "responsavel_legal_do_beneficiario_menor": r.responsavel_legal_do_beneficiario_menor_meta,
    "statusId": r.statusId,
    "created_at": r.created_at
    } for r in requests]

def serialize_history_modified_by_alert_id(requests):
    return [{
    "cid": r.cid_modified,
    "resp_rg": r.resp_rg_modified,
    "benef_rg": r.benef_rg_modified,
    "nome_mae": r.nome_mae_modified,
    "nome_pai": r.nome_pai_modified,
    "resp_cep": r.resp_cep_modified,
    "resp_cpf": r.resp_cpf_modified,
    "benef_cep": r.benef_cep_modified,
    "benef_cpf": r.benef_cpf_modified,
    "resp_nome": r.resp_nome_modified,
    "benef_nome": r.benef_nome_modified,
    "resp_bairro": r.resp_bairro_modified,
    "resp_numero": r.resp_numero_modified,
    "benef_bairro": r.benef_bairro_modified,
    "benef_numero": r.benef_numero_modified,
    "naturalidade": r.naturalidade_modified,
    "resp_municipio": r.resp_municipio_modified,
    "tipo_sanguineo": r.tipo_sanguineo_modified,
    "benef_municipio": r.benef_municipio_modified,
    "data_nascimento": r.data_nascimento_modified,
    "resp_logradouro": r.resp_logradouro_modified,
    "benef_logradouro": r.benef_logradouro_modified,
    "resp_endereco_completo": r.resp_endereco_completo_modified,
    "benef_endereco_completo": r.benef_endereco_completo_modified
    }for r in requests]

def serialize_aproved_ciptea(requests):
    return [{

    }for r in requests]

def serialize_solicitation_by_alert_id(requests):
    return [{
    "alert_id": r.alert_id,
    "benef_cpf": r.benef_cpf,
    "benef_nome": r.benef_nome,
    "attachments": r.attachments
    }for r in requests]

def serialize_aproved_ciptea(requests):
    return [{
        "numero_carteira": r.numero_carteira,
        "foto_3x4": r.foto_3x4,
        "nome": r.nome,
        "cpf": r.cpf,
        "rg_beneficiario_meta": r.rg_beneficiario_meta,
        "cid_beneficiario": r.cid_beneficiario,
        "data_de_nascimento": r.data_de_nascimento,
        "telefone_beneficiario_meta": r.telefone_beneficiario_meta,
        "tipo_sanguineo_beneficiario_meta": r.tipo_sanguineo_beneficiario_meta,
        "naturalidade_beneficiario": r.naturalidade_beneficiario,
        "expedicao": r.expedicao,
        "vencimento": r.vencimento,
        "endereco_beneficiario": r.endereco_beneficiario,
        "filiacao": r.filiacao,
        "nome_responsavel_legal_do_beneficiario_meta": r.nome_responsavel_legal_do_beneficiario_meta,
        "rg_responsavel_meta": r.rg_responsavel_meta,
        "email_meta": r.email_meta,
        "telefone_responsavel_meta": r.telefone_responsavel_meta,
        "endereco_responsavel": r.endereco_responsavel,
        "foto_digital": r.foto_digital,
        "url_qr_code": r.url_qr_code
    } for r in requests]

def serialize_solicitation_meta_alert_id(requests):
    return[{
        "meta": json.loads(r.meta)
    }for r in requests]

def serialize_solicitation_old_cpf(requests):
    return[{
    "alert_id": r.alert_id,
    "benef_cpf": r.benef_cpf, 
    "benef_nome": r.benef_nome, 
    "created_at": r.created_at, 
    "updated_at": r.updated_at,
    "status": r.status,
    "status_validacao": r.status_validacao,
    "estrutura": r.estrutura
    }for r in requests]

def serialize_recepcao(requests):
    return [{
    'cpf':r.benef_cpf,
    'hashId':r.hashId,
    'nome':r.nome,
    'alert_id': r.alert_id,
    'tipo_da_deficiencia_meta': r.tipo_da_deficiencia_meta,
    'local_de_retirada': r.local_de_retirada,
    'municipios_naturalidade_meta': r.municipios_naturalidade_meta,
    'cid': r.cid,
    'carteirinha': r.carteirinha,
    'status': r.status,
    'created_at': r.created_at
    }for r in requests]

def serialize_count_recepcao(requests):
    return [{
        'count': r.count
    }for r in requests]

def serialize_produtividade(requests):
    return [{
        'auditor': r.auditor,
        'quantidade': r.quantidade,
        'total': r.total
    }for r in requests]

def serialize_status_solicitacao(solicitacao):
    # Verifica se a solicitação existe
    if not solicitacao:
        return None
        
    # Retorna um único dicionário ao invés de uma lista
    return {
        'cpf': solicitacao.benef_cpf,
        'nome': solicitacao.benef_nome,
        'statusId': solicitacao.statusId,
        'alert_id': solicitacao.alert_id,
        'channelId': solicitacao.channelId,
        'motivo_reprovado': solicitacao.motivo_reprovado,
    }

@app.get("/requests")
async def requests(limit='100', offset='0', full='false'):
    requests = get_requests(int(limit), int(offset))
    serialize = serialize_full_requests if full == 'true' else serialize_requests

    return {
        "requests": serialize(requests)
    }


@app.get("/historico")
async def history(
        cpf: str,
        order: str,
        inicio: int,
        fim: int,
        alert_id: Optional[int] = Query(None, alias='alert_id'),
        statusId: Optional[int] = Query(None, alias='statusId'),
        nome: Optional[str] = Query(None, alias='nome'),
        start_date: Optional[str] = Query(None, alias='start_date'),
        end_date: Optional[str] = Query(None, alias='end_date')
):
    filter = {'alert_id': alert_id, 'statusId': statusId,'inicio': inicio, 'fim': fim,
              'cpf': cpf, 'order': order, 'nome': nome,
              'start_date': start_date, 'end_date': end_date}

    requests = get_historico(filter)


    return {
        "requests": serialize_history_requests(requests)
    }

@app.get("/cpf")
async def get_cpf(
        view: str,
        order: str,
        inicio: int,
        fim: int,
        cpf: Optional[str] = Query(None, alias='cpf'),
        nome: Optional[str] = Query(None, alias='nome'),
        nome_responsavel: Optional[str] = Query(None, alias='nome_responsavel'),
        cid: Optional[str] = Query(None, alias='cid'),
        alert_id: Optional[str] = Query(None, alias='alert_id'),
        projeto: Optional[str] = Query(None, alias='projeto'),
        via: Optional[str] = Query(None, alias='via'),
        municipio_realizado_cadastro: Optional[str] = Query(None, alias='municipio_realizado_cadastro'),
        local_de_retirada: Optional[str] = Query(None, alias = 'local_de_retirada'),
        deficiencia: Optional[str] = Query(None, alias= 'deficiencia'),
        start_date: Optional[str] = Query(None, alias='start_date'),
        end_date: Optional[str] = Query(None, alias='end_date'),
        especific_date: Optional[str] = Query(None, alias='especific_date')
):
    filters = {'view': view, 'order': order, 'inicio': inicio, 'fim': fim, 'cpf': cpf, 
    'nome': nome, 'nome_responsavel': nome_responsavel, 'cid': cid, 'alert_id': alert_id, 
    'projeto': projeto, 'via': via, 'municipio_realizado_cadastro': municipio_realizado_cadastro,
    'local_de_retirada': local_de_retirada, 'deficiencia': deficiencia, 
    'start_date': start_date, 'end_date': end_date, 'especific_date': especific_date}
    
    requests = get_hash(filters=filters)

    return {
        "requests": serialize_hash(requests)
    }

@app.get("/count_cpf")
async def get_count_cpf(
        view: str,
        cpf: Optional[str] = Query(None, alias='cpf'),
        nome: Optional[str] = Query(None, alias='nome'),
        nome_responsavel: Optional[str] = Query(None, alias='nome_responsavel'),
        cid: Optional[str] = Query(None, alias='cid'),
        alert_id: Optional[str] = Query(None, alias='alert_id'),
        projeto: Optional[str] = Query(None, alias='projeto'),
        via: Optional[str] = Query(None, alias='via'),
        municipio_realizado_cadastro: Optional[str] = Query(None, alias='municipio_realizado_cadastro'),
        local_de_retirada: Optional[str] = Query(None, alias = 'local_de_retirada'),
        deficiencia: Optional[str] = Query(None, alias= 'deficiencia'),
        start_date: Optional[str] = Query(None, alias='start_date'),
        end_date: Optional[str] = Query(None, alias='end_date'),
        especific_date: Optional[str] = Query(None, alias='especific_date')

):
    filters = {'view': view, 'cpf': cpf, 'nome': nome, 'nome_responsavel': nome_responsavel, 'cid': cid, 
    'alert_id': alert_id, 'projeto': projeto, 'via': via, 'municipio_realizado_cadastro': municipio_realizado_cadastro,
    'local_de_retirada': local_de_retirada, 'deficiencia': deficiencia,
    'start_date': start_date, 'end_date': end_date, 'especific_date': especific_date}

    requests = get_count_cpf_hash(filters=filters)

    return {
        "requests": serialize_count_hash(requests)
    }

@app.get("/arquivados")
async def get_cpf(
        order: str,
        inicio: int,
        fim: int,
        status: List[int] = Query(...),
        cpf: Optional[str] = Query(None, alias='cpf'),
        nome: Optional[str] = Query(None, alias='nome'),
        nome_responsavel: Optional[str] = Query(None, alias='nome_responsavel'),
        cid: Optional[str] = Query(None, alias='cid'),
        alert_id: Optional[str] = Query(None, alias='alert_id'),
        projeto: Optional[str] = Query(None, alias='projeto'),
        via: Optional[str] = Query(None, alias='via'),
        municipio_realizado_cadastro: Optional[str] = Query(None, alias='municipio_realizado_cadastro'),
        local_de_retirada: Optional[str] = Query(None, alias = 'local_de_retirada'),
        deficiencia: Optional[str] = Query(None, alias= 'deficiencia'),
        start_date: Optional[str] = Query(None, alias='start_date'),
        end_date: Optional[str] = Query(None, alias='end_date'),
        especific_date: Optional[str] = Query(None, alias='especific_date')
):
    filters = {'order': order, 'inicio': inicio, 'fim': fim, 'status': status, 'cpf': cpf, 
    'nome': nome, 'nome_responsavel': nome_responsavel, 'cid': cid, 'alert_id': alert_id, 
    'projeto': projeto, 'via': via, 'municipio_realizado_cadastro': municipio_realizado_cadastro,
    'local_de_retirada': local_de_retirada, 'deficiencia': deficiencia, 
    'start_date': start_date, 'end_date': end_date, 'especific_date': especific_date}
    
    requests = get_arquivados(filters=filters)

    return {
        "requests": serialize_hash_arquivados(requests)
    }

@app.get("/count_arquivados")
async def get_count_cpf(
        status: List[int] = Query(...),
        cpf: Optional[str] = Query(None, alias='cpf'),
        nome: Optional[str] = Query(None, alias='nome'),
        nome_responsavel: Optional[str] = Query(None, alias='nome_responsavel'),
        cid: Optional[str] = Query(None, alias='cid'),
        alert_id: Optional[str] = Query(None, alias='alert_id'),
        projeto: Optional[str] = Query(None, alias='projeto'),
        via: Optional[str] = Query(None, alias='via'),
        municipio_realizado_cadastro: Optional[str] = Query(None, alias='municipio_realizado_cadastro'),
        local_de_retirada: Optional[str] = Query(None, alias = 'local_de_retirada'),
        deficiencia: Optional[str] = Query(None, alias= 'deficiencia'),
        start_date: Optional[str] = Query(None, alias='start_date'),
        end_date: Optional[str] = Query(None, alias='end_date'),
        especific_date: Optional[str] = Query(None, alias='especific_date')

):
    filters = {'status': status, 'cpf': cpf, 'nome': nome, 'nome_responsavel': nome_responsavel, 'cid': cid, 
    'alert_id': alert_id, 'projeto': projeto, 'via': via, 'municipio_realizado_cadastro': municipio_realizado_cadastro,
    'local_de_retirada': local_de_retirada, 'deficiencia': deficiencia,
    'start_date': start_date, 'end_date': end_date, 'especific_date': especific_date}

    requests = get_count_arquivados(filters=filters)

    return {
        "requests": serialize_count_hash(requests)
    }

@app.get("/consulta_geral")
async def get_consultas_gerais(
        filtro: str,
        order: str,
        inicio: int,
        fim: int,
        alert_id: Optional[int] = Query(None, alias='alert_id'),
        benef_cpf: Optional[str] = Query(None, alias='benef_cpf'),
        benef_nome: Optional[str] = Query(None, alias='benef_nome'),
        cid: Optional[str] = Query(None, alias='cid'),
):
    filters = {'filtro': filtro, 'order': order, 'inicio': inicio, 'fim': fim, 'alert_id': alert_id,
               'benef_cpf': benef_cpf, 'benef_nome': benef_nome, 'cid': cid}
    requests = get_consulta_geral(filters=filters)

    return {
        "requests": serialize_consulta_geral(requests)
    }

@app.get("/count_consulta_geral")
async def get_count_consultas_gerais(
        filtro: str,
        alert_id: Optional[int] = Query(None, alias='alert_id'),
        benef_cpf: Optional[str] = Query(None, alias='benef_cpf'),
        benef_nome: Optional[str] = Query(None, alias='benef_nome'),
        cid: Optional[str] = Query(None, alias='cid')
):
    filters = {'filtro': filtro, 'alert_id': alert_id, 'benef_cpf': benef_cpf, 'benef_nome': benef_nome, 
               'cid': cid}
    requests = get_count_consulta_geral(filters=filters)

    return {
        "requests": serialize_count_consulta_geral(requests)
    }

@app.get("/solicitacoes")
async def solicitacoes(
        status: List[int] = Query(None, alias='status'),
        inicio: int = Query(...),
        fim: int = Query(...),
        order: str = Query(...),
        alert_id: Optional[int] = Query(None, alias='alert_id'),
        cpf: Optional[str] = Query(None, alias='cpf'),
        hashId: Optional[str] = Query(None, alias='hashId'),
        nome: Optional[str] = Query(None, alias='nome'),
        nome_responsavel: Optional[str] = Query(None, alias='nome_responsavel'),
        cid: Optional[str] = Query(None, alias='cid'),
        deficiencia: Optional[str] = Query(None, alias='deficiencia'),
        local_retirada: Optional[str] = Query(None, alias='local_retirada'),
        municipio: Optional[str] = Query(None, alias='municipio'),
        projeto: Optional[str] = Query(None, alias='projeto'),
        start_date: Optional[str] = Query(None, alias='start_date'),
        end_date: Optional[str] = Query(None, alias='end_date'),
        orientation_date: Optional[str] = Query(None, alias='orientation_date')
):
    filters = {'alert_id': alert_id, 'cpf': cpf, 'hashId': hashId, 'inicio': inicio, 'fim': fim, 'order':order,
               'nome': nome, 'nome_responsavel': nome_responsavel, 'cid': cid, 'deficiencia': deficiencia,
               'local_retirada': local_retirada, 'municipio': municipio,
               'status': status, 'projeto': projeto, 
               'start_date': start_date, 'end_date': end_date, 'orientation_date': orientation_date}

    requests = get_solicitacoes(filters=filters)

    return {
        "requests": serialize_solicitation_requests(requests)
    }

@app.get("/solicitacao_hashid")
async def solicitacao_hashId(
        benef_cpf: str
):
    requests = get_solicitation_hashid(benef_cpf=benef_cpf)

    return {
        "requests": serialize_solicitation_hashid(requests)
    }

@app.get("/aprovados_alert_id")
async def aprovados_alert_id(
    hash_id: str
):
    requests = get_aprovados_alert_id(hash_id=hash_id)
    return{
        "requests": serialize_aprovados_alert_id(requests)
    }

@app.get("/solicitacao_alert")
async def solicitacao_alert(
        hashId: str,
        alert_id: Optional[int] = Query(None, alias='alert_id')
):

    filters = {'hashId': hashId, 'alert_id': alert_id}

    requests = get_solicitacao_alert(filters=filters)

    return {
        "requests": serialize_solicitation_alert_requests(requests)
    }

@app.get("/count_solicitacoes")
async def count_solicitacoes(
        status: List[int] = Query(None, alias='status'),
        inicio: int = Query(...),
        fim: int = Query(...),
        alert_id: Optional[int] = Query(None, alias='alert_id'),
        cpf: Optional[str] = Query(None, alias='cpf'),
        hashId: Optional[str] = Query(None, alias='hashId'),
        nome: Optional[str] = Query(None, alias='nome'),
        cid: Optional[str] = Query(None, alias='cid'),
        deficiencia: Optional[str] = Query(None, alias='deficiencia'),
        local_retirada: Optional[str] = Query(None, alias='local_retirada'),
        municipio: Optional[str] = Query(None, alias='municipio'),
        projeto: Optional[str] = Query(None, alias='projeto'),
        start_date: Optional[str] = Query(None, alias='start_date'),
        end_date: Optional[str] = Query(None, alias='end_date'),
        orientation_date: Optional[str] = Query(None, alias='orientation_date')
):
    filters = {'alert_id': alert_id, 'cpf': cpf, 'hashId': hashId, 'inicio': inicio, 'fim': fim,
               'nome': nome, 'cid': cid, 'deficiencia': deficiencia, 'local_retirada': local_retirada,
               'municipio': municipio, 'status': status, 'projeto': projeto, 
               'start_date': start_date, 'end_date': end_date, 'orientation_date': orientation_date}

    requests = get_count_solicitacoes(filters=filters)

    return {
        "requests": serialize_count_solicitation_requests(requests)
    }

@app.get("/aprovados")
async def pcd(
        projeto: str = Query(...),
        status: List[int] = Query(...),
        order: str = Query(...),
        inicio: int = Query(...),
        fim: int = Query(...),
        alert_id: Optional[int] = Query(None, alias='alert_id'),
        carteira: Optional[int] = Query(None, alias='carteira'),
        cpf: Optional[str] = Query(None, alias='cpf'),
        nome: Optional[str] = Query(None, alias='nome'),
        municipio: Optional[str] = Query(None, alias='municipio'),
        local_de_retirada: Optional[str] = Query(None, alias='local_de_retirada'),
        start_date: Optional[str] = Query(None, alias='start_date'),
        end_date: Optional[str] = Query(None, alias='end_date'),
        orientation_date: Optional[str] = Query(None, alias='orientation_date')
):
    filters = {'status': status, 'order': order, 'inicio': inicio, 'fim': fim, 'alert_id': alert_id, 'id': id,
               'carteira': carteira, 'cpf': cpf, 'nome': nome, 'municipio': municipio, "local_de_retirada": local_de_retirada,
               'start_date': start_date, 'end_date': end_date, 'orientation_date': orientation_date}
    
    if (start_date or end_date) and not orientation_date:
        raise HTTPException(status_code=400, detail="orientation_date is required when start_date or end_date are provided")
    
    if projeto == 'PCD':
        requests = get_aprovados_pcd(filters=filters)
    elif projeto == 'CIPTEA':
        requests = get_aprovados_ciptea(filters=filters)
    else:
        raise HTTPException(status_code=404, detail="project not found")

    return {
        "requests": serialize_approved_requests(requests)
    }


@app.get("/count_aprovados")
async def count_pcd(
        projeto: str = Query(...),
        status: List[int] = Query(...),
        alert_id: Optional[int] = Query(None, alias='alert_id'),
        id: Optional[int] = Query(None, alias='id'),
        carteira: Optional[int] = Query(None, alias='carteira'),
        cpf: Optional[str] = Query(None, alias='cpf'),
        nome: Optional[str] = Query(None, alias='nome'),
        municipio: Optional[str] = Query(None, alias='municipio'),
        local_de_retirada: Optional[str] = Query(None, alias='local_de_retirada'),
        start_date: Optional[str] = Query(None, alias='start_date'),
        end_date: Optional[str] = Query(None, alias='end_date'),
        orientation_date: Optional[str] = Query(None, alias='orientation_date')
):
    filters = {'status': status, 'alert_id': alert_id, 'id': id,
               'carteira': carteira, 'cpf': cpf, 'nome': nome, 'municipio': municipio, "local_de_retirada": local_de_retirada,
               'start_date': start_date, 'end_date': end_date, 'orientation_date': orientation_date}
   
    if (start_date or end_date) and not orientation_date:
        raise HTTPException(status_code=400, detail="orientation_date is required when start_date or end_date are provided")
    

    if projeto == 'PCD':
        requests = get_count_aprovados_pcd(filters=filters)
    elif projeto == 'CIPTEA':
        requests = get_count_aprovados_ciptea(filters=filters)
    else:
        raise HTTPException(status_code=404, detail="project not found")

    return {
        "requests": serialize_count_approved_requests(requests)
    }

@app.get("/lotes")
async def lote(
        projeto: str,
        order: str,
        inicio: int,
        fim: int,
        statusId: Optional[int] = Query(None, alias='statusId'),
        cpf: Optional[str] = Query(None, alias='cpf'),
        nome: Optional[str] = Query(None, alias='nome'),
        alert_id: Optional[int] = Query(None, alias='alert_id'),
        lote: Optional[int] = Query(None, alias='lote')
):
    filters = {'projeto': projeto, 'order': order, 'inicio': inicio, 'fim': fim, 'statusId': statusId, 'cpf': cpf,
               'nome': nome, 'alert_id': alert_id, 'lote': lote}
    requests = get_lote(filters=filters)

    return {
        "requests": serialize_lote(requests)
    }

@app.get("/count_lotes")
async def count_lote(
        projeto: str,
        statusId: Optional[int] = Query(None, alias='statusId'),
        cpf: Optional[str] = Query(None, alias='cpf'),
        nome: Optional[str] = Query(None, alias='nome'),
        alert_id: Optional[int] = Query(None, alias='alert_id'),
        lote: Optional[int] = Query(None, alias='lote')
):
    filters = {'projeto': projeto, 'statusId': statusId, 'cpf': cpf, 'nome': nome, 'alert_id': alert_id, 'lote': lote}
    requests = get_count_lote(filters=filters)

    return {
        "requests": serialize_count_lote(requests)
    }

@app.get("/export_lote")
async def lote_export(lote:int):
    try:
        filename = f"lote_{lote}.xlsx"
        buffer = get_lote_xlsx(lote)

        if buffer.getbuffer().nbytes == 0:
            raise HTTPException(status_code=400, detail="Lote não encontrado")

        return StreamingResponse(
            buffer,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export_solicitacoes")
async def solicitations_export(
    status: List[int] = Query(None, alias='status'),
    naturalidade: Optional[str] = Query(None, alias='naturalidade'),
    municipio: Optional[str] = Query(None, alias='municipio'),
    cid: Optional[str] = Query(None, alias='cid'),
    carteira: Optional[str] = Query(None, alias='carteira'),
    deficiencia: Optional[str] = Query(None, alias='deficiencia'),
    start_date: Optional[str] = Query(None, alias='start_date'),
    end_date: Optional[str] = Query(None, alias='end_date')
):
    filters = {'status': status, 'naturalidade': naturalidade, 
               'municipio': municipio, 'start_date': start_date, 'end_date': end_date, 'cid':cid, 'carteira':carteira, 'deficiencia':deficiencia}
    try:
        filename = 'solicitacoes.xlsx'
        buffer = solicitacoes_xlsx(filters)

        if buffer.getbuffer().nbytes == 0:
            raise HTTPException(status_code=400, detail="Lote não encontrado")
        return StreamingResponse(
            buffer,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/visual_export")
async def visual_export_route(
    status: List[int] = Query(None, alias='status'),
    naturalidade: Optional[str] = Query(None, alias='naturalidade'),
    municipio: Optional[str] = Query(None, alias='municipio'),
    cid: Optional[str] = Query(None, alias='cid'),
    deficiencia: Optional[str] = Query(None, alias='deficiencia'),
    carteira: Optional[str] = Query(None, alias='carteira'),
    start_date: Optional[str] = Query(None, alias='start_date'),
    end_date: Optional[str] = Query(None, alias='end_date'),
    inicio: int = Query(...),
    fim: int = Query(...)
):
    filters = {'status': status, 'naturalidade': naturalidade, 
               'municipio': municipio, 'start_date': start_date, 'end_date': end_date, 'cid':cid, 'carteira':carteira,'fim':fim, 'inicio':inicio, 'deficiencia':deficiencia}
    result = visual_export(filters)
    return {"response": serialize_visual_export(result)}

@app.get("/count_visual_export")
async def count_visual_export_route(
    status: List[int] = Query(None, alias='status'),
    naturalidade: Optional[str] = Query(None, alias='naturalidade'),
    cid: Optional[str] = Query(None, alias='cid'),
    municipio: Optional[str] = Query(None, alias='municipio'),
    carteira: Optional[str] = Query(None, alias='carteira'),
    deficiencia: Optional[str] = Query(None, alias='deficiencia'),
    start_date: Optional[str] = Query(None, alias='start_date'),
    end_date: Optional[str] = Query(None, alias='end_date')
):
    filters = {'status': status, 'naturalidade': naturalidade, 
               'municipio': municipio, 'start_date': start_date, 'end_date': end_date, 'cid':cid, 'carteira':carteira, 'deficiencia':deficiencia}
    count = count_visual_export(filters)
    return {"response":serialize_count_visual_export(count)}

# comentario
@app.get("/valida_carteirinha_hashId")
async def validar_carteira(hashId: str):
    try:
        requests = validar_campos_carteira(hashId)
        return{
            'response': serialize_validar_carteira(requests)
        }        
    except Exception as e:
        raise HTTPException(status_code=404, detail="hashId not found")


@app.get("/dashboard/projeto")
async def count_project():
    requests = get_total_by_project()

    return {"requests": serialize_count_project(requests)}


@app.get("/dashboard/municipio")
async def count_municipio():
    requests = get_total_by_municipio()

    return {"requests": serialize_count_municipio(requests)}

@app.get("/dashboard/solicitacoes")
async def table_solicitations(
        limit: int
):
    requests = get_last_solicitations(limit)

    return {"requests": serialize_last_solicitations(requests)}

@app.get("/lote_alerts")
async def lote_alert(
        projeto: str,
        lote: int,
        inicio: int,
        fim: int,
        cpf: Optional[str] = Query(None, alias='cpf'),
        nome: Optional[str] = Query(None, alias='nome'),
        alert_id: Optional[int] = Query(None, alias='alert_id')
):
    filters = {'projeto': projeto, 'lote': lote, 'inicio': inicio, 'fim': fim, 'cpf': cpf, 'nome': nome, 'alert_id': alert_id}
    requests = get_lote_alert(filters=filters)

    return {
        "requests": serialize_lote_alerts(requests)
    }


@app.get("/last_lote_number")
async def last_lote_number(
        projeto: str
):
    requests = get_last_lote(projeto=projeto)
    return {
        "requests": serialize_last_number_lote(requests)
    }

@app.get("/last_number")
async def last_number(
        projeto: str
):

    if projeto == 'PCD':
        requests = get_last_number_pcd()
    elif projeto == 'CIPTEA':
        requests = get_last_number_ciptea()
    else:
        raise HTTPException(status_code=404, detail="project not found")

    return {
        "requests": serialize_last_number_approved(requests)
    }

@app.get("/carteira_virtual")
async def carteira_virtual(
        projeto: str,
        hashId: str
):

    filters = {'projeto': projeto, 'hashId': hashId}
    requests = get_carteira_virtual(filters=filters)
    return {
        "requests": serialize_carteira(requests)
    }

@app.get("/informations_carteirinha")
async def informations_carteirinha(
    alert_id: int,
    tipo_carteirinha: str
):
    try:
        requests = get_informations_carteirinha(alert_id, tipo_carteirinha)

        return {
                'response': requests
            }
    except:
        raise HTTPException(status_code=404, detail="alert_id not found")

@app.get("/informations_ciptea")
async def informations_ciptea(
    alert_id: int
):
    try:
        requests = get_aproved_ciptea(alert_id)
        return {
            'response': serialize_aproved_ciptea(requests)
        }
    except:
        raise HTTPException(status_code=404, detail='alert_id not found')

@app.get("/attachments_edicao")
async def attachments_get(alert_id: int):
    try:
        response = get_attachments_alert_id(alert_id)
        return {
                'response': response
            }
    except Exception as e:
        raise e


@app.post("/insert/historico")
async def insert_historico(
        alert_id: int,
        nome: str,
        cpf: str,
        carteira: str,
        meta: dict,
        modified: dict,
        auditor: str,
        statusId: int,
        comentario: Optional[str] = None):
    try:
        insert_historicos(alert_id, nome, cpf, carteira, meta, modified, auditor, statusId, comentario)
    except Exception as e:
        raise e

    return {"success": True}


@app.post("/insert/aprovados")
async def insert_aprovado(
        projeto: str,
        alert_id: int,
        numero_carteira: int,
        nome: str,
        cpf: str,
        hashId: str,
        meta: dict,
        auditor: str,
        statusId: int):
    try:
        insert_aprovados(projeto, alert_id, numero_carteira, nome, cpf, hashId, auditor, statusId, meta)
    except Exception as e:
        raise e

    return {"success": True}

@app.post('/insert_num_carteira')
async def insert_num_carteira(
    projeto: str = Query(...),
    cpf: str = Query(...),
    alert_id: int = Query(...),
    via: int = Query(...)
):
    try:
        insert_num_carteiras(projeto, cpf, alert_id, via)
        return {"sucess": True}
    except Exception as e:
        raise e
    

@app.patch("/update/aprovados")
async def patch_aprovados(
        projeto: str,
        alert_ids: int,
        statusId: int,
        foto_3x4: Optional[str] = Body(None, alias='foto_3x4'),
        nome: Optional[str] = Body(None, alias='nome'),
        foto_digital: Optional[str] = Body(None, alias='foto_digital'),
        vencimento: Optional[str] = Body(None, alias='vencimento'),
        expedicao: Optional[str] = Body(None, alias='expedicao'),
        lote: Optional[str] = Body(None, alias='lote')
):
    parameters = {'foto_3x4': foto_3x4, 'foto_digital': foto_digital, 'vencimento': vencimento, 'expedicao': expedicao, 'lote': lote, 'statusId': statusId, 'nome': nome}

    try:
        update_aprovados(projeto, parameters, alert_ids)
        return {"success": True}
    except Exception as e:
        raise e
    

@app.patch("/update/solicitacoes")
async def patch_solicitacoes(
        alert_id: int,
        statusId: int,
        meta: Optional[dict] = Body(None, alias='meta'),
        benef_rg: Optional[str] = Body(None, alias='benef_rg'),
        benef_nascimento: Optional[str] = Body(None, alias='benef_nascimento'),
        benef_nome: Optional[str] = Body(None, alias='benef_nome'),
        cid: Optional[str] = Body(None, alias='cid'),
        fator_rh: Optional[str] = Body(None, alias='fator_rh'),
        resp_nome: Optional[str] = Body(None, alias='resp_nome'),
        resp_rg: Optional[str] = Body(None, alias='resp_rg')
):
    parameters = {"meta": meta, "benef_rg": benef_rg,
                  "benef_data_nasc": benef_nascimento,
                  "benef_nome": benef_nome, "cid": cid,
                  "fator_rh": fator_rh, "resp_nome": resp_nome,
                  "resp_rg": resp_rg}

    try:
        update_solicitacoes(alert_id, statusId, parameters)
    except Exception as e:
        raise e
    
@app.patch("/update/solicitacoes_teste")
async def patch_solicitacoes_teste(
        alert_id: int, 
        statusId: int,
        auditor: str,
        motivo_reprovado: Optional[str] = Query(None, alias='motivo_reprovado'),
        comentario_beneficiario: Optional[str] = Query(None, alias='comentario_beneficiario'),
        meta: Optional[dict] = Body(None, alias='meta'),
        keys: Optional[List[str]] = Query(None, alias='keys'),
        values: Optional[List[str]] = Query(None, alias='values'),                           
):
    if keys and values and len(keys) != len(values):
        return {"error": "The number of keys must match the number of values."}

    try:
        update_solicitacoes_teste(
            alert_id, statusId, auditor, motivo_reprovado, 
            comentario_beneficiario, meta, keys, values
        )
        return {"success": True}
    except Exception as e:
        raise e


@app.patch("/requests/{alert_id}")
async def patch_request(alert_id: int, item: dict):
    request = get_request(alert_id)

    if request is None:
        raise HTTPException(status_code=404, detail="request not found")

    request.update(status=item.get("status"), data=item.get("data"))
    update_request(request)

    return {"success": True}


@app.post("/upload/image")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        img_name = upload_image(contents)
        return {"uuid": img_name}
    except Exception as e:
        raise e
    
@app.get("/historico_cpf")
async def historicoByCPF(cpf: str):
    try:
        requests = get_historico_by_cpf(cpf=cpf)
        requests_1 = get_alert_events_by_cpf(cpf=cpf)

        return {
            'response': serialize_history_by_cpf(requests) + serialize_alert_events_by_cpf(requests_1)
        }
    except (json.JSONDecodeError, AttributeError):
        return {
            'response': 'CPF não encontrado'
        }


@app.get("/solicitation_hashId")
async def solicitationByCPF(hashId:str):
    try:
        requests = get_solicitacao_by_hashId(hashId=hashId)
        return {
            'response': serialize_solicitation_by_hashId(requests)
        }
    except (json.JSONDecodeError, AttributeError):
        return {
            'response': 'HashId não encontrado'
        }
    
@app.get("/historico_alert_id")
async def historicoByAlertId(alert_id:int):
    try:
        requests = get_historic_by_alertd_id(alert_id=alert_id)
        return {
            'response': serialize_history_by_alert_id(requests)
        }
    except (json.JSONDecodeError, AttributeError):
        return {
            'response': 'alert_id não encontrado'
        }
    
@app.get("/historico_modified_alert_id")
async def HistoricoModifiedByAlertId(alert_id:int):
    try:
        requests = get_historico_modified_by_alert_id(alert_id=alert_id)
        return{
            'response': serialize_history_modified_by_alert_id(requests)
        }
    
    except (json.JSONDecodeError, AttributeError):
        return {
            'response': 'alert_id não encontrado'
        }
    
@app.get("/solicitation_alert_id")
async def SolicitationByAlertId(alert_id:int):
    try:
        requests = get_solicitation_by_alert_id(alert_id=alert_id)
        return{
            'response': serialize_solicitation_by_alert_id(requests)
        }
    
    except (json.JSONDecodeError, AttributeError):
        return {
            'response': 'alert_id não encontrado'
        }
    
@app.get("/solicitation_meta_alert_id")
async def SolicitationMetaByAlertId(alert_id:int):
    try:
        requests = get_solicitation_meta_by_alert_id(alert_id)
        return {
            'response': serialize_solicitation_meta_alert_id(requests)
        }
    except (json.JSONDecodeError, AttributeError):
        return {
            'response': 'alert_id não encontrado'
        }

@app.get("/solicitation_old_cpf")
async def SolicitationOldByCPF(cpf:str):
    try:
        requests = get_solicitation_old_by_cpf(cpf)
        return{
            'response': serialize_solicitation_old_cpf(requests)
        }
    except (json.JSONDecodeError, AttributeError):
        return {
            'response': 'cpf não encontrado'
        }

@app.get("/recepcao")
async def solicitacaoRecepcao(order: str = Query(...), 
                              inicio: int = Query(...), 
                              fim: int = Query(...),
                              cpf: Optional[str] = Query(None, alias='cpf'), 
                              alert_id: Optional[int] = Query(None, alias='alert_id'), 
                              nome: Optional[str] = Query(None, alias='nome')
                              ):
    
    parameters = {'cpf': cpf, 'alert_id': alert_id, 'nome': nome, 'order': order, 'inicio':inicio, 'fim':fim}
    try:
        requests = get_recepcao(parameters)
        return{
            'response': serialize_recepcao(requests)
        }
    except (json.JSONDecodeError, AttributeError):
        return {
            'response': 'nenhum dado foi encontrado'
        }

@app.get("/count_recepcao")
async def countRecepcao(cpf: Optional[str] = Query(None, alias='cpf'), 
                        alert_id: Optional[int] = Query(None, alias='alert_id'), 
                        nome: Optional[str] = Query(None, alias='nome')
                              ):
    
    parameters = {'cpf': cpf, 'alert_id': alert_id, 'nome': nome}
    try:
        requests = get_count_recepcao(parameters)
        return{
            'response': serialize_count_recepcao(requests)
        }
    except (json.JSONDecodeError, AttributeError):
        return {
            'response': 'nenhum dado foi encontrado'
        }
    

@app.get("/produtividade")
async def getProdutividade(
    request: Request,  # Adiciona o request
    auditor: Optional[str] = Query(None, alias='auditor'),
    range_date: Optional[str] = Query(None, alias='range_date'),
    especific_date: Optional[str] = Query(None, alias='especific_date')
    ):
    
    # Verifica se o request veio do ambiente de desenvolvimento
    is_dev = "dev" in request.url.hostname

    parameters = {
        'auditor': auditor, 
        'range_date': range_date, 
        'especific_date': especific_date,
        'is_dev': is_dev  # Agora passamos se é dev ou não
    }

    try:
        requests = get_produtividade(parameters)
        return {
            'response': serialize_produtividade(requests)
        }
    except (json.JSONDecodeError, AttributeError):
        return {
            'response': 'nenhum dado foi encontrado'
        }
    
@app.get("/get_status_solicitacao")
async def get_status_solicitacao(
    cpf: str = Query(None, alias='cpf'),
    data_nascimento: str = Query(None, alias='data_nascimento'),
    projeto: str = Query(None, alias='projeto')
):
    try:
        # Chama a função que valida a carteira
        solicitacao = getStatus_solicitacao(cpf, data_nascimento, projeto)
        
        if not solicitacao:
            raise HTTPException(status_code=404, detail="Carteira não encontrada")

        # Serializa um único objeto ao invés de uma lista
        resultado = serialize_status_solicitacao(solicitacao)
        if not resultado:
            raise HTTPException(status_code=404, detail="Carteira não encontrada")

        return {"response": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/testilson")
async def testando():
    return {
        'response': 'funcionou'
    }

