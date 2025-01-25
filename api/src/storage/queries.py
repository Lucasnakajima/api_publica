from enum import Enum

class Queries(str, Enum):
    get_request = '''
        SELECT id, status, 
               created_at, alert_id, 
               cid, cpf, birthdate, 
               beneficiary_name, mother_name, data 
        FROM requests WHERE alert_id=%s
    '''

    update_request = ''''
            UPDATE requests SET data=%s, status=%s WHERE alert_id=%s
    '''

    get_historico = ''' 
            select h.id, h.alert_id, h.carteira, h.auditor,
                   h.meta, h.modified,
                   h.statusId, s.tipo_carteira, h.created_at from historico h join solicitacoes s on h.alert_id=s.alert_id
            where {conditions} order by created_at {order} limit %s offset %s;
    '''

    get_solicitacoes = '''
            select id, alert_id, auditor, resp_nome, fn_CALC_IDADE(benef_data_nasc) as idade, cid, 
            tipo_da_deficiencia_meta, 
            UPPER(REPLACE(REGEXP_REPLACE(local_de_retirada_meta, '^[0-9]+_', ''), '_', ' ')) AS local_de_retirada_meta, 
            UPPER(REPLACE(municipios_naturalidade_meta, '_', ' ')) AS municipios_naturalidade_meta,
            UPPER(REPLACE(municipios_endereco_beneficiario_meta, '_', ' ')) AS municipios_endereco_beneficiario_meta, 
            meta, attachments, statusId, channelId, 
            tipo_carteira, external_id, motivo_reprovado, comentario_beneficiario, justificativa_recurso, tag_recurso, created_at, updated_at
            from solicitacoes
            where 1=1 {conditions} order by updated_at {order} limit %s offset %s;
    '''

    get_count_solicitacoes = '''
            select count(*) as count
            from solicitacoes
            where 1=1 {conditions} limit %s offset %s;
    '''

    get_solicitacao_alert = '''
            select id, alert_id, benef_cpf, meta, attachments,
                   statusId, channelId, tipo_carteira, updated_at, created_at
            from solicitacoes
            where {conditions}
    '''

    get_solicitacao_hashid = '''
                select hashId
                from solicitacoes
                where benef_cpf=%s
        '''
    get_aprovados_ciptea_alert_id = '''
    select alert_id from aprovados_ciptea where hashId = %s
    '''

    get_aprovados = '''
            select a.id, a.alert_id, a.numero_carteira, a.nome, 
            UPPER(REPLACE(a.municipios_beneficiario_meta, '_', ' ')) AS municipios_beneficiario_meta, a.cpf, 
            UPPER(REPLACE(a.cid_beneficiario_meta, '_', ' ')) AS cid_beneficiario_meta, 
            a.statusId, 
            a.tipo_da_deficiencia_meta, 
            UPPER(REPLACE(a.municipios_beneficiario_meta, '_', ' ')) AS municipios_beneficiario_meta, 
            UPPER(REPLACE(REGEXP_REPLACE(s.local_de_retirada_meta, '^[0-9]+_', ''), '_', ' ')) AS local_de_retirada_meta, 
            a.foto_3x4, a.foto_digital, a.hashId, a.vencimento, a.expedicao, a.lote, a.auditor, a.statusId, 
            a.meta, s.tipo_carteira, a.created_at, a.updated_at
            from {projeto} a join solicitacoes s on a.alert_id=s.alert_id
            where {conditions}
            order by updated_at {order} limit %s offset %s;
    '''

    get_attachments = '''
        select attachments from solicitacoes where alert_id = %s
        '''

    get_count_aprovados = '''
            select count(*) as count
            from {projeto} a join solicitacoes s on a.alert_id=s.alert_id where {conditions}
    '''

    get_last_number = '''
            select max(numero_carteira) as last_number
            from {projeto} ;
    '''

    get_cpf_hash = '''
            select benef_cpf, hashId, benef_nome, resp_nome,
            UPPER(REPLACE(municipio_realizado_cadastro_meta, '_', ' ')) AS municipio,
            UPPER(REPLACE(cid, '_', ' ')) AS cid, 
            tipo_da_deficiencia_meta, 
            UPPER(REPLACE(municipios_naturalidade_meta, '_', ' ')) AS municipios_naturalidade_meta,
            fn_CALC_IDADE(benef_data_nasc) as idade, benef_telefone, 
            UPPER(REPLACE(REGEXP_REPLACE(local_de_retirada_meta, '^[0-9]+_', ''), '_', ' ')) AS local_de_retirada_meta,
            group_concat(channelId) as channelId,
            group_concat(alert_id) as alert_id,
            MAX(DATE(CONVERT_TZ(created_at, '+00:00', '-04:00'))) AS last_created, 
            MAX(DATE(CONVERT_TZ(updated_at, '+00:00', '-04:00'))) AS last_updated, count(*) 
                from solicitacoes where {conditions}
            group by benef_cpf having 1=1 {conditions_group} order by last_created {order} limit %s offset %s;
    '''

    get_arquivados = '''
            SELECT 
        s.benef_cpf, 
        s.hashId, 
        s.benef_nome, 
        s.resp_nome,
        h.auditor AS auditor_arquivado,
        UPPER(REPLACE(s.municipio_realizado_cadastro_meta, '_', ' ')) AS municipio,
        UPPER(REPLACE(s.cid, '_', ' ')) AS cid, 
        s.tipo_da_deficiencia_meta, 
        UPPER(REPLACE(s.municipios_naturalidade_meta, '_', ' ')) AS municipios_naturalidade_meta,
        fn_CALC_IDADE(s.benef_data_nasc) as idade, 
        s.benef_telefone, 
        UPPER(REPLACE(REGEXP_REPLACE(s.local_de_retirada_meta, '^[0-9]+_', ''), '_', ' ')) AS local_de_retirada_meta,
        GROUP_CONCAT(s.channelId) as channelId,
        GROUP_CONCAT(s.alert_id) as alert_id,
        MAX(DATE(CONVERT_TZ(s.created_at, '+00:00', '-04:00'))) AS last_created, 
        MAX(DATE(CONVERT_TZ(s.updated_at, '+00:00', '-04:00'))) AS last_updated, 
        COUNT(*) AS total_solicitacoes
        FROM solicitacoes s
        LEFT JOIN historico h ON s.alert_id = h.alert_id
        AND h.statusId = s.statusId 
        WHERE s.statusId IN {status_condition} {conditions}
        GROUP BY s.benef_cpf HAVING 1=1 {conditions_group}  ORDER BY last_created {order} LIMIT %s OFFSET %s;
    '''

    get_count_cpf_hash = '''
            select count(distinct benef_cpf) as count_cpf
            from solicitacoes where {conditions}    
    '''

    get_consulta_geral = '''
                select benef_cpf,
                hashId, benef_nome, group_concat(alert_id) as alert_ids,
                tipo_da_deficiencia_meta, benef_telefone,
                UPPER(REPLACE(REGEXP_REPLACE(local_de_retirada_meta, '^[0-9]+_', ''), '_', ' ')) AS local_de_retirada_meta, 
                UPPER(REPLACE(municipios_naturalidade_meta, '_', ' ')) AS municipios_naturalidade_meta, cid, group_concat(channelId) as channelIds,
                max(created_at) as last_created, max(updated_at) as last_updated, count(*) as total
                from solicitacoes
                where {conditions}
                group by benef_cpf
                order by last_updated {order} limit %s offset %s;
    '''

    get_count_consulta_geral = '''
                select count(distinct benef_cpf) as count_cpf
                from solicitacoes
                where {conditions}  
    '''

    get_lotes = '''
                select lote, count(*) as total, max(updated_at) as updated_at, max(statusId) as statusId,
                group_concat(alert_id) as alert_id, group_concat(numero_carteira) as numero_carteira
                    from {projeto} where lote is not null {conditions}
                group by lote order by lote {order} limit %s offset %s;
        '''

    get_count_lotes = '''
                select count(distinct lote) as count
                from {projeto} where lote is not null {conditions}    
        '''

    get_lote_alerts = '''
                select lote, nome, cpf, alert_id, numero_carteira,
                foto_3x4, foto_digital, hashId, vencimento, expedicao, via_meta, meta, created_at, updated_at, email_meta
                from {projeto} where lote is not null {conditions}
                order by numero_carteira limit %s offset %s;
        '''

    get_last_lote = '''
                select max(lote) as last_lote
                from {projeto} ;
        '''
    
    get_lote_xlsx = '''
    SELECT 
    UPPER(numero_carteira) AS numero_carteira, 
    UPPER(lote) AS lote, 
    UPPER(nome) AS nome, 
    UPPER(cpf) AS cpf, 
    UPPER(rg_beneficiario_meta) AS rg_beneficiario_meta, 
    UPPER(REPLACE(cid_beneficiario_meta, '_', ' ')) AS cid_beneficiario_meta,
    UPPER(data_de_nascimento) AS data_de_nascimento, 
    UPPER(telefone_beneficiario_meta) AS telefone_beneficiario_meta, 
    CASE tipo_sanguineo_beneficiario_meta
        WHEN 'o_positivo' THEN 'O+'
        WHEN 'o_negativo' THEN 'O-'
        WHEN 'a_positivo' THEN 'A+'
        WHEN 'a_negativo' THEN 'A-'
        WHEN 'b_positivo' THEN 'B+'
        WHEN 'b_negativo' THEN 'B-'
        WHEN 'ab_positivo' THEN 'AB+'
        WHEN 'ab_negativo' THEN 'AB-'
        ELSE tipo_sanguineo_beneficiario_meta
        END AS tipo_sanguineo_beneficiario_meta, 
        UPPER(REPLACE(naturalidade_beneficiario_meta, '_', ' ')) AS naturalidade_beneficiario_meta,
        UPPER(REPLACE(municipios_beneficiario_meta, '_', ' ')) AS municipios_beneficiario_meta,
        FormatDate(expedicao) AS expedicao, 
        FormatDate(vencimento) AS vencimento, 
        UPPER(
        COALESCE(
            TRIM(CONCAT_WS(' ',
                IF(avenida_rua_beneficiario_meta != '', avenida_rua_beneficiario_meta, NULL),
                IF(numero_beneficiario_meta != '', numero_beneficiario_meta, NULL),
                IF(bairro_beneficiario_meta != '', 
                            CONCAT(', ', 
                                CASE bairro_beneficiario_meta
                                    WHEN 'adrianopolis' THEN 'Adrianópolis'
                                    WHEN 'aleixo' THEN 'Aleixo'
                                    WHEN 'alvorada' THEN 'Alvorada'
                                    WHEN 'armando_mendes' THEN 'Armando Mendes'
                                    WHEN 'betania' THEN 'Betânia'
                                    WHEN 'cachoeirinha' THEN 'Cachoeirinha'
                                    WHEN 'centro' THEN 'Centro'
                                    WHEN 'chapada' THEN 'Chapada'
                                    WHEN 'cidade_de_deus' THEN 'Cidade de Deus'
                                    WHEN 'cidade_nova' THEN 'Cidade Nova'
                                    WHEN 'colonia_antonio_aleixo' THEN 'Colônia Antônio Aleixo'
                                    WHEN 'colonia_oliveira_machado' THEN 'Colônia Oliveira Machado'
                                    WHEN 'colonia_santo_antonio' THEN 'Colônia Santo Antônio'
                                    WHEN 'colonia_terra_nova' THEN 'Colônia Terra Nova'
                                    WHEN 'compensa' THEN 'Compensa'
                                    WHEN 'coroado' THEN 'Coroado'
                                    WHEN 'crespo' THEN 'Crespo'
                                    WHEN 'da_paz' THEN 'Da Paz'
                                    WHEN 'distrito_industrial_i' THEN 'Distrito Industrial I'
                                    WHEN 'distrito_industrial_ii' THEN 'Distrito Industrial II'
                                    WHEN 'dom_pedro' THEN 'Dom Pedro'
                                    WHEN 'educandos' THEN 'Educandos'
                                    WHEN 'flores' THEN 'Flores'
                                    WHEN 'gilberto_mestrinho' THEN 'Gilberto Mestrinho'
                                    WHEN 'gloria' THEN 'Glória'
                                    WHEN 'japiim' THEN 'Japiim'
                                    WHEN 'jorge_teixeira' THEN 'Jorge Teixeira'
                                    WHEN 'lago_azul' THEN 'Lago Azul'
                                    WHEN 'lirio_do_vale' THEN 'Lírio do Vale'
                                    WHEN 'mauazinho' THEN 'Mauazinho'
                                    WHEN 'monte_das_oliveiras' THEN 'Monte das Oliveiras'
                                    WHEN 'morro_da_liberdade' THEN 'Morro da Liberdade'
                                    WHEN 'nossa_senhora_aparecida' THEN 'Nossa Senhora Aparecida'
                                    WHEN 'nossa_senhora_das_gracas' THEN 'Nossa Senhora das Graças'
                                    WHEN 'nova_cidade' THEN 'Nova Cidade'
                                    WHEN 'nova_esperanca' THEN 'Nova Esperança'
                                    WHEN 'novo_aleixo' THEN 'Novo Aleixo'
                                    WHEN 'novo_israel' THEN 'Novo Israel'
                                    WHEN 'parque_10_denovembro' THEN 'Parque 10 de Novembro'
                                    WHEN 'petropolis' THEN 'Petrópolis'
                                    WHEN 'planalto' THEN 'Planalto'
                                    WHEN 'ponta_negra' THEN 'Ponta Negra'
                                    WHEN 'praca_14_de_janeiro' THEN 'Praça 14 de Janeiro'
                                    WHEN 'prediente_vargas' THEN 'Presidente Vargas'
                                    WHEN 'puraquequara' THEN 'Puraquequara'
                                    WHEN 'raiz' THEN 'Raiz'
                                    WHEN 'redencao' THEN 'Redenção'
                                    WHEN 'santa_etelvina' THEN 'Santa Etelvina'
                                    WHEN 'santa_luizia' THEN 'Santa Luzia'
                                    WHEN 'santo_agostinho' THEN 'Santo Agostinho'
                                    WHEN 'santo_antonio' THEN 'Santo Antônio'
                                    WHEN 'sao_francisco' THEN 'São Francisco'
                                    WHEN 'sao_geraldo' THEN 'São Geraldo'
                                    WHEN 'sao_jorge' THEN 'São Jorge'
                                    WHEN 'sao_jose_operario' THEN 'São José Operário'
                                    WHEN 'sao_lazaro' THEN 'São Lazaro'
                                    WHEN 'sao_raimundo' THEN 'São Raimundo'
                                    WHEN 'tancredo_neves' THEN 'Tancredo Neves'
                                    WHEN 'taruma' THEN 'Tarumã'
                                    WHEN 'taruma_acu' THEN 'Tarumã-Açu'
                                    WHEN 'vila_buriti' THEN 'Vila Buriti'
                                    WHEN 'vila_da_prata' THEN 'Vila da Prata'
                                    WHEN 'zumbi_dos_palmares' THEN 'Zumbi dos Palmares'
                                    WHEN 'santa_ines' THEN 'Santa Inês'
                                    WHEN 'joao_paulo' THEN 'João Paulo'
                                    ELSE bairro_beneficiario_meta
                                END
                            ), 
                        NULL),
                IF(cep_beneficiario_meta != '', CONCAT('- ', cep_beneficiario_meta), NULL)
            )), ''
        )
        ) AS endereco_beneficiario, 
        UPPER(nome_da_mae_meta) AS nome_da_mae_meta, 
        UPPER(nome_do_pai_meta) AS nome_do_pai_meta, 
        UPPER(nome_responsavel_legal_do_beneficiario_meta) AS nome_responsavel_legal_do_beneficiario_meta, 
        UPPER(rg_responsavel_meta) AS rg_responsavel_meta, 
        UPPER(telefone_responsavel_meta) AS telefone_responsavel_meta, 
        UPPER(
        TRIM(
            COALESCE(
                IF(
                    (rua_avenida_responsavel_meta IS NULL OR rua_avenida_responsavel_meta = '') AND
                    (bairro_responsavel_meta IS NULL OR bairro_responsavel_meta = '') AND
                    (cep_responsavel_meta IS NULL OR cep_responsavel_meta = ''),
                    UPPER(
        COALESCE(
            TRIM(CONCAT_WS(' ',
                IF(avenida_rua_beneficiario_meta != '', avenida_rua_beneficiario_meta, NULL),
                IF(numero_beneficiario_meta != '', numero_beneficiario_meta, NULL),
                IF(bairro_beneficiario_meta != '', 
                            CONCAT(', ', 
                                CASE bairro_beneficiario_meta
                                    WHEN 'adrianopolis' THEN 'Adrianópolis'
                                    WHEN 'aleixo' THEN 'Aleixo'
                                    WHEN 'alvorada' THEN 'Alvorada'
                                    WHEN 'armando_mendes' THEN 'Armando Mendes'
                                    WHEN 'betania' THEN 'Betânia'
                                    WHEN 'cachoeirinha' THEN 'Cachoeirinha'
                                    WHEN 'centro' THEN 'Centro'
                                    WHEN 'chapada' THEN 'Chapada'
                                    WHEN 'cidade_de_deus' THEN 'Cidade de Deus'
                                    WHEN 'cidade_nova' THEN 'Cidade Nova'
                                    WHEN 'colonia_antonio_aleixo' THEN 'Colônia Antônio Aleixo'
                                    WHEN 'colonia_oliveira_machado' THEN 'Colônia Oliveira Machado'
                                    WHEN 'colonia_santo_antonio' THEN 'Colônia Santo Antônio'
                                    WHEN 'colonia_terra_nova' THEN 'Colônia Terra Nova'
                                    WHEN 'compensa' THEN 'Compensa'
                                    WHEN 'coroado' THEN 'Coroado'
                                    WHEN 'crespo' THEN 'Crespo'
                                    WHEN 'da_paz' THEN 'Da Paz'
                                    WHEN 'distrito_industrial_i' THEN 'Distrito Industrial I'
                                    WHEN 'distrito_industrial_ii' THEN 'Distrito Industrial II'
                                    WHEN 'dom_pedro' THEN 'Dom Pedro'
                                    WHEN 'educandos' THEN 'Educandos'
                                    WHEN 'flores' THEN 'Flores'
                                    WHEN 'gilberto_mestrinho' THEN 'Gilberto Mestrinho'
                                    WHEN 'gloria' THEN 'Glória'
                                    WHEN 'japiim' THEN 'Japiim'
                                    WHEN 'jorge_teixeira' THEN 'Jorge Teixeira'
                                    WHEN 'lago_azul' THEN 'Lago Azul'
                                    WHEN 'lirio_do_vale' THEN 'Lírio do Vale'
                                    WHEN 'mauazinho' THEN 'Mauazinho'
                                    WHEN 'monte_das_oliveiras' THEN 'Monte das Oliveiras'
                                    WHEN 'morro_da_liberdade' THEN 'Morro da Liberdade'
                                    WHEN 'nossa_senhora_aparecida' THEN 'Nossa Senhora Aparecida'
                                    WHEN 'nossa_senhora_das_gracas' THEN 'Nossa Senhora das Graças'
                                    WHEN 'nova_cidade' THEN 'Nova Cidade'
                                    WHEN 'nova_esperanca' THEN 'Nova Esperança'
                                    WHEN 'novo_aleixo' THEN 'Novo Aleixo'
                                    WHEN 'novo_israel' THEN 'Novo Israel'
                                    WHEN 'parque_10_denovembro' THEN 'Parque 10 de Novembro'
                                    WHEN 'petropolis' THEN 'Petrópolis'
                                    WHEN 'planalto' THEN 'Planalto'
                                    WHEN 'ponta_negra' THEN 'Ponta Negra'
                                    WHEN 'praca_14_de_janeiro' THEN 'Praça 14 de Janeiro'
                                    WHEN 'prediente_vargas' THEN 'Presidente Vargas'
                                    WHEN 'puraquequara' THEN 'Puraquequara'
                                    WHEN 'raiz' THEN 'Raiz'
                                    WHEN 'redencao' THEN 'Redenção'
                                    WHEN 'santa_etelvina' THEN 'Santa Etelvina'
                                    WHEN 'santa_luizia' THEN 'Santa Luzia'
                                    WHEN 'santo_agostinho' THEN 'Santo Agostinho'
                                    WHEN 'santo_antonio' THEN 'Santo Antônio'
                                    WHEN 'sao_francisco' THEN 'São Francisco'
                                    WHEN 'sao_geraldo' THEN 'São Geraldo'
                                    WHEN 'sao_jorge' THEN 'São Jorge'
                                    WHEN 'sao_jose_operario' THEN 'São José Operário'
                                    WHEN 'sao_lazaro' THEN 'São Lazaro'
                                    WHEN 'sao_raimundo' THEN 'São Raimundo'
                                    WHEN 'tancredo_neves' THEN 'Tancredo Neves'
                                    WHEN 'taruma' THEN 'Tarumã'
                                    WHEN 'taruma_acu' THEN 'Tarumã-Açu'
                                    WHEN 'vila_buriti' THEN 'Vila Buriti'
                                    WHEN 'vila_da_prata' THEN 'Vila da Prata'
                                    WHEN 'zumbi_dos_palmares' THEN 'Zumbi dos Palmares'
                                    WHEN 'santa_ines' THEN 'Santa Inês'
                                    WHEN 'joao_paulo' THEN 'João Paulo'
                                    ELSE bairro_beneficiario_meta
                                END
                            ), 
                        NULL),
                IF(cep_beneficiario_meta != '', CONCAT('- ', cep_beneficiario_meta), NULL)
            )), ''
        )
        ),
                    CONCAT_WS(' ',
                        IF(rua_avenida_responsavel_meta != '', rua_avenida_responsavel_meta, NULL),
                        IF(bairro_responsavel_meta != '', 
                            CONCAT(', ', 
                                CASE bairro_responsavel_meta
                                    WHEN 'adrianopolis' THEN 'Adrianópolis'
                                    WHEN 'aleixo' THEN 'Aleixo'
                                    WHEN 'alvorada' THEN 'Alvorada'
                                    WHEN 'armando_mendes' THEN 'Armando Mendes'
                                    WHEN 'betania' THEN 'Betânia'
                                    WHEN 'cachoeirinha' THEN 'Cachoeirinha'
                                    WHEN 'centro' THEN 'Centro'
                                    WHEN 'chapada' THEN 'Chapada'
                                    WHEN 'cidade_de_deus' THEN 'Cidade de Deus'
                                    WHEN 'cidade_nova' THEN 'Cidade Nova'
                                    WHEN 'colonia_antonio_aleixo' THEN 'Colônia Antônio Aleixo'
                                    WHEN 'colonia_oliveira_machado' THEN 'Colônia Oliveira Machado'
                                    WHEN 'colonia_santo_antonio' THEN 'Colônia Santo Antônio'
                                    WHEN 'colonia_terra_nova' THEN 'Colônia Terra Nova'
                                    WHEN 'compensa' THEN 'Compensa'
                                    WHEN 'coroado' THEN 'Coroado'
                                    WHEN 'crespo' THEN 'Crespo'
                                    WHEN 'da_paz' THEN 'Da Paz'
                                    WHEN 'distrito_industrial_i' THEN 'Distrito Industrial I'
                                    WHEN 'distrito_industrial_ii' THEN 'Distrito Industrial II'
                                    WHEN 'dom_pedro' THEN 'Dom Pedro'
                                    WHEN 'educandos' THEN 'Educandos'
                                    WHEN 'flores' THEN 'Flores'
                                    WHEN 'gilberto_mestrinho' THEN 'Gilberto Mestrinho'
                                    WHEN 'gloria' THEN 'Glória'
                                    WHEN 'japiim' THEN 'Japiim'
                                    WHEN 'jorge_teixeira' THEN 'Jorge Teixeira'
                                    WHEN 'lago_azul' THEN 'Lago Azul'
                                    WHEN 'lirio_do_vale' THEN 'Lírio do Vale'
                                    WHEN 'mauazinho' THEN 'Mauazinho'
                                    WHEN 'monte_das_oliveiras' THEN 'Monte das Oliveiras'
                                    WHEN 'morro_da_liberdade' THEN 'Morro da Liberdade'
                                    WHEN 'nossa_senhora_aparecida' THEN 'Nossa Senhora Aparecida'
                                    WHEN 'nossa_senhora_das_gracas' THEN 'Nossa Senhora das Graças'
                                    WHEN 'nova_cidade' THEN 'Nova Cidade'
                                    WHEN 'nova_esperanca' THEN 'Nova Esperança'
                                    WHEN 'novo_aleixo' THEN 'Novo Aleixo'
                                    WHEN 'novo_israel' THEN 'Novo Israel'
                                    WHEN 'parque_10_denovembro' THEN 'Parque 10 de Novembro'
                                    WHEN 'petropolis' THEN 'Petrópolis'
                                    WHEN 'planalto' THEN 'Planalto'
                                    WHEN 'ponta_negra' THEN 'Ponta Negra'
                                    WHEN 'praca_14_de_janeiro' THEN 'Praça 14 de Janeiro'
                                    WHEN 'prediente_vargas' THEN 'Presidente Vargas'
                                    WHEN 'puraquequara' THEN 'Puraquequara'
                                    WHEN 'raiz' THEN 'Raiz'
                                    WHEN 'redencao' THEN 'Redenção'
                                    WHEN 'santa_etelvina' THEN 'Santa Etelvina'
                                    WHEN 'santa_luizia' THEN 'Santa Luzia'
                                    WHEN 'santo_agostinho' THEN 'Santo Agostinho'
                                    WHEN 'santo_antonio' THEN 'Santo Antônio'
                                    WHEN 'sao_francisco' THEN 'São Francisco'
                                    WHEN 'sao_geraldo' THEN 'São Geraldo'
                                    WHEN 'sao_jorge' THEN 'São Jorge'
                                    WHEN 'sao_jose_operario' THEN 'São José Operário'
                                    WHEN 'sao_lazaro' THEN 'São Lazaro'
                                    WHEN 'sao_raimundo' THEN 'São Raimundo'
                                    WHEN 'tancredo_neves' THEN 'Tancredo Neves'
                                    WHEN 'taruma' THEN 'Tarumã'
                                    WHEN 'taruma_acu' THEN 'Tarumã-Açu'
                                    WHEN 'vila_buriti' THEN 'Vila Buriti'
                                    WHEN 'vila_da_prata' THEN 'Vila da Prata'
                                    WHEN 'zumbi_dos_palmares' THEN 'Zumbi dos Palmares'
                                    WHEN 'santa_ines' THEN 'Santa Inês'
                                    WHEN 'joao_paulo' THEN 'João Paulo'
                                    ELSE bairro_responsavel_meta
                                END
                            ), 
                        NULL),
                        IF(cep_responsavel_meta != '', CONCAT('- ', cep_responsavel_meta), NULL)
                    )
                ),
                ''
            )
        )
    ) AS endereco_responsavel,
        CONCAT('https://sejusc-pcd-ciptea-images.s3.sa-east-1.amazonaws.com/', foto_3x4) AS foto_3x4,
        CONCAT('https://sejusc-pcd-ciptea-images.s3.sa-east-1.amazonaws.com/', foto_digital) AS foto_digital, 
        CONCAT('id.sejusc.am.gov.br/', hashId) as url_qr_code, 
        CASE via_meta
                WHEN '1_via' THEN '1ª via'
                WHEN '2_via' THEN '2ª via'
                WHEN '1º' THEN '1ª via'
                WHEN '2º' THEN '2ª via'
                ELSE via_meta
        END AS via_meta, 
        email_meta
        FROM aprovados_ciptea 
        WHERE lote = %s
        ORDER BY updated_at DESC;
        '''
    
    get_solicitacoes_xlsx = '''
    SELECT 
    alert_id, 
    benef_cpf, 
    UPPER(benef_nome) AS benef_nome, 
    benef_rg, 
    UPPER(REPLACE(cid, '_', ' ')) AS cid_beneficiario,
    CASE 
    WHEN channelId = 12837 THEN 'intelectual' 
    ELSE tipo_da_deficiencia_meta 
     END AS deficiencia,
    UPPER(REPLACE(municipios_naturalidade_meta, '_', ' - ')) AS naturalidade_beneficiario, 
    UPPER(nome_da_mae) AS nome_da_mae, 
    UPPER(nome_do_pai) AS nome_do_pai, 
    CASE fator_rh
        WHEN 'o_positivo' THEN 'O+'
        WHEN 'o_negativo' THEN 'O-'
        WHEN 'a_positivo' THEN 'A+'
        WHEN 'a_negativo' THEN 'A-'
        WHEN 'b_positivo' THEN 'B+'
        WHEN 'b_negativo' THEN 'B-'
        WHEN 'ab_positivo' THEN 'AB+'
        WHEN 'ab_negativo' THEN 'AB-'
        ELSE fator_rh
    END AS fator_rh, 
    FormatDate(benef_data_nasc) AS data_nascimento, 
    sexo_genero_beneficiario, 
    estado_civil_beneficiario, 
    nacionalidade_beneficiario, 
    orgao_expedidor_beneficiario, 
    UPPER(REPLACE(REGEXP_REPLACE(municipios_endereco_beneficiario_meta, '^[0-9]+_', ''), '_', ' ')) AS municipios_endereco_beneficiario_meta, 
    CASE tipo_carteira
        WHEN '1_via' THEN '1ª via'
        WHEN '2_via' THEN '2ª via'
        WHEN '1º' THEN '1ª via'
        WHEN '2º' THEN '2ª via'
        ELSE tipo_carteira
    END AS tipo_carteira,
    descricao_motivo_2via,
    UPPER(REPLACE(REGEXP_REPLACE(local_de_retirada_meta, '^[0-9]+_', ''), '_', ' ')) AS local_de_retirada_meta,
    UPPER(
        COALESCE(
            TRIM(CONCAT_WS(' ',
                IF(avenidade_rua_beneficiario != '', avenidade_rua_beneficiario, NULL),
                IF(numero_beneficiario != '', numero_beneficiario, NULL),
                IF(bairro_beneficiario != '', 
                    CONCAT(', ', 
                        CASE bairro_beneficiario
                            WHEN 'adrianopolis' THEN 'Adrianópolis'
                            WHEN 'aleixo' THEN 'Aleixo'
                            WHEN 'alvorada' THEN 'Alvorada'
                            WHEN 'armando_mendes' THEN 'Armando Mendes'
                            WHEN 'betania' THEN 'Betânia'
                            WHEN 'cachoeirinha' THEN 'Cachoeirinha'
                            WHEN 'centro' THEN 'Centro'
                            WHEN 'chapada' THEN 'Chapada'
                            WHEN 'cidade_de_deus' THEN 'Cidade de Deus'
                            WHEN 'cidade_nova' THEN 'Cidade Nova'
                            WHEN 'colonia_antonio_aleixo' THEN 'Colônia Antônio Aleixo'
                            WHEN 'colonia_oliveira_machado' THEN 'Colônia Oliveira Machado'
                            WHEN 'colonia_santo_antonio' THEN 'Colônia Santo Antônio'
                            WHEN 'colonia_terra_nova' THEN 'Colônia Terra Nova'
                            WHEN 'compensa' THEN 'Compensa'
                            WHEN 'coroado' THEN 'Coroado'
                            WHEN 'crespo' THEN 'Crespo'
                            WHEN 'da_paz' THEN 'Da Paz'
                            WHEN 'distrito_industrial_i' THEN 'Distrito Industrial I'
                            WHEN 'distrito_industrial_ii' THEN 'Distrito Industrial II'
                            WHEN 'dom_pedro' THEN 'Dom Pedro'
                            WHEN 'educandos' THEN 'Educandos'
                            WHEN 'flores' THEN 'Flores'
                            WHEN 'gilberto_mestrinho' THEN 'Gilberto Mestrinho'
                            WHEN 'gloria' THEN 'Glória'
                            WHEN 'japiim' THEN 'Japiim'
                            WHEN 'jorge_teixeira' THEN 'Jorge Teixeira'
                            WHEN 'lago_azul' THEN 'Lago Azul'
                            WHEN 'lirio_do_vale' THEN 'Lírio do Vale'
                            WHEN 'mauazinho' THEN 'Mauazinho'
                            WHEN 'monte_das_oliveiras' THEN 'Monte das Oliveiras'
                            WHEN 'morro_da_liberdade' THEN 'Morro da Liberdade'
                            WHEN 'nossa_senhora_aparecida' THEN 'Nossa Senhora Aparecida'
                            WHEN 'nossa_senhora_das_gracas' THEN 'Nossa Senhora das Graças'
                            WHEN 'nova_cidade' THEN 'Nova Cidade'
                            WHEN 'nova_esperanca' THEN 'Nova Esperança'
                            WHEN 'novo_aleixo' THEN 'Novo Aleixo'
                            WHEN 'novo_israel' THEN 'Novo Israel'
                            WHEN 'parque_10_denovembro' THEN 'Parque 10 de Novembro'
                            WHEN 'petropolis' THEN 'Petrópolis'
                            WHEN 'planalto' THEN 'Planalto'
                            WHEN 'ponta_negra' THEN 'Ponta Negra'
                            WHEN 'praca_14_de_janeiro' THEN 'Praça 14 de Janeiro'
                            WHEN 'prediente_vargas' THEN 'Presidente Vargas'
                            WHEN 'puraquequara' THEN 'Puraquequara'
                            WHEN 'raiz' THEN 'Raiz'
                            WHEN 'redencao' THEN 'Redenção'
                            WHEN 'santa_etelvina' THEN 'Santa Etelvina'
                            WHEN 'santa_luizia' THEN 'Santa Luzia'
                            WHEN 'santo_agostinho' THEN 'Santo Agostinho'
                            WHEN 'santo_antonio' THEN 'Santo Antônio'
                            WHEN 'sao_francisco' THEN 'São Francisco'
                            WHEN 'sao_geraldo' THEN 'São Geraldo'
                            WHEN 'sao_jorge' THEN 'São Jorge'
                            WHEN 'sao_jose_operario' THEN 'São José Operário'
                            WHEN 'sao_lazaro' THEN 'São Lazaro'
                            WHEN 'sao_raimundo' THEN 'São Raimundo'
                            WHEN 'tancredo_neves' THEN 'Tancredo Neves'
                            WHEN 'taruma' THEN 'Tarumã'
                            WHEN 'taruma_acu' THEN 'Tarumã-Açu'
                            WHEN 'vila_buriti' THEN 'Vila Buriti'
                            WHEN 'vila_da_prata' THEN 'Vila da Prata'
                            WHEN 'zumbi_dos_palmares' THEN 'Zumbi dos Palmares'
                            WHEN 'santa_ines' THEN 'Santa Inês'
                            WHEN 'joao_paulo' THEN 'João Paulo'
                            ELSE bairro_beneficiario
                        END
                    ), 
                NULL),
                IF(cep_beneficiario != '', CONCAT('- ', cep_beneficiario), NULL)
            )), ''
        )
    ) AS endereco_beneficiario,
    nome_do_responsavel_legal_beneficiario, 
    cpf_responsavel, 
    resp_rg, 
    resp_email, 
    UPPER(
        TRIM(
            COALESCE(
                IF(
                    (rua_avenida_responsavel IS NULL OR rua_avenida_responsavel = '') AND
                    (bairro_responsavel IS NULL OR bairro_responsavel = '') AND
                    (cep_responsavel IS NULL OR cep_responsavel = ''),
                    UPPER(
                        COALESCE(
                            TRIM(CONCAT_WS(' ',
                                IF(avenidade_rua_beneficiario != '', avenidade_rua_beneficiario, NULL),
                                IF(numero_beneficiario != '', numero_beneficiario, NULL),
                                IF(bairro_beneficiario != '', 
                                    CONCAT(', ', 
                                        CASE bairro_beneficiario
                                            WHEN 'adrianopolis' THEN 'Adrianópolis'
                                            WHEN 'aleixo' THEN 'Aleixo'
                                            WHEN 'alvorada' THEN 'Alvorada'
                                            WHEN 'armando_mendes' THEN 'Armando Mendes'
                                            WHEN 'betania' THEN 'Betânia'
                                            WHEN 'cachoeirinha' THEN 'Cachoeirinha'
                                            WHEN 'centro' THEN 'Centro'
                                            WHEN 'chapada' THEN 'Chapada'
                                            WHEN 'cidade_de_deus' THEN 'Cidade de Deus'
                                            WHEN 'cidade_nova' THEN 'Cidade Nova'
                                            WHEN 'colonia_antonio_aleixo' THEN 'Colônia Antônio Aleixo'
                                            WHEN 'colonia_oliveira_machado' THEN 'Colônia Oliveira Machado'
                                            WHEN 'colonia_santo_antonio' THEN 'Colônia Santo Antônio'
                                            WHEN 'colonia_terra_nova' THEN 'Colônia Terra Nova'
                                            WHEN 'compensa' THEN 'Compensa'
                                            WHEN 'coroado' THEN 'Coroado'
                                            WHEN 'crespo' THEN 'Crespo'
                                            WHEN 'da_paz' THEN 'Da Paz'
                                            WHEN 'distrito_industrial_i' THEN 'Distrito Industrial I'
                                            WHEN 'distrito_industrial_ii' THEN 'Distrito Industrial II'
                                            WHEN 'dom_pedro' THEN 'Dom Pedro'
                                            WHEN 'educandos' THEN 'Educandos'
                                            WHEN 'flores' THEN 'Flores'
                                            WHEN 'gilberto_mestrinho' THEN 'Gilberto Mestrinho'
                                            WHEN 'gloria' THEN 'Glória'
                                            WHEN 'japiim' THEN 'Japiim'
                                            WHEN 'jorge_teixeira' THEN 'Jorge Teixeira'
                                            WHEN 'lago_azul' THEN 'Lago Azul'
                                            WHEN 'lirio_do_vale' THEN 'Lírio do Vale'
                                            WHEN 'mauazinho' THEN 'Mauazinho'
                                            WHEN 'monte_das_oliveiras' THEN 'Monte das Oliveiras'
                                            WHEN 'morro_da_liberdade' THEN 'Morro da Liberdade'
                                            WHEN 'nossa_senhora_aparecida' THEN 'Nossa Senhora Aparecida'
                                            WHEN 'nossa_senhora_das_gracas' THEN 'Nossa Senhora das Graças'
                                            WHEN 'nova_cidade' THEN 'Nova Cidade'
                                            WHEN 'nova_esperanca' THEN 'Nova Esperança'
                                            WHEN 'novo_aleixo' THEN 'Novo Aleixo'
                                            WHEN 'novo_israel' THEN 'Novo Israel'
                                            WHEN 'parque_10_denovembro' THEN 'Parque 10 de Novembro'
                                            WHEN 'petropolis' THEN 'Petrópolis'
                                            WHEN 'planalto' THEN 'Planalto'
                                            WHEN 'ponta_negra' THEN 'Ponta Negra'
                                            WHEN 'praca_14_de_janeiro' THEN 'Praça 14 de Janeiro'
                                            WHEN 'prediente_vargas' THEN 'Presidente Vargas'
                                            WHEN 'puraquequara' THEN 'Puraquequara'
                                            WHEN 'raiz' THEN 'Raiz'
                                            WHEN 'redencao' THEN 'Redenção'
                                            WHEN 'santa_etelvina' THEN 'Santa Etelvina'
                                            WHEN 'santa_luizia' THEN 'Santa Luzia'
                                            WHEN 'santo_agostinho' THEN 'Santo Agostinho'
                                            WHEN 'santo_antonio' THEN 'Santo Antônio'
                                            WHEN 'sao_francisco' THEN 'São Francisco'
                                            WHEN 'sao_geraldo' THEN 'São Geraldo'
                                            WHEN 'sao_jorge' THEN 'São Jorge'
                                            WHEN 'sao_jose_operario' THEN 'São José Operário'
                                            WHEN 'sao_lazaro' THEN 'São Lazaro'
                                            WHEN 'sao_raimundo' THEN 'São Raimundo'
                                            WHEN 'tancredo_neves' THEN 'Tancredo Neves'
                                            WHEN 'taruma' THEN 'Tarumã'
                                            WHEN 'taruma_acu' THEN 'Tarumã-Açu'
                                            WHEN 'vila_buriti' THEN 'Vila Buriti'
                                            WHEN 'vila_da_prata' THEN 'Vila da Prata'
                                            WHEN 'zumbi_dos_palmares' THEN 'Zumbi dos Palmares'
                                            WHEN 'santa_ines' THEN 'Santa Inês'
                                            WHEN 'joao_paulo' THEN 'João Paulo'
                                            ELSE bairro_beneficiario
                                        END
                                    ), 
                                NULL),
                                IF(cep_beneficiario != '', CONCAT('- ', cep_beneficiario), NULL)
                            )), ''
                        )
                    ),
                    CONCAT_WS(' ',
                        IF(rua_avenida_responsavel != '', rua_avenida_responsavel, NULL),
                        IF(bairro_responsavel != '', 
                            CONCAT(', ', 
                                CASE bairro_responsavel
                                    WHEN 'adrianopolis' THEN 'Adrianópolis'
                                    WHEN 'aleixo' THEN 'Aleixo'
                                    WHEN 'alvorada' THEN 'Alvorada'
                                    WHEN 'armando_mendes' THEN 'Armando Mendes'
                                    WHEN 'betania' THEN 'Betânia'
                                    WHEN 'cachoeirinha' THEN 'Cachoeirinha'
                                    WHEN 'centro' THEN 'Centro'
                                    WHEN 'chapada' THEN 'Chapada'
                                    WHEN 'cidade_de_deus' THEN 'Cidade de Deus'
                                    WHEN 'cidade_nova' THEN 'Cidade Nova'
                                    WHEN 'colonia_antonio_aleixo' THEN 'Colônia Antônio Aleixo'
                                    WHEN 'colonia_oliveira_machado' THEN 'Colônia Oliveira Machado'
                                    WHEN 'colonia_santo_antonio' THEN 'Colônia Santo Antônio'
                                    WHEN 'colonia_terra_nova' THEN 'Colônia Terra Nova'
                                    WHEN 'compensa' THEN 'Compensa'
                                    WHEN 'coroado' THEN 'Coroado'
                                    WHEN 'crespo' THEN 'Crespo'
                                    WHEN 'da_paz' THEN 'Da Paz'
                                    WHEN 'distrito_industrial_i' THEN 'Distrito Industrial I'
                                    WHEN 'distrito_industrial_ii' THEN 'Distrito Industrial II'
                                    WHEN 'dom_pedro' THEN 'Dom Pedro'
                                    WHEN 'educandos' THEN 'Educandos'
                                    WHEN 'flores' THEN 'Flores'
                                    WHEN 'gilberto_mestrinho' THEN 'Gilberto Mestrinho'
                                    WHEN 'gloria' THEN 'Glória'
                                    WHEN 'japiim' THEN 'Japiim'
                                    WHEN 'jorge_teixeira' THEN 'Jorge Teixeira'
                                    WHEN 'lago_azul' THEN 'Lago Azul'
                                    WHEN 'lirio_do_vale' THEN 'Lírio do Vale'
                                    WHEN 'mauazinho' THEN 'Mauazinho'
                                    WHEN 'monte_das_oliveiras' THEN 'Monte das Oliveiras'
                                    WHEN 'morro_da_liberdade' THEN 'Morro da Liberdade'
                                    WHEN 'nossa_senhora_aparecida' THEN 'Nossa Senhora Aparecida'
                                    WHEN 'nossa_senhora_das_gracas' THEN 'Nossa Senhora das Graças'
                                    WHEN 'nova_cidade' THEN 'Nova Cidade'
                                    WHEN 'nova_esperanca' THEN 'Nova Esperança'
                                    WHEN 'novo_aleixo' THEN 'Novo Aleixo'
                                    WHEN 'novo_israel' THEN 'Novo Israel'
                                    WHEN 'parque_10_denovembro' THEN 'Parque 10 de Novembro'
                                    WHEN 'petropolis' THEN 'Petrópolis'
                                    WHEN 'planalto' THEN 'Planalto'
                                    WHEN 'ponta_negra' THEN 'Ponta Negra'
                                    WHEN 'praca_14_de_janeiro' THEN 'Praça 14 de Janeiro'
                                    WHEN 'prediente_vargas' THEN 'Presidente Vargas'
                                    WHEN 'puraquequara' THEN 'Puraquequara'
                                    WHEN 'raiz' THEN 'Raiz'
                                    WHEN 'redencao' THEN 'Redenção'
                                    WHEN 'santa_etelvina' THEN 'Santa Etelvina'
                                    WHEN 'santa_luizia' THEN 'Santa Luzia'
                                    WHEN 'santo_agostinho' THEN 'Santo Agostinho'
                                    WHEN 'santo_antonio' THEN 'Santo Antônio'
                                    WHEN 'sao_francisco' THEN 'São Francisco'
                                    WHEN 'sao_geraldo' THEN 'São Geraldo'
                                    WHEN 'sao_jorge' THEN 'São Jorge'
                                    WHEN 'sao_jose_operario' THEN 'São José Operário'
                                    WHEN 'sao_lazaro' THEN 'São Lazaro'
                                    WHEN 'sao_raimundo' THEN 'São Raimundo'
                                    WHEN 'tancredo_neves' THEN 'Tancredo Neves'
                                    WHEN 'taruma' THEN 'Tarumã'
                                    WHEN 'taruma_acu' THEN 'Tarumã-Açu'
                                    WHEN 'vila_buriti' THEN 'Vila Buriti'
                                    WHEN 'vila_da_prata' THEN 'Vila da Prata'
                                    WHEN 'zumbi_dos_palmares' THEN 'Zumbi dos Palmares'
                                    WHEN 'santa_ines' THEN 'Santa Inês'
                                    WHEN 'joao_paulo' THEN 'João Paulo'
                                    ELSE bairro_responsavel
                                END
                            ), 
                        NULL),
                        IF(cep_responsavel != '', CONCAT('- ', cep_responsavel), NULL)
                    )
                ),
                ''
            )
        )
    ) AS endereco_responsavel,
    CASE 
        WHEN statusId = 1 THEN 'Pericía Médica'
        WHEN statusId = 2 THEN 'Registrado'
        WHEN statusId = 3 THEN 'Aprovado'
        WHEN statusId = 4 THEN 'Fechado'
        WHEN statusId = 5 THEN 'Biometria'
        WHEN statusId = 6 THEN 'Reprovado'
        WHEN statusId = 7 THEN 'Emitidas SEPCD'
        WHEN statusId = 8 THEN '2º Via'
        WHEN statusId = 9 THEN 'Aguardando Impressão SEPCD'
        WHEN statusId = 10 THEN 'Entregue'
        WHEN statusId = 11 THEN 'Retificação'
        WHEN statusId = 13 THEN 'Aprovado PAC'
        WHEN statusId = 17 THEN 'Entregue PAC'
        WHEN statusId = 18 THEN 'Emitidas Interior'
        WHEN statusId = 19 THEN 'Entregue Interior'
        WHEN statusId = 20 THEN 'Aprovado Interior'
        WHEN statusId = 21 THEN 'Pendente'
        WHEN statusId = 22 THEN 'Aguardando Envio'
        WHEN statusId = 23 THEN 'Enviado Impressão'
        WHEN statusId = 24 THEN 'Pronto para Retirada'
        WHEN statusId = 25 THEN 'Cancelado'
        WHEN statusId = 26 THEN 'Pré Aprovado'
        WHEN statusId = 27 THEN 'Encaminhado para Gráfica'
        WHEN statusId = 28 THEN 'Revisão de Carteira'
        WHEN statusId = 29 THEN 'Emitidas PAC'
        WHEN statusId = 30 THEN 'Aprovado Temporário'
        WHEN statusId = 31 THEN 'Edição de Carteira'
        ELSE 'Arquivado Perícia'
    END AS status,
        CASE 
        WHEN channelId = 12837 THEN 'CIPTEA' 
        WHEN channelId = 12836 THEN 'PCD' 
    END AS Canal,
    FormatDate(created_at),
    FormatDate(updated_at)
    FROM solicitacoes
    WHERE 1=1 {conditions}
    ORDER BY created_at DESC;
    '''

    get_valida_carteira = '''
        SELECT 
        UPPER(numero_carteira) AS numero_carteira, 
        UPPER(nome) AS nome, 
        UPPER(cpf) AS cpf, 
        UPPER(rg_beneficiario_meta) AS rg_beneficiario_meta, 
        UPPER(REPLACE(cid_beneficiario_meta, '_', ' ')) AS cid_beneficiario_meta,
        UPPER(data_de_nascimento) AS data_de_nascimento, 
        UPPER(telefone_beneficiario_meta) AS telefone_beneficiario_meta, 
        CASE tipo_sanguineo_beneficiario_meta
        WHEN 'o_positivo' THEN 'O+'
        WHEN 'o_negativo' THEN 'O-'
        WHEN 'a_positivo' THEN 'A+'
        WHEN 'a_negativo' THEN 'A-'
        WHEN 'b_positivo' THEN 'B+'
        WHEN 'b_negativo' THEN 'B-'
        WHEN 'ab_positivo' THEN 'AB+'
        WHEN 'ab_negativo' THEN 'AB-'
        ELSE tipo_sanguineo_beneficiario_meta
        END AS tipo_sanguineo_beneficiario_meta, 
        UPPER(REPLACE(naturalidade_beneficiario_meta, '_', ' ')) AS naturalidade_beneficiario_meta, 
        DATE(expedicao) AS expedicao, 
        DATE(vencimento) AS vencimento, 
        UPPER(
        COALESCE(
            TRIM(CONCAT_WS(' ',
                IF(avenida_rua_beneficiario_meta != '', avenida_rua_beneficiario_meta, NULL),
                IF(numero_beneficiario_meta != '', numero_beneficiario_meta, NULL),
                IF(bairro_beneficiario_meta != '', CONCAT(', ', bairro_beneficiario_meta), NULL),
                IF(cep_beneficiario_meta != '', CONCAT('- ', cep_beneficiario_meta), NULL)
            )), ''
        )
        ) AS endereco_beneficiario, 
        UPPER(nome_da_mae_meta) AS nome_da_mae_meta, 
        UPPER(nome_do_pai_meta) AS nome_do_pai_meta, 
        UPPER(nome_responsavel_legal_do_beneficiario_meta) AS nome_responsavel_legal_do_beneficiario_meta, 
        UPPER(rg_responsavel_meta) AS rg_responsavel_meta, 
        UPPER(telefone_responsavel_meta) AS telefone_responsavel_meta, 
        UPPER(
                COALESCE(
            TRIM(CONCAT_WS(' ',
                IF(rua_avenida_responsavel_meta != '', rua_avenida_responsavel_meta, NULL),
                IF(bairro_responsavel_meta != '', CONCAT(', ', bairro_responsavel_meta), NULL),
                IF(cep_responsavel_meta != '', CONCAT('- ', cep_responsavel_meta), NULL)
            )), ''
        )
        ) AS endereco_responsavel, 
        CONCAT('https://sejusc-pcd-ciptea-images.s3.sa-east-1.amazonaws.com/', foto_3x4) AS foto_3x4,
        CONCAT('https://sejusc-pcd-ciptea-images.s3.sa-east-1.amazonaws.com/', foto_digital) AS foto_digital, 
        CONCAT('id.sejusc.am.gov.br/', hashId) as url_qr_code, 
        CASE via_meta
                WHEN '1_via' THEN '1ªvia'
                WHEN '2_via' THEN '2ªvia'
                WHEN '1º' THEN '1ªvia'
                WHEN '2º' THEN '2ªvia'
                ELSE via_meta
        END AS via_meta, 
        email_meta
        FROM aprovados_ciptea 
        WHERE hashId = %s AND statusId IN(10, 18, 7, 17, 24, 30, 20, 29, 19)
        ORDER BY created_at DESC LIMIT 1;
        '''

    get_carteira_virtual = '''
                select id, alert_id, numero_carteira, nome, cpf,
                foto_3x4, foto_digital, hashId,
                vencimento, expedicao, lote, auditor, statusId, meta, created_at, updated_at
                from {projeto} where {conditions}
            '''

    updates_aprovados = '''
            update {projeto} set {conditions}
            where alert_id in (%s);
    '''

    update_solicitacoes = '''
            update solicitacoes set {conditions} where alert_id = %s;
    '''

    update_solicitacoes_teste = '''
            update solicitacoes set statusId = %s, auditor = %s {conditions} where alert_id = %s;
        '''

    insert_historico = '''
            insert into historico (
                       alert_id,
                       nome,
                       cpf,
                       carteira,
                       meta,
                       modified,
                       auditor,
                       statusId,
                       comentario
                       )
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''

    insert_aprovados_pcd = '''
            insert into aprovados_pcd(
                        alert_id,
                        numero_carteira,
                        nome,
                        cpf,
                        hashId,
                        auditor,
                        statusId,
                        meta
                        )
            values (%s, %s, %s, %s, %s, %s, %s, %s)
    '''

    insert_aprovados_ciptea = '''
            insert into aprovados_ciptea(
                        alert_id,
                        numero_carteira,
                        nome,
                        cpf,
                        hashId,
                        auditor,
                        statusId,
                        meta
                        )
            values (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
    
    insert_num_carteira_ciptea = '''
            insert into tb_num_ciptea(cpf, alert_id, via) values (%s, %s, %s)
    '''

    insert_num_carteira_pcd = '''
            insert into tb_num_pcd(cpf, alert_id, via) values (%s, %s, %s)
    '''

    insert_num_carteira_2_via_ciptea = '''
            call sp_cria_via(%s, %s)
        '''
    
    insert_num_carteira_2_via_pcd = '''
            call sp_cria_via_pcd(%s, %s)
        '''

    count_by_project = '''
            select projeto, count(*) as total from dashboard group by projeto
        '''

    count_by_municipio = '''
            select cad_municipio, count(*) as total from dashboard group by cad_municipio
        '''

    get_last_solicitations = '''
            select alert_id,benef_nome, cid, fator_rh, channelId, created_at
                from solicitacoes
            order by created_at desc limit %s
        '''
    get_historico_by_cpf = '''
        select h.alert_id, h.statusId, s.channelId, s.tipo_carteira, h.created_at, h.auditor, 
        CASE WHEN h.statusId = 6 THEN s.motivo_reprovado ELSE NULL END as motivo_reprovado, 
        h.comentario
        from historico h join solicitacoes s on h.alert_id = s.alert_id 
        where h.cpf = %s order by h.created_at desc;
        '''
    get_alert_events_by_cpf = '''
    select a.alert_id, s.channelId, a.status_meta, a.comment_meta, a.name_author, a.createdAt 
    from alert_events a join solicitacoes s on s.alert_id = a.alert_id
    where s.benef_cpf = %s and notification_meta is null order by a.createdAt desc;
    '''

    get_solicitation_by_hashId = '''
        select alert_id ,benef_cpf ,benef_nome ,benef_rg ,benef_data_nasc ,cid ,fator_rh ,resp_nome ,resp_rg ,benef_telefone, resp_telefone, meta, 
        UPPER(REPLACE(REGEXP_REPLACE(local_de_retirada_meta, '^[0-9]+_', ''), '_', ' ')) AS local_de_retirada_meta, 
        UPPER(REPLACE(municipios_naturalidade_meta, '_', ' ')) AS municipios_naturalidade_meta, 
        tipo_da_deficiencia_meta, external_id, created_at, tipo_carteira, statusId, channelId, attachments, resp_email, 
        meta ->> '$.sexo_genero_beneficiario' as sexo_beneficiario
        from solicitacoes s
        where hashId = %s
        order by created_at desc
        '''
    get_historico_by_alert_id = '''
        select alert_id, nome, cpf, carteira, maioridade_meta, nome_da_mae_meta, nome_do_pai_meta, 
        bairro_beneficiario_meta, tipo_carteira_meta, rg_responsavel_meta, cep_responsavel_meta, cpf_responsavel_meta,
        rg_beneficiario_meta, cep_beneficiario_meta, cid_beneficiario_meta, 
        UPPER(REPLACE(municipios_naturalidade_meta, '_', ' ')) AS municipios_naturalidade_meta, 
        cid2_beneficiario_meta, 
        UPPER(REPLACE(REGEXP_REPLACE(local_de_retirada_meta, '^[0-9]+_', ''), '_', ' ')) AS local_de_retirada_meta, 
        bairro_responsavel_meta, numero_responsavel_meta, 
        para_quem_cadastro_meta, numero_beneficiario_meta, motivo_2_via_meta, nome_do_beneficiario_meta,
        UPPER(REPLACE(municipio_responsavel_meta, '_', ' ')) AS municipio_responsavel_meta, 
        endereco_do_responsavel_meta, 
        UPPER(REPLACE(municipios_beneficiario_meta, '_', ' ')) AS municipios_beneficiario_meta, 
        rua_avenida_responsavel_meta, telefone_1_beneficiario_meta, telefone_2_beneficiario_meta, 
        avenida_rua_beneficiario_meta, sexo_genero_beneficiario_meta, estado_civil_beneficiario_meta, 
        naturalidade_beneficiario_meta, nacionalidade_beneficiario_meta, tipo_sanguineo_beneficiario_meta, 
        UPPER(REPLACE(municipio_realizado_cadastro_meta, '_', ' ')) AS municipio_realizado_cadastro_meta, 
        orgao_expedidor_beneficiario_meta, data_de_nascimento_beneficiario_meta, 
        tipo_da_deficiencia_beneficiario_meta, nome_responsavel_legal_do_beneficiario_meta, 
        responsavel_legal_do_beneficiario_meta, responsavel_legal_do_beneficiario_menor_meta, statusId, created_at 
        from historico 
        where alert_id = %s order by created_at limit 1
        '''
    
    get_historico_modified_by_alert_id = '''
        select cid_modified, resp_rg_modified, benef_rg_modified, nome_mae_modified, nome_pai_modified, resp_cep_modified, resp_cpf_modified, benef_cep_modified, benef_cpf_modified, resp_nome_modified, benef_nome_modified, resp_bairro_modified, resp_numero_modified, benef_bairro_modified, benef_numero_modified, naturalidade_modified, resp_municipio_modified, tipo_sanguineo_modified, benef_municipio_modified, data_nascimento_modified, resp_logradouro_modified, benef_logradouro_modified, resp_endereco_completo_modified, benef_endereco_completo_modified 
        from pcd.historico 
        where alert_id = %s order by created_at desc limit 1;
        '''
    
    get_solicitation_by_alert_id = '''
        select alert_id, benef_cpf, benef_nome, attachments
        from solicitacoes
        where alert_id = %s;
        '''
    get_solicitation_meta_by_alert_id = '''
        select meta from solicitacoes where alert_id = %s;
        '''
    get_solicitation_old_by_cpf = '''
    select s.alert_id, s.benef_cpf, s.benef_nome, s.created_at, s.updated_at, a.status, a.meta, a.channel
    from solicitacoes_old s join alerts a on s.alert_id = a.sasiAPIId 
    where s.benef_cpf = %s order by created_at desc;    
    '''

    get_informations_carteirinha_pcd = '''
    select numero_carteira, UPPER(nome) as nome, foto_3x4, UPPER(REPLACE(bairro_beneficiario_meta, '_', ' ')) as bairro_beneficiario_meta, 
    numero_beneficiario_meta, UPPER(avenida_rua_beneficiario_meta) as avenida_rua_beneficiario_meta, 
    cpf, expedicao, UPPER(cid_beneficiario_meta) as cid_beneficiario_meta, vencimento, tipo_da_deficiencia_meta,
    CASE tipo_sanguineo_beneficiario_meta
    WHEN 'o_positivo' THEN 'O+'
    WHEN 'o_negativo' THEN 'O-'
    WHEN 'a_positivo' THEN 'A+'
    WHEN 'a_negativo' THEN 'A-'
    WHEN 'b_positivo' THEN 'B+'
    WHEN 'b_negativo' THEN 'B-'
    WHEN 'ab_positivo' THEN 'AB+'
    WHEN 'ab_negativo' THEN 'AB-'
    ELSE tipo_sanguineo_beneficiario_meta
    END AS tipo_sanguineo_beneficiario_meta, 
    rg_beneficiario_meta, telefone_beneficiario_meta, 
    UPPER(responsavel_legal_do_beneficiario_meta), telefone_responsavel_meta, SHA1(alert_id) as hash_alert_id, alert_id
    from aprovados_pcd 
    where alert_id = %s;
    '''

    get_informations_carteirinha_ciptea = '''
    select numero_carteira, 
    UPPER(nome) as nome, 
    foto_3x4, foto_digital, UPPER(REPLACE(bairro_beneficiario_meta, '_', ' ')) as bairro_beneficiario_meta, 
    numero_beneficiario_meta, UPPER(avenida_rua_beneficiario_meta) as avenida_rua_beneficiario_meta, 
    cpf, expedicao, UPPER(cid_beneficiario_meta) as cid_beneficiario_meta, vencimento,
    CASE tipo_sanguineo_beneficiario_meta
    WHEN 'o_positivo' THEN 'O+'
    WHEN 'o_negativo' THEN 'O-'
    WHEN 'a_positivo' THEN 'A+'
    WHEN 'a_negativo' THEN 'A-'
    WHEN 'b_positivo' THEN 'B+'
    WHEN 'b_negativo' THEN 'B-'
    WHEN 'ab_positivo' THEN 'AB+'
    WHEN 'ab_negativo' THEN 'AB-'
    ELSE tipo_sanguineo_beneficiario_meta
    END AS tipo_sanguineo_beneficiario_meta, rg_beneficiario_meta, telefone_beneficiario_meta, 
    UPPER(responsavel_legal_do_beneficiario_meta), telefone_responsavel_meta, email_meta, SHA1(alert_id) as hash_alert_id, alert_id
    from aprovados_ciptea 
    where alert_id = %s;
    '''

    get_aproved_ciptea = '''
    SELECT 
    numero_carteira, 
    foto_3x4, 
    UPPER(nome) AS nome, 
    cpf, 
    rg_beneficiario_meta, 
    UPPER(REPLACE(cid_beneficiario_meta, '_', ' ')) AS cid_beneficiario, 
    data_de_nascimento, 
    telefone_beneficiario_meta, 
    CASE tipo_sanguineo_beneficiario_meta
    WHEN 'o_positivo' THEN 'O+'
    WHEN 'o_negativo' THEN 'O-'
    WHEN 'a_positivo' THEN 'A+'
    WHEN 'a_negativo' THEN 'A-'
    WHEN 'b_positivo' THEN 'B+'
    WHEN 'b_negativo' THEN 'B-'
    WHEN 'ab_positivo' THEN 'AB+'
    WHEN 'ab_negativo' THEN 'AB-'
    ELSE tipo_sanguineo_beneficiario_meta
    END AS tipo_sanguineo_beneficiario_meta, 
    UPPER(REPLACE(naturalidade_beneficiario_meta, '_', ' ')) AS naturalidade_beneficiario, 
    FormatDate(expedicao), 
    FormatDate(vencimento), 
    UPPER(
        COALESCE(
            TRIM(CONCAT_WS(' ',
                    IF(avenida_rua_beneficiario_meta != '', avenida_rua_beneficiario_meta, NULL),
                    IF(numero_beneficiario_meta != '', numero_beneficiario_meta, NULL),
                    IF(bairro_beneficiario_meta != '', CONCAT(', ', bairro_beneficiario_meta), NULL),
                    IF(cep_beneficiario_meta != '', CONCAT('- ', cep_beneficiario_meta), NULL)
                )), ''
            )
        ) AS endereco_beneficiario,  
        CONCAT(
        UPPER(nome_da_mae_meta),
        IF(nome_do_pai_meta != '', CONCAT(', ', UPPER(nome_do_pai_meta)), '')
    ) AS filiacao, 
        UPPER(nome_responsavel_legal_do_beneficiario_meta), 
        json_unquote(json_extract(meta,_utf8mb4'$.meta.cpf_responsavel')) as rg_responsavel_meta, 
        email_meta, 
        telefone_responsavel_meta, 
        COALESCE(
            TRIM(CONCAT_WS(' ',
                IF(rua_avenida_responsavel_meta != '', rua_avenida_responsavel_meta, NULL),
                IF(bairro_responsavel_meta != '', CONCAT(', ', bairro_responsavel_meta), NULL),
                IF(cep_responsavel_meta != '', CONCAT('- ', cep_responsavel_meta), NULL)
            )), ''
        ) AS endereco_responsavel, 
        foto_digital,
        CONCAT('id.sejusc.am.gov.br/', hashId) AS url_qr_code
    FROM aprovados_ciptea
    WHERE alert_id = %s ORDER BY created_at DESC LIMIT 1
    '''

    get_informations_recepcao = '''
    SELECT 
    benef_cpf, 
    hashId, 
    UPPER(benef_nome) AS nome, 
    alert_id, 
    tipo_da_deficiencia_meta, 
    UPPER(REPLACE(
        TRIM(BOTH ' ' FROM REGEXP_REPLACE(local_de_retirada_meta, '^[0-9]+[ ]+', '')), 
        '_', 
        ' '
    )) AS local_de_retirada, 
    UPPER(REPLACE(municipios_endereco_beneficiario_meta, '_', ' ')) AS municipios_endereco_beneficiario_meta, 
    UPPER(REPLACE(cid, '_', ' ')) AS cid, 
    CASE 
        WHEN channelId = 12837 THEN 'CIPTEA' 
        WHEN channelId = 12836 THEN 'PCD' 
    END AS carteirinha,
    CASE 
        WHEN statusId = 1 THEN 'Pericía Médica'
        WHEN statusId = 2 THEN 'Registrado'
        WHEN statusId = 3 THEN 'Aprovado'
        WHEN statusId = 4 THEN 'Fechado'
        WHEN statusId = 5 THEN 'Biometria'
        WHEN statusId = 6 THEN 'Reprovado'
        WHEN statusId = 7 THEN 'Emitidas SEPCD'
        WHEN statusId = 8 THEN '2º Via'
        WHEN statusId = 9 THEN 'Aguardando Impressão SEPCD'
        WHEN statusId = 10 THEN 'Entregue'
        WHEN statusId = 11 THEN 'Retificação'
        WHEN statusId = 13 THEN 'Aprovado PAC'
        WHEN statusId = 17 THEN 'Entregue PAC'
        WHEN statusId = 18 THEN 'Emitidas Interior'
        WHEN statusId = 19 THEN 'Entregue Interior'
        WHEN statusId = 20 THEN 'Aprovado Interior'
        WHEN statusId = 21 THEN 'Pendente'
        WHEN statusId = 22 THEN 'Aguardando Envio'
        WHEN statusId = 23 THEN 'Enviado Impressão'
        WHEN statusId = 24 THEN 'Pronto para Retirada'
        WHEN statusId = 25 THEN 'Cancelado'
        WHEN statusId = 26 THEN 'Pré Aprovado'
        WHEN statusId = 27 THEN 'Encaminhado para Gráfica'
        WHEN statusId = 28 THEN 'Revisão de Carteira'
        WHEN statusId = 29 THEN 'Emitidas PAC'
        WHEN statusId = 30 THEN 'Aprovado Temporário'
        ELSE 'Edição de Carteira'
    END AS status,
    created_at
    FROM solicitacoes
    WHERE 1=1 {conditions}
    ORDER BY created_at {order}
    LIMIT %s
    OFFSET %s;
    '''

    get_count_recepcao = '''
    select count(*) from solicitacoes where 1=1 {conditions}
    '''

    get_produtividade = '''
    SELECT
    UPPER(auditor) AS Auditor,
    GROUP_CONCAT(CONCAT(status_id, ':', IFNULL(Quantidade, 0)) ORDER BY status_id ASC SEPARATOR ',') AS 'Quantidade por Status',
    SUM(IFNULL(Quantidade, 0)) AS Total
    FROM (
        SELECT
            a.auditor,
            st.id AS status_id,
            IFNULL(COUNT(h.statusId), 0) AS Quantidade
        FROM
            (SELECT DISTINCT auditor FROM pcd.historico
            WHERE {conditions}) a
        CROSS JOIN pcd.status st
        LEFT JOIN (
            SELECT *
            FROM pcd.historico
            WHERE 1=1 {conditions_date}
        ) h 
        ON h.auditor = a.auditor 
        AND h.statusId = st.id
        GROUP BY
            a.auditor,
            st.id
    ) AS subquery
    GROUP BY
        auditor
    ORDER BY
        Auditor
    '''

    get_status_solicitacao = '''
        SELECT alert_id, benef_cpf, benef_nome, statusId, channelId, motivo_reprovado
        FROM solicitacoes
        WHERE {conditions} {conditions_channel_ids}
    '''

    get_visual_export = '''
        SELECT s.alert_id, benef_nome, channelId, statusId, municipios_endereco_beneficiario_meta, tipo_da_deficiencia_meta, updated_at from solicitacoes s 
        WHERE 1=1 {conditions}
        order by updated_at desc limit %s offset %s;
    '''

    get_count_visual_export = '''
        SELECT count(*) from solicitacoes s 
        WHERE 1=1 {conditions}
    '''