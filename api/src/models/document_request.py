from enum import Enum
from functools import reduce
import json
from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional
import requests

documentRequestStatus = ["registered", "pending", "analysis", "approved", "rejected"]

def count_attachments(acc, atts):
  return acc + len(atts[1])

# teste
def extract_attachments_images(lista_attachments: list):
    lista_imagens = []
    extensions_images = ['jpg', 'png', 'jpeg']
    url_base = 'https://sa-east-1-uploads.s3.amazonaws.com/100760000427/attachments/image/{uuid}.{extension}'  
    for flat in lista_attachments:
        for extension in extensions_images:
            url = url_base.format(uuid=flat, extension=extension)
            r = requests.head(url)
            if r.status_code == 200:
              lista_imagens.append(url)
              break
    return lista_imagens


class Projetos:
  def __init__(self, projeto, total):
    self.projeto = projeto
    self.total = total

class Municipios:
  def __init__(self, cad_municipio, total):
    self.cad_municipio = cad_municipio
    self.total = total

class LastSolicitations:
  def __init__(self, alert_id, benef_nome, cid, fator_rh, channelId, created_at):
    self.alert_id = alert_id
    self.benef_nome = benef_nome
    self.cid = cid
    self.fator_rh = fator_rh
    self.channelId = 'CIPTEA' if channelId in (12837, 6744, 6790) else 'PCD'
    self.created_at = created_at

class HashRequest:
  def __init__(self, benef_cpf, hashId, benef_nome, resp_nome, municipio, cid, tipo_da_deficiencia_meta, tag_recurso,
                naturalidade, idade, benef_telefone, local_de_retirada, channelId, alert_id, last_created, last_updated, total):
    self.benef_cpf = benef_cpf
    self.hashId = hashId
    self.benef_nome = benef_nome
    self.resp_nome = resp_nome
    self.municipio = municipio
    self.cid = cid
    self.tipo_da_deficiencia_meta = tipo_da_deficiencia_meta
    self.tag_recurso = tag_recurso
    self.naturalidade = naturalidade
    self.idade = idade
    self.benef_telefone = benef_telefone
    self.local_de_retirada = local_de_retirada
    self.channelId = channelId
    self.alert_id = alert_id
    self.last_created = last_created
    self.last_updated = last_updated
    self.total = total
    self.curatela_tutela = 'Curatela' if idade >= 18 else 'Tutela'

class HashRequestArquivados:
  def __init__(self, benef_cpf, hashId, benef_nome, resp_nome, auditor_arquivado, municipio, cid, tipo_da_deficiencia_meta, naturalidade, idade, benef_telefone, local_de_retirada, channelId, alert_id, last_created, last_updated, total):
    self.benef_cpf = benef_cpf
    self.hashId = hashId
    self.benef_nome = benef_nome
    self.resp_nome = resp_nome
    self.auditor_arquivado = auditor_arquivado
    self.cid = cid
    self.tipo_da_deficiencia_meta = tipo_da_deficiencia_meta
    self.municipio = municipio
    self.naturalidade = naturalidade
    self.idade = idade
    self.benef_telefone = benef_telefone
    self.local_de_retirada = local_de_retirada
    self.channelId = channelId
    self.alert_id = alert_id
    self.last_created = last_created
    self.last_updated = last_updated
    self.total = total
    self.curatela_tutela = 'Curatela' if idade >= 18 else 'Tutela'

class CountHashRequest:
  def __init__(self, count):
    self.count = count

class ConsultaGeralRequest:
  def __init__(self, benef_cpf, hashId, benef_nome, alert_id, deficiencia, telefone, local_de_retirada, municipio,
                cid, channelIds, last_created, last_updated, total):
    self.benef_cpf = benef_cpf
    self.hashId = hashId
    self.benef_nome = benef_nome
    self.alert_id = alert_id
    self.deficiencia = deficiencia
    self.telefone = telefone
    self.local_de_retirada = local_de_retirada
    self.municipio = municipio
    self.cid = cid
    self.channelIds = channelIds
    self.last_created = last_created
    self.last_updated = last_updated
    self.total = total

class CountConsultaGeralRequest:
  def __init__(self, count):
    self.count = count

class ApprovedRequest:
  def __init__(self, id, alert_id, numero_carteira, nome, municipio_beneficiario, cpf, cid, status, deficiencia, municipio, local_de_retirada,
               foto_3x4, foto_digital, hashId, vencimento, expedicao, lote, auditor, statusId, meta, via, created_at, updated_at):
    self.id = id
    self.alert_id = alert_id
    self.numero_carteira = numero_carteira
    self.nome = nome
    self.municipio_beneficiario = municipio_beneficiario
    self.cpf = cpf
    self.cid = cid
    self.status = status
    self.deficiencia = deficiencia
    self.municipio = municipio
    self.local_de_retirada = local_de_retirada
    self.foto_3x4 = foto_3x4
    self.foto_digital = foto_digital
    self.hashId = hashId
    self.vencimento = vencimento
    self.expedicao = expedicao
    self.lote = lote
    self.auditor = auditor
    self.statusId = statusId
    self.meta = json.loads(meta)
    self.via = via
    self.created_at = created_at
    self.updated_at = updated_at

class CountApprovedRequest:
  def __init__(self, count):
    self.count = count

class LoteRequest:
  def __init__(self, lote, total, updated_at, statusId, alert_id, numero_carteira):
    self.lote = lote
    self.total = total
    self.updated_at = updated_at
    self.statusId = statusId
    self.alert_id = alert_id
    self.numero_carteira = numero_carteira

class CountLote:
  def __init__(self, count):
    self.count = count

class ValidarCarteiraHashId:
    def __init__(self, numero_carteira: str, nome: str, cpf: str, rg_beneficiario_meta: str, cid_beneficiario_meta: str,
                 data_de_nascimento: str, telefone_beneficiario_meta: str, tipo_sanguineo_beneficiario_meta: str,
                 naturalidade_beneficiario_meta: str, expedicao: date, vencimento: date, endereco_beneficiario: str,
                 nome_da_mae_meta: str, nome_do_pai_meta: str, nome_responsavel_legal_do_beneficiario_meta: str,
                 rg_responsavel_meta: str, telefone_responsavel_meta: str, endereco_responsavel: str, foto_3x4: str,
                 foto_digital: str, url_qr_code: str, via_meta: str, email_meta: str):
        self.numero_carteira = numero_carteira
        self.nome = nome
        self.cpf = cpf
        self.rg_beneficiario_meta = rg_beneficiario_meta
        self.cid_beneficiario_meta = cid_beneficiario_meta
        self.data_de_nascimento = data_de_nascimento
        self.telefone_beneficiario_meta = telefone_beneficiario_meta
        self.tipo_sanguineo_beneficiario_meta = tipo_sanguineo_beneficiario_meta
        self.naturalidade_beneficiario_meta = naturalidade_beneficiario_meta
        self.expedicao = expedicao
        self.vencimento = vencimento
        self.endereco_beneficiario = endereco_beneficiario
        self.nome_da_mae_meta = nome_da_mae_meta
        self.nome_do_pai_meta = nome_do_pai_meta
        self.nome_responsavel_legal_do_beneficiario_meta = nome_responsavel_legal_do_beneficiario_meta
        self.rg_responsavel_meta = rg_responsavel_meta
        self.telefone_responsavel_meta = telefone_responsavel_meta
        self.endereco_responsavel = endereco_responsavel
        self.foto_3x4 = foto_3x4
        self.foto_digital = foto_digital
        self.url_qr_code = url_qr_code
        self.via_meta = via_meta
        self.email_meta = email_meta
    

class LoteAlertsRequest:
  def __init__(self, lote, nome, cpf, alert_id, numero_carteira,
               foto_3x4, foto_digital, hashId, vencimento, expedicao,
               via_meta, meta, created_at, updated_at, email):
    self.lote = lote
    self.nome = nome
    self.cpf = cpf
    self.alert_id = alert_id
    self.numero_carteira = numero_carteira
    self.foto_3x4 = foto_3x4
    self.foto_digital = foto_digital
    self.hashId = hashId
    self.vencimento = vencimento
    self.expedicao = expedicao
    self.via_meta = via_meta
    self.meta = json.loads(meta)
    self.created_at = created_at
    self.updated_at = updated_at
    self.email = email

class LastNumberLote:
  def __init__(self, last_lote):
    self.last_lote = last_lote

class CarteiraRequest:
  def __init__(self, id,
               alert_id, numero_carteira,
               nome, cpf, foto_3x4,
               foto_digital, hashId,
               vencimento, expedicao,
               lote, auditor,
               statusId, meta,
               created_at, updated_at) -> None:
    self.id = id
    self.alert_id = alert_id
    self.numero_carteira = numero_carteira
    self.nome = nome
    self.cpf = cpf
    self.foto_3x4 = foto_3x4
    self.foto_digital = foto_digital
    self.hashId = hashId
    self.vencimento = vencimento
    self.expedicao = expedicao
    self.lote = lote
    self.auditor = auditor
    self.statusId = statusId
    self.meta = json.loads(meta)
    self.created_at = created_at
    self.updated_at = updated_at

class InformationsCarteirinhaPCD(BaseModel):
    numero_carteira: Optional[str] = None
    nome: Optional[str] = None
    foto_3x4: Optional[str] = None
    bairro_beneficiario_meta: Optional[str] = None
    numero_beneficiario_meta: Optional[str] = None
    avenida_rua_beneficiario_meta: Optional[str] = None
    cpf: Optional[str] = None
    expedicao: Optional[datetime] = None
    cid_beneficiario_meta: Optional[str] = None
    vencimento: Optional[datetime] = None
    tipo_da_deficiencia_meta: Optional[str] = None
    tipo_sanguineo_beneficiario_meta: Optional[str] = None
    rg_beneficiario_meta: Optional[str] = None
    telefone_beneficiario_meta: Optional[str] = None
    responsavel_legal_do_beneficiario_meta: Optional[str] = None
    telefone_responsavel_meta: Optional[str] = None
    hash_alert_id: str
    alert_id: int
    tipo_carteirinha: str
    
    def serialize_pessoas(results: list):
        informations = [
        InformationsCarteirinhaPCD(
            numero_carteira=result[0],
            nome=result[1],
            foto_3x4=result[2],
            bairro_beneficiario_meta=result[3],
            numero_beneficiario_meta=result[4],
            avenida_rua_beneficiario_meta=result[5],
            cpf=result[6],
            expedicao=result[7],
            cid_beneficiario_meta=result[8],
            vencimento=result[9],
            tipo_da_deficiencia_meta=result[10],
            tipo_sanguineo_beneficiario_meta=result[11],
            rg_beneficiario_meta=result[12],
            telefone_beneficiario_meta=result[13],
            responsavel_legal_do_beneficiario_meta=result[14],
            telefone_responsavel_meta=result[15],
            hash_alert_id=result[16],
            alert_id=result[17],
            tipo_carteirinha='PCD'
        ) for result in results
    ]
        values = [information for information in informations]
        values_dict = values[0]

        informations_dict = {}

        informations_dict['numero_carteira'] = values_dict.numero_carteira
        informations_dict['nome_beneficiario'] = values_dict.nome
        informations_dict['foto_3x4'] = values_dict.foto_3x4
        
        if values_dict.bairro_beneficiario_meta:
          informations_dict['endereco_beneficiario'] = '{}, Nº {}, - {}'.format(values_dict.avenida_rua_beneficiario_meta, values_dict.numero_beneficiario_meta, values_dict.bairro_beneficiario_meta)
        else:
          informations_dict['endereco_beneficiario'] = '{}, Nº {}'.format(values_dict.avenida_rua_beneficiario_meta, values_dict.numero_beneficiario_meta)
        
        informations_dict['cpf_beneficiario'] = values_dict.cpf
        if values_dict.expedicao:
          informations_dict['expedicao'] = values_dict.expedicao.date().strftime('%d/%m/%Y')
        else: None
        informations_dict['cid_beneficiario'] = values_dict.cid_beneficiario_meta
        if values_dict.vencimento:
          informations_dict['validade'] = values_dict.vencimento.date().strftime('%d/%m/%Y')
        else: None
        informations_dict['deficiencia'] = values_dict.tipo_da_deficiencia_meta
        informations_dict['tipo_sanguineo'] = values_dict.tipo_sanguineo_beneficiario_meta
        informations_dict['rg_beneficiario'] = values_dict.rg_beneficiario_meta
        informations_dict['telefone_beneficiario'] = values_dict.telefone_beneficiario_meta
        informations_dict['responsavel_do_beneficiario'] = values_dict.responsavel_legal_do_beneficiario_meta
        if values_dict.telefone_responsavel_meta == 'sem_telefone':
          informations_dict['telefone_responsavel'] = " "
        else:
          informations_dict['telefone_responsavel'] = values_dict.telefone_responsavel_meta

        informations_dict['hash_id'] = values_dict.hash_alert_id
        informations_dict['alert_id'] = values_dict.alert_id
        informations_dict['tipo_carteirinha'] = 'PCD'

      
        
        return informations_dict
    
class InformationsCarteirinhaCIPTEA(BaseModel):
    numero_carteira: Optional[str] = None
    nome: Optional[str] = None
    foto_3x4: Optional[str] = None
    foto_digital: Optional[str] = None
    bairro_beneficiario_meta: Optional[str] = None
    numero_beneficiario_meta: Optional[str] = None
    avenida_rua_beneficiario_meta: Optional[str] = None
    cpf: Optional[str] = None
    expedicao: Optional[datetime] = None
    cid_beneficiario_meta: Optional[str] = None
    vencimento: Optional[datetime] = None
    tipo_sanguineo_beneficiario_meta: Optional[str] = None
    rg_beneficiario_meta: Optional[str] = None
    telefone_beneficiario_meta: Optional[str] = None
    responsavel_legal_do_beneficiario_meta: Optional[str] = None
    telefone_responsavel_meta: Optional[str] = None
    email_meta: Optional[str] = None
    hash_alert_id: str
    alert_id: int
    tipo_carteirinha: str
    
    def serialize_pessoas(results: list):
        informations = [
        InformationsCarteirinhaCIPTEA(
            numero_carteira=result[0],
            nome=result[1],
            foto_3x4=result[2],
            foto_digital=result[3],
            bairro_beneficiario_meta=result[4],
            numero_beneficiario_meta=result[5],
            avenida_rua_beneficiario_meta=result[6],
            cpf=result[7],
            expedicao=result[8],
            cid_beneficiario_meta=result[9],
            vencimento=result[10],
            tipo_sanguineo_beneficiario_meta=result[11],
            rg_beneficiario_meta=result[12],
            telefone_beneficiario_meta=result[13],
            responsavel_legal_do_beneficiario_meta=result[14],
            telefone_responsavel_meta=result[15],
            email_meta=result[16],
            hash_alert_id=result[17],
            alert_id=result[18],
            tipo_carteirinha='CIPTEA'
        ) for result in results
    ]
        values = [information for information in informations]
        values_dict = values[0]

        informations_dict = {}

        informations_dict['numero_carteira'] = values_dict.numero_carteira
        informations_dict['nome_beneficiario'] = values_dict.nome
        informations_dict['foto_3x4'] = values_dict.foto_3x4
        informations_dict['foto_digital'] = values_dict.foto_digital
        
        if values_dict.bairro_beneficiario_meta:
          informations_dict['endereco_beneficiario'] = '{}, Nº {}, - {}'.format(values_dict.avenida_rua_beneficiario_meta, values_dict.numero_beneficiario_meta, values_dict.bairro_beneficiario_meta)
        else:
          informations_dict['endereco_beneficiario'] = '{}, Nº {}'.format(values_dict.avenida_rua_beneficiario_meta, values_dict.numero_beneficiario_meta)
        
        informations_dict['cpf_beneficiario'] = values_dict.cpf
        
        if values_dict.expedicao:
          informations_dict['expedicao'] = values_dict.expedicao.date().strftime('%d/%m/%Y')
        else: None
        informations_dict['cid_beneficiario'] = values_dict.cid_beneficiario_meta
        
        if values_dict.vencimento:
          informations_dict['validade'] = values_dict.vencimento.date().strftime('%d/%m/%Y')
        else: None
        
        informations_dict['tipo_sanguineo'] = values_dict.tipo_sanguineo_beneficiario_meta
        informations_dict['rg_beneficiario'] = values_dict.rg_beneficiario_meta
        informations_dict['telefone_beneficiario'] = values_dict.telefone_beneficiario_meta
        informations_dict['responsavel_do_beneficiario'] = values_dict.responsavel_legal_do_beneficiario_meta
        
        if values_dict.telefone_responsavel_meta == 'sem_telefone':
          informations_dict['telefone_responsavel'] = " "
        else:
          informations_dict['telefone_responsavel'] = values_dict.telefone_responsavel_meta

        informations_dict['email'] = values_dict.email_meta
        informations_dict['hash_id'] = values_dict.hash_alert_id
        informations_dict['alert_id'] = values_dict.alert_id

        informations_dict['tipo_carteirinha'] = 'CIPTEA'
        
        return informations_dict


class AprovedCIPTEA:
  def __init__(self, numero_carteira, foto_3x4, nome, cpf, rg_beneficiario_meta, 
                 cid_beneficiario, data_de_nascimento, telefone_beneficiario_meta, 
                 tipo_sanguineo_beneficiario_meta, naturalidade_beneficiario, 
                 expedicao, vencimento, endereco_beneficiario,  
                 filiacao, 
                 nome_responsavel_legal_do_beneficiario_meta, rg_responsavel_meta, 
                 email_meta, telefone_responsavel_meta, endereco_responsavel, 
                 foto_digital, url_qr_code):
        self.numero_carteira = numero_carteira
        self.foto_3x4 = self._verify_image(foto_3x4) if foto_3x4 != None else None
        self.nome = nome
        self.cpf = cpf
        self.rg_beneficiario_meta = rg_beneficiario_meta
        self.cid_beneficiario = cid_beneficiario
        self.data_de_nascimento = data_de_nascimento
        self.telefone_beneficiario_meta = telefone_beneficiario_meta
        self.tipo_sanguineo_beneficiario_meta = tipo_sanguineo_beneficiario_meta
        self.naturalidade_beneficiario = naturalidade_beneficiario
        self.expedicao = expedicao
        self.vencimento = vencimento
        self.endereco_beneficiario = endereco_beneficiario
        self.filiacao = filiacao
        self.nome_responsavel_legal_do_beneficiario_meta = nome_responsavel_legal_do_beneficiario_meta
        self.rg_responsavel_meta = rg_responsavel_meta
        self.email_meta = email_meta
        self.telefone_responsavel_meta = telefone_responsavel_meta
        self.endereco_responsavel = endereco_responsavel if endereco_responsavel != None and endereco_responsavel != '' else endereco_beneficiario
        self.foto_digital = f'https://sejusc-pcd-ciptea-images.s3.sa-east-1.amazonaws.com/{foto_digital}' if foto_digital != None else None
        self.url_qr_code = url_qr_code

  def _verify_image(self, image):
    url_s3 = 'https://sejusc-pcd-ciptea-images.s3.sa-east-1.amazonaws.com/{image}'
    url_monitoramento = 'https://sa-east-1-uploads.s3.amazonaws.com/100760000427/attachments/image/{image}'
        
    image_s3 = url_s3.format(image=image)
    response = requests.head(image_s3)
    
    if response.status_code == 200:
        return image_s3
    elif response.status_code != 200:
        # Se o status code for 403, tenta a segunda URL
        return url_monitoramento.format(image=image)

class LastNumberApproved:
  def __init__(self, last_number):
    self.last_number = last_number

class SolicitationHashId:
  def __init__(self, hashId):
    self.hashId = hashId
  

class AprovadoAlertId:
  def __init__(self, alert_id) -> None:
    self.alert_id = alert_id

class SolicitationRequest:
  def __init__(self, id, alert_id, auditor, resp_nome, idade, cid, deficiencia, local_retirada, municipio_naturalidade, 
               municipios_endereco, meta, attachments, statusId, channelId, via, external_id,
                motivo_reprovado, comentario_beneficiario, justificativa_recurso, tag_recurso, anexos_pendentes, created_at, updated_at) -> None:
    self.id = id
    self.alert_id = alert_id
    self.auditor = auditor
    self.resp_nome = resp_nome
    self.idade = idade
    self.cid = cid
    self.deficiencia = deficiencia
    self.local_retirada = local_retirada
    self.municipio_naturalidade = municipio_naturalidade
    self.municipios_endereco = municipios_endereco
    self.meta = json.loads(meta)
    self.attachments = json.loads(attachments)
    self.statusId = statusId
    self.channelId = channelId
    self.via = via
    self.external_id = external_id
    self.motivo_reprovado = motivo_reprovado
    self.comentario_beneficiario = comentario_beneficiario
    self.justificativa_recurso = justificativa_recurso
    self.tag_recurso = tag_recurso
    self.anexos_pendentes = anexos_pendentes
    self.created_at = created_at
    self.updated_at = updated_at

class SolicitationRecepcao:
    def __init__(self, benef_cpf, hashId, nome, alert_id, tipo_da_deficiencia_meta, local_de_retirada, 
                 municipios_naturalidade_meta, cid, carteirinha, status, created_at):
        self.benef_cpf = benef_cpf
        self.hashId = hashId
        self.nome = nome
        self.alert_id = alert_id
        self.tipo_da_deficiencia_meta = tipo_da_deficiencia_meta
        self.local_de_retirada = local_de_retirada
        self.municipios_naturalidade_meta = municipios_naturalidade_meta
        self.cid = cid
        self.carteirinha = carteirinha
        self.status = status
        self.created_at = created_at

class CountRecepcao:
  def __init__(self, count) -> None:
    self.count = count

class SolicitationAlertRequest:
  def __init__(self, id, alert_id, benef_cpf, meta, attachments, attachments_recurso, statusId, channelId, tipo_carteira, updated_at, created_at) -> None:
    self.id = id
    self.alert_id = alert_id
    self.benef_cpf = benef_cpf
    self.meta = json.loads(meta)
    self.attachments = json.loads(attachments)
    try:
      self.attachments_recurso = json.loads(attachments_recurso)
    except:
      self.attachments_recurso = json.loads('{}')
    self.statusId = statusId
    self.channelId = channelId
    self.via = tipo_carteira
    self.updated_at = updated_at
    self.created_at = created_at

class CountSolicitationRequest:
  def __init__(self, count):
    self.count = count

class HistoryRequest:
  def __init__(self, id, alert_id, carteira, auditor, meta, modified, statusId, via, created_at) -> None:

    self.id = id
    self.alert_id = alert_id
    self.carteira = carteira
    self.auditor = auditor
    self.meta = json.loads(meta)
    self.modified = modified
    self.statusId = statusId
    self.via = via
    self.created_at = created_at
    try:
      self.modified = json.loads(modified)
    except:
      self.modified = json.loads('{}')

class HistoryByCPF:
  def __init__(self, alert_id, statusId, channelId, tipo_carteira, created_at, auditor ,motivo_reprovado, comentario) -> None:
    self.alert_id = alert_id
    self.statusId = statusId
    self.channelId = 'PCD' if channelId == 12836 else 'CIPTEA'
    self.tipo_carteira = tipo_carteira
    self.created_at = created_at
    self.auditor = auditor
    self.motivo_reprovado = motivo_reprovado
    self.comentario = comentario
  
class AlertEventsBYCPF:
  def __init__(self, alert_id, carteira, status_meta, comment_meta, name_author, createdAt) -> None:
    self.alert_id = alert_id
    self.carteira = 'PCD' if carteira == 12836 else 'CIPTEA'
    self.status_meta = status_meta
    self.comment_meta = comment_meta
    self.name_author = name_author
    self.createdAt = createdAt
      
class SolicitationByhashId:
  def __init__(self, alert_id ,benef_cpf ,benef_nome ,benef_rg ,benef_data_nasc ,cid ,fator_rh ,resp_nome ,resp_rg , benef_telefone, resp_telefone, meta, local_de_retirada, municipios_naturalidade_meta, tipo_da_deficiencia_meta, external_id, created_at, tipo_carteira, statusId, channelId, attachments, resp_email, sexo_beneficiario, attachments_recurso) -> None:
    self.alert_id = alert_id
    self.benef_cpf = benef_cpf
    self.benef_nome = benef_nome
    self.benef_rg = benef_rg
    self.benef_data_nasc = benef_data_nasc if benef_data_nasc != None else json.loads(meta).get('data_nascimento')
    self.cid = cid
    self.fator_rh = fator_rh
    self.resp_nome = resp_nome
    self.resp_rg= resp_rg
    self.benef_telefone = benef_telefone
    self.resp_telefone = resp_telefone
    self.naturalidade, self.nome_da_mae, self.nome_do_pai, self.maioridade , self.descricao_motivo_2via = self._extract_data_beneficiario(meta)
    self.responsavel_legal_do_beneficiario_menor, self.cpf_responsavel, self.responsavel_legal_do_beneficiario = self._extract_data_responsavel(meta)
    self.cep_beneficiario, self.municipios_endereco_beneficiario, self.bairro_beneficiario, self.avenida_rua_beneficiario, self.numero_beneficiario = self._extract_data_endereco(meta)
    self.local_de_retirada = local_de_retirada
    self.municipios_naturalidade_meta = municipios_naturalidade_meta
    self.tipo_da_deficiencia_meta = tipo_da_deficiencia_meta
    self.external_id = external_id
    self.created_at = created_at
    self.tipo_carteira = tipo_carteira
    self.statusId = statusId
    self.channelId = channelId
    self.cep_responsavel, self.bairro_responsavel, self.numero_responsavel, self.municipio_responsavel, self.rua_avenida_responsavel, self.endereco_do_responsavel = self._extract_data_endereco_responsavel(meta)
    extracted_info = self._extract_attachments_info(attachments)
    (
        self.doc_cid_laudo,
        self.anexo_comprovacao_2via,
        self.doc_cpf_do_beneficiario_anexo,
        self.doc_rg_beneficiario_verso_anexo,
        self.doc_comprovante_de_endereco_anexo,
        self.doc_foto_3_x_4_beneficiario_anexo,
        self.doc_rg_do_beneficiario_frente_anexo,
        self.doc_curatela_anexo,
        self.doc_cpf_responsavel_legal_anexo,
        self.doc_rg_responsavel_legal_verso_anexo,
        self.doc_rg_responsavel_legal_frente_anexo,
        self.doc_comprovante_endereco_responsavel_legal_anexo,
        self.biometria_do_beneficiario
    ) = extracted_info
    self.resp_email = resp_email
    self.sexo_beneficiario = sexo_beneficiario
    try :
      self.attachments_recurso = self._format_attachments_recurso(attachments_recurso)
    except:
      self.attachments_recurso = json.loads('{}')

  def _extract_data_beneficiario(self, meta):
    try:
      meta_dict = json.loads(meta)
      naturalidade = meta_dict.get('naturalidade') or meta_dict.get('naturalidade_beneficiario') or meta_dict.get('naturalidade_do_estrangeiro')
      nome_da_mae = meta_dict.get('nome_da_mae') or meta_dict.get('nome_mae')
      nome_do_pai = meta_dict.get('nome_do_pai') or meta_dict.get('nome_pai')
      maioridade = meta_dict.get('maioridade')
      descricao_motivo_2via = meta_dict.get('descricao_motivo_2via')

      return naturalidade, nome_da_mae, nome_do_pai, maioridade, descricao_motivo_2via
    except (json.JSONDecodeError, AttributeError):
            print("Erro ao decodificar o JSON ou meta não fornecido.")
            return None, None
    
  def _extract_data_responsavel(self, meta):
    try:
      meta_dict = json.loads(meta)
      responsavel_legal_do_beneficiario_menor = meta_dict.get('responsavel_legal_do_beneficiario_menor')
      cpf_responsavel = meta_dict.get('cpf_responsavel') or meta_dict.get('resp_cpf')
      responsavel_legal_do_beneficiario = meta_dict.get('responsavel_legal_do_beneficiario')
      return responsavel_legal_do_beneficiario_menor, cpf_responsavel, responsavel_legal_do_beneficiario
    
    except (json.JSONDecodeError, AttributeError):
        print('Erro ao decodificar o JSON ou meta não fornecido')
        return None, None
    
  def _extract_data_endereco(self, meta):
    try:
      meta_dict = json.loads(meta)
      cep_beneficiario = meta_dict.get('cep_beneficiario') or meta_dict.get('benef_cep')
      municipios_endereco_beneficiario = meta_dict.get('municipios_endereco_beneficiario') or meta_dict.get('municipios_beneficiario') or meta_dict.get('benef_municipio')
      bairro_beneficiario = meta_dict.get('bairro_beneficiario') or meta_dict.get('outro_bairro_beneficiario') or meta_dict.get('outro_bairro') or meta_dict.get('benef_bairro')
      avenida_rua_beneficiario = meta_dict.get('avenida_rua_beneficiario') or meta_dict.get('avenidade_rua_beneficiario') or meta_dict.get('benef_logradouro')
      numero_beneficiario = meta_dict.get('numero_beneficiario') or meta_dict.get('benef_numero')
      return cep_beneficiario, municipios_endereco_beneficiario, bairro_beneficiario, avenida_rua_beneficiario, numero_beneficiario
    except (json.JSONDecodeError, AttributeError):
      print('Erro ao decodificar o JSON ou meta não fornecido')
      return None, None
    
  def _extract_data_endereco_responsavel(self, meta):
    try:
      meta_dict = json.loads(meta)
      cep_responsavel = meta_dict.get('cep_responsavel') or meta_dict.get('resp_cep')
      bairro_responsavel = meta_dict.get('bairro_responsavel') or meta_dict.get('resp_bairro')
      numero_responsavel = meta_dict.get('numero_responsavel') or meta_dict.get('resp_numero')
      municipio_responsavel = meta_dict.get('municipio_responsavel') or meta_dict.get('resp_municipio')
      rua_avenida_responsavel = meta_dict.get('rua_avenida_responsavel') or meta_dict.get('resp_logradouro')
      endereco_do_responsavel = meta_dict.get('endereco_do_responsavel') or meta_dict.get('endereco_responsavel')
      return cep_responsavel, bairro_responsavel, numero_responsavel, municipio_responsavel, rua_avenida_responsavel, endereco_do_responsavel
    except (json.JSONDecodeError, AttributeError):
      print('Erro ao decodificar o JSON ou meta não fornecido')
      return None, None
    
  def _format_attachments_recurso(self, attachments):
    base_url = "https://sejusc-pcd-ciptea-images.s3.sa-east-1.amazonaws.com/recurso/" 
    attachments_com_url = []
    for valor in attachments.values():
      attachments_com_url.append(base_url + valor)


    return attachments_com_url

  
  def _extract_attachments_info(self, attachments):
    try:
        meta_dict = json.loads(attachments)
        
        doc_cid_laudo = meta_dict.get('doc_laudo_cid_anexo') or  meta_dict.get('doc_cid_laudo_anexo')
        if doc_cid_laudo != None:
          doc_cid_laudo = extract_attachments_images(doc_cid_laudo) 
        
        anexo_comprovacao_2via = meta_dict.get('anexo_comprovacao_2via')
        if anexo_comprovacao_2via != None:
          anexo_comprovacao_2via = extract_attachments_images(anexo_comprovacao_2via)
        
        doc_cpf_do_beneficiario_anexo = meta_dict.get('doc_cpf_do_beneficiario_anexo') or meta_dict.get("doc_cpf_beneficiario_anexo")
        if doc_cpf_do_beneficiario_anexo != None:
          doc_cpf_do_beneficiario_anexo = extract_attachments_images(doc_cpf_do_beneficiario_anexo)
        
        doc_rg_beneficiario_verso_anexo = meta_dict.get('doc_rg_beneficiario_verso_anexo')
        if doc_rg_beneficiario_verso_anexo != None:
          doc_rg_beneficiario_verso_anexo = extract_attachments_images(doc_rg_beneficiario_verso_anexo)
        
        doc_comprovante_de_endereco_anexo = meta_dict.get('doc_comprovante_de_endereco_anexo') or meta_dict.get("doc_comprovante_endereco_beneficiario_anexo")
        if doc_comprovante_de_endereco_anexo != None:
          doc_comprovante_de_endereco_anexo = extract_attachments_images(doc_comprovante_de_endereco_anexo)
        
        doc_foto_3_x_4_beneficiario_anexo = meta_dict.get("doc_foto_3_x_4_beneficiario_anexo") or meta_dict.get("doc_foto_3x_4_beneficiario_anexo")
        if doc_foto_3_x_4_beneficiario_anexo != None:
          doc_foto_3_x_4_beneficiario_anexo = extract_attachments_images(doc_foto_3_x_4_beneficiario_anexo)
        
        doc_rg_do_beneficiario_frente_anexo = meta_dict.get("doc_rg_do_beneficiario_frente_anexo") or meta_dict.get("doc_rg_beneficiario_frente_anexo")
        if doc_rg_do_beneficiario_frente_anexo:
          doc_rg_do_beneficiario_frente_anexo  = extract_attachments_images(doc_rg_do_beneficiario_frente_anexo) 

        doc_curatela_anexo = meta_dict.get('doc_curatela_anexo') or meta_dict.get("doc_tutela_do_menor_anexo")
        if doc_curatela_anexo != None:
          doc_curatela_anexo = extract_attachments_images(doc_curatela_anexo)
        
        doc_cpf_responsavel_legal_anexo = meta_dict.get('doc_cpf_reponsavel_legal_anexo') or meta_dict.get("doc_cpf_responsavel_legal_anexo")
        if doc_cpf_responsavel_legal_anexo != None:
          doc_cpf_responsavel_legal_anexo = extract_attachments_images(doc_cpf_responsavel_legal_anexo)

        doc_rg_responsavel_legal_verso_anexo = meta_dict.get('doc_rg_responsavel_legal_verso_anexo')
        if doc_rg_responsavel_legal_verso_anexo != None:
          doc_rg_responsavel_legal_verso_anexo = extract_attachments_images(doc_rg_responsavel_legal_verso_anexo)

        doc_rg_responsavel_legal_frente_anexo = meta_dict.get('doc_rg_responsavel_legal_frente_anexo')
        if doc_rg_responsavel_legal_frente_anexo != None:
          doc_rg_responsavel_legal_frente_anexo = extract_attachments_images(doc_rg_responsavel_legal_frente_anexo)
        
        doc_comprovante_endereco_responsavel_legal_anexo = meta_dict.get('doc_comprovante_endereco_responsavel_legal_anexo')
        if doc_comprovante_endereco_responsavel_legal_anexo != None:
          doc_comprovante_endereco_responsavel_legal_anexo = extract_attachments_images(doc_comprovante_endereco_responsavel_legal_anexo)

        biometria_do_beneficiario = meta_dict.get('biometria_do_beneficiario')
        if biometria_do_beneficiario != None:
          biometria_do_beneficiario = extract_attachments_images(biometria_do_beneficiario)
       
        # Verifica se algum dos valores é vazio e substitui por None
        if any(value == '' for value in (doc_cid_laudo, anexo_comprovacao_2via, doc_cpf_do_beneficiario_anexo, doc_rg_beneficiario_verso_anexo, doc_comprovante_de_endereco_anexo, doc_foto_3_x_4_beneficiario_anexo, doc_rg_do_beneficiario_frente_anexo, doc_curatela_anexo, doc_cpf_responsavel_legal_anexo, doc_rg_responsavel_legal_verso_anexo, doc_rg_responsavel_legal_frente_anexo, doc_comprovante_endereco_responsavel_legal_anexo, biometria_do_beneficiario)):
            return (None, None, None, None, None, None, None, None, None, None, None, None)
        
        return (doc_cid_laudo, anexo_comprovacao_2via, doc_cpf_do_beneficiario_anexo, doc_rg_beneficiario_verso_anexo, doc_comprovante_de_endereco_anexo, doc_foto_3_x_4_beneficiario_anexo, doc_rg_do_beneficiario_frente_anexo, doc_curatela_anexo, doc_cpf_responsavel_legal_anexo, doc_rg_responsavel_legal_verso_anexo, doc_rg_responsavel_legal_frente_anexo, doc_comprovante_endereco_responsavel_legal_anexo, biometria_do_beneficiario)
    except Exception as e:
        print(f"Erro ao extrair informações dos anexos: {e}")
        return (None, None, None, None, None, None, None, None, None, None, None, None)


class HistoryByAlertId:
  def __init__(self, alert_id, nome, cpf, carteira, maioridade_meta, nome_da_mae_meta, nome_do_pai_meta, 
               bairro_beneficiario_meta, tipo_carteira_meta, rg_responsavel_meta, cep_responsavel_meta, cpf_responsavel_meta,
               rg_beneficiario_meta, cep_beneficiario_meta, cid_beneficiario_meta, municipios_naturalidade_meta,
               cid2_beneficiario_meta, local_de_retirada_meta, bairro_responsavel_meta, numero_responsavel_meta,
              para_quem_cadastro_meta, numero_beneficiario_meta, motivo_2_via_meta, nome_do_beneficiario_meta, 
              municipio_responsavel_meta, endereco_do_responsavel_meta, municipios_beneficiario_meta, 
              rua_avenida_responsavel_meta, telefone_1_beneficiario_meta, telefone_2_beneficiario_meta, 
              avenida_rua_beneficiario_meta, sexo_genero_beneficiario_meta, estado_civil_beneficiario_meta, 
              naturalidade_beneficiario_meta, nacionalidade_beneficiario_meta, tipo_sanguineo_beneficiario_meta,
              municipio_realizado_cadastro_meta, orgao_expedidor_beneficiario_meta, 
              data_de_nascimento_beneficiario_meta, tipo_da_deficiencia_beneficiario_meta, 
              nome_responsavel_legal_do_beneficiario_meta, responsavel_legal_do_beneficiario_meta, 
              responsavel_legal_do_beneficiario_menor_meta, statusId, created_at) -> None:
    
        self.alert_id = alert_id
        self.nome = nome
        self.cpf = cpf
        self.carteira = carteira
        self.maioridade_meta = maioridade_meta 
        self.nome_da_mae_meta = nome_da_mae_meta 
        self.nome_do_pai_meta = nome_do_pai_meta 
        self.bairro_beneficiario_meta = bairro_beneficiario_meta 
        self.tipo_carteira_meta = tipo_carteira_meta 
        self.rg_responsavel_meta = rg_responsavel_meta 
        self.cep_responsavel_meta = cep_responsavel_meta 
        self.rg_beneficiario_meta = rg_beneficiario_meta 
        self.cep_beneficiario_meta = cep_beneficiario_meta
        self.cpf_responsavel_meta = cpf_responsavel_meta
        self.cid_beneficiario_meta = cid_beneficiario_meta
        self.municipios_naturalidade_meta = municipios_naturalidade_meta 
        self.cid2_beneficiario_meta = cid2_beneficiario_meta 
        self.local_de_retirada_meta = local_de_retirada_meta 
        self.bairro_responsavel_meta = bairro_responsavel_meta 
        self.numero_responsavel_meta = numero_responsavel_meta 
        self.para_quem_cadastro_meta = para_quem_cadastro_meta 
        self.numero_beneficiario_meta = numero_beneficiario_meta
        self.motivo_2_via_meta = motivo_2_via_meta
        self.nome_do_beneficiario_meta = nome_do_beneficiario_meta 
        self.municipio_responsavel_meta = municipio_responsavel_meta 
        self.endereco_do_responsavel_meta = endereco_do_responsavel_meta 
        self.municipios_beneficiario_meta = municipios_beneficiario_meta 
        self.rua_avenida_responsavel_meta = rua_avenida_responsavel_meta 
        self.telefone_1_beneficiario_meta = telefone_1_beneficiario_meta 
        self.telefone_2_beneficiario_meta = telefone_2_beneficiario_meta 
        self.avenida_rua_beneficiario_meta = avenida_rua_beneficiario_meta 
        self.sexo_genero_beneficiario_meta = sexo_genero_beneficiario_meta
        self.estado_civil_beneficiario_meta = estado_civil_beneficiario_meta
        self.naturalidade_beneficiario_meta = naturalidade_beneficiario_meta
        self.nacionalidade_beneficiario_meta = nacionalidade_beneficiario_meta
        self.tipo_sanguineo_beneficiario_meta = tipo_sanguineo_beneficiario_meta
        self.municipio_realizado_cadastro_meta = municipio_realizado_cadastro_meta
        self.orgao_expedidor_beneficiario_meta = orgao_expedidor_beneficiario_meta
        self.data_de_nascimento_beneficiario_meta = data_de_nascimento_beneficiario_meta
        self.tipo_da_deficiencia_beneficiario_meta = tipo_da_deficiencia_beneficiario_meta
        self.nome_responsavel_legal_do_beneficiario_meta = nome_responsavel_legal_do_beneficiario_meta
        self.responsavel_legal_do_beneficiario_meta = responsavel_legal_do_beneficiario_meta
        self.responsavel_legal_do_beneficiario_menor_meta = responsavel_legal_do_beneficiario_menor_meta 
        self.statusId = statusId
        self.created_at = created_at

    
class HistoryModifiedByAlertId:
  def __init__(self, cid_modified, resp_rg_modified, benef_rg_modified, nome_mae_modified, nome_pai_modified,
                 resp_cep_modified, resp_cpf_modified, benef_cep_modified, benef_cpf_modified, resp_nome_modified,
                 benef_nome_modified, resp_bairro_modified, resp_numero_modified, benef_bairro_modified,
                 benef_numero_modified, naturalidade_modified, resp_municipio_modified, tipo_sanguineo_modified,
                 benef_municipio_modified, data_nascimento_modified, resp_logradouro_modified,
                 benef_logradouro_modified, resp_endereco_completo_modified, benef_endereco_completo_modified):
        self.cid_modified = cid_modified
        self.resp_rg_modified = resp_rg_modified
        self.benef_rg_modified = benef_rg_modified
        self.nome_mae_modified = nome_mae_modified
        self.nome_pai_modified = nome_pai_modified
        self.resp_cep_modified = resp_cep_modified
        self.resp_cpf_modified = resp_cpf_modified
        self.benef_cep_modified = benef_cep_modified
        self.benef_cpf_modified = benef_cpf_modified
        self.resp_nome_modified = resp_nome_modified
        self.benef_nome_modified = benef_nome_modified
        self.resp_bairro_modified = resp_bairro_modified
        self.resp_numero_modified = resp_numero_modified
        self.benef_bairro_modified = benef_bairro_modified
        self.benef_numero_modified = benef_numero_modified
        self.naturalidade_modified = naturalidade_modified
        self.resp_municipio_modified = resp_municipio_modified
        self.tipo_sanguineo_modified = tipo_sanguineo_modified
        self.benef_municipio_modified = benef_municipio_modified
        self.data_nascimento_modified = data_nascimento_modified
        self.resp_logradouro_modified = resp_logradouro_modified
        self.benef_logradouro_modified = benef_logradouro_modified
        self.resp_endereco_completo_modified = resp_endereco_completo_modified
        self.benef_endereco_completo_modified = benef_endereco_completo_modified

class SolicitationByAlertId:
    def __init__(self, alert_id, benef_cpf, benef_nome, attachments) -> None:
        self.alert_id = alert_id
        self.benef_cpf = benef_cpf
        self.benef_nome = benef_nome
        self.attachments = self._extract_anexos(attachments)

    def _extract_anexos(self, attachments):
      try:
        attachments_dict = json.loads(attachments)
        attachments_aninhados = attachments_dict.values()
        attachments_desaninhados = [anexo for anexos in attachments_aninhados for anexo in anexos]

        return attachments_desaninhados
      
      except:
        return None, None
      
class SolicitationMetaByAlertId:
    def __init__(self, meta) -> None:
      self.meta = meta

    def serialize_meta(requests):
      return [{
        "meta": r.meta
      }for r in requests]
    
class SolicitationOldByCPF:
  def __init__(self, alert_id, benef_cpf, benef_nome, created_at, updated_at, status, meta, channel) -> None:
    meta_dict = json.loads(meta)
    self.alert_id = alert_id
    self.benef_cpf = benef_cpf
    self.benef_nome = benef_nome
    self.created_at = created_at
    self.updated_at = updated_at
    self.status = status
    self.status_validacao = meta_dict['data'].get('status_validacao')
    self.estrutura = self._extract_channel(channel, created_at)
    
  def _extract_channel(self, channel, created_at):
    data_referencia = datetime(2022, 4, 1)

    if channel in (12837, 6790, 4499, 12836, 4495):
      if channel == 4495 and created_at < data_referencia:
        return "antiga_estrutura"
      elif channel == 4495 and created_at >= data_referencia:
        return "nova_estrutura"
      
      return "antiga_estrutura"

    elif channel in (13800, 13781, 14057):
      return  "nova_estrutura"



class DocumentRequest:
  def __init__(self, id, status, created_at, alert_id, cid, cpf, birthdate, name, mother_name, data) -> None:
    self.id = id
    self.status = status
    self.created_at = created_at
    self.external_id = alert_id
    self.cid = cid
    self.cpf = cpf
    self.birthdate = birthdate
    self.name = name
    self.mother_name = mother_name

    data = json.loads(data)

    self.attachments = data["attachments"]
    self.total_attachments = reduce(count_attachments, [(k, v) for k, v in self.attachments.items()], 0)
    self.comments = data["comments"]
    self.data = data["data"]

class Produtividade:
  def __init__(self, auditor, quantidade, total) -> None:
    self.auditor = auditor
    self.quantidade = quantidade
    self.total = total

  def update(self, status, data):
    if status in documentRequestStatus:
      self.status = status

    for k in self.data.keys():
      if k in data.keys():
        self.data[k] = data[k]

class StatusSolicitacao:
  def __init__(self, alert_id, benef_cpf, benef_nome, statusId, channelId, motivo_reprovado) -> None:
    self.alert_id = alert_id
    self.benef_cpf = benef_cpf
    self.benef_nome = benef_nome
    self.statusId = statusId
    self.channelId = channelId
    self.motivo_reprovado = motivo_reprovado

class VisualExportResponse:
    def __init__(self, alert_id: int, benef_nome: str, channelId: int, statusId: int, municipios_endereco_beneficiario_meta: str, tipo_da_deficiencia_meta: str,updated_at: str):
        self.alert_id = alert_id
        self.benef_nome = benef_nome
        self.channelId = channelId
        self.statusId = statusId
        self.municipios_endereco_beneficiario_meta = municipios_endereco_beneficiario_meta
        self.tipo_da_deficiencia_meta = tipo_da_deficiencia_meta
        self.updated_at = updated_at

# Função para serializar a contagem
class CountVisualExportResponse:
    def __init__(self, count):
        self.count = count