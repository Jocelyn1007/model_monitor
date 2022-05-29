from pyhive import hive
import pandas as pd
import numpy as np
from lib.properties.db_prop import bigdb
from lib.utility.writelog import log

logger = log()


def bigquery(sql):
    try:
        logger.info("开始查询数据库")
        conn = hive.Connection(**bigdb)
        # conn = hive.Connection(host='10.67.16.18', port=10000,
        #                        username='dm_credit', password='1edPNvhi8zqxCNJJ',
        #                        database='dm_credit', auth='LDAP')
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = cursor.description
        results = cursor.fetchall()
        data_dict = [dict(zip([col[0] for col in columns], row)) for row in results]
        cursor.close()
        conn.close()
        logger.info("数据获取完毕")
        return data_dict
    except Exception as e:
        logger.error("数据获取出错")
        logger.error(e)
# 获取psi原始数据
def query_psi_data():
    try:
        logger.info("开始查询数据库-psi")
        conn = hive.Connection(**bigdb)
        xslhp_overdue_m30_with_a_score_backup = pd.read_sql('''
        select 
        case when to_date(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')))>=to_date('2020-01-11') and to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))<=to_date('2020-04-21') then to_date(to_date('2020-04-21')) 
             when to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))>to_date('2020-04-21') and to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))<=date_sub(trunc(to_date(CURRENT_DATE),'MM'),1) then substr(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),1,7)
             when to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))>to_date('2020-04-21') and datediff(to_date(current_date()),trunc(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),'MM'))>7 and to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))<=date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),  day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 7 )    then concat(trunc(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),'MM'),'-',date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')), day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 7 ))
             when to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))>to_date('2020-04-21') and datediff(to_date(current_date()),trunc(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),'MM'))>14 and to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))<=date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),  day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 14 ) then concat(date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')), day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 8 ),'-',date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')), day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 14 ))
             when to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))>to_date('2020-04-21') and datediff(to_date(current_date()),trunc(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),'MM'))>21 and to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))<=date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),  day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 21 ) then concat(date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')), day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 15 ),'-',date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')), day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 21 ))
             when to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))>to_date('2020-04-21') and datediff(to_date(current_date()),trunc(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),'MM'))>28 and to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))<=date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),  day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 28 ) then concat(date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')), day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 22 ),'-',date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')), day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 28 ))
             when to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))>to_date('2020-04-21') and datediff(to_date(current_date()),trunc(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),'MM'))<=7  then concat(trunc(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),'MM'),'-',to_date(current_date()))
             when to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))>to_date('2020-04-21') and datediff(to_date(current_date()),trunc(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),'MM'))<=14 then concat(date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')), day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 8 ),'-',to_date(current_date()))
             when to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))>to_date('2020-04-21') and datediff(to_date(current_date()),trunc(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),'MM'))<=21 then concat(date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')), day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 15 ),'-',to_date(current_date()))
             when to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))>to_date('2020-04-21') and datediff(to_date(current_date()),trunc(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')),'MM'))<=28 then concat(date_sub(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')), day(to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))) + 22 ),'-',to_date(current_date()))
             else to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')) end as apply_month,
        a.applthst_apply_no as apply_no,
        trim(replace(SUBSTRING_INDEX(split(b.xslhp_adtrs_detail,'"user_type":')[1] ,',',1),'}','')) as user_type,
        case when trim(replace(SUBSTRING_INDEX(split(b.xslhp_adtrs_detail,'"user_type":')[1] ,',',1),'}',''))=4 and j.rsk_is_new_user=1 then 41
             when trim(replace(SUBSTRING_INDEX(split(b.xslhp_adtrs_detail,'"user_type":')[1] ,',',1),'}',''))=4 and j.rsk_is_new_user=2 then 42
             else trim(replace(SUBSTRING_INDEX(split(b.xslhp_adtrs_detail,'"user_type":')[1] ,',',1),'}','')) end as new_user_type,
        b.xslhp_adtrs_status,
        j.rsk_is_new_user,
        c.bh_rl_d360_creditlimitsum,
        d.br_als_m1_cell_nbank_nsloan_orgnum,
        d.br_als_m6_cell_max_inteday,
        d.br_als_m6_id_bank_ret_orgnum,
        e.dhbcse_bxf_scorea03,
        f.dhbs_creditv2,
        g.jg_risk_factors_app_v3_6_180,
        h.r360_af_riskscore,
        i.r360_br_feature04,
        k.r360_fs_score,
        l.r360_mla_feature_20,
        round((case when (c.bh_rl_d360_creditlimitsum <1800.0 or c.bh_rl_d360_creditlimitsum is null or c.bh_rl_d360_creditlimitsum in ('null')) then 53.72
                    when c.bh_rl_d360_creditlimitsum >=1800.0 then 73.07
                    else -999 end
            +
            case when (d.br_als_m1_cell_nbank_nsloan_orgnum is null or d.br_als_m1_cell_nbank_nsloan_orgnum in ('null')) then 52.7
                 when d.br_als_m1_cell_nbank_nsloan_orgnum <4.0 then 65.84
                 when d.br_als_m1_cell_nbank_nsloan_orgnum >=4.0 then 44.65
                 else -999 end
            +
            case when (d.br_als_m6_cell_max_inteday <30.0 or d.br_als_m6_cell_max_inteday is null or d.br_als_m6_cell_max_inteday in ('null')) then 67.7
                 when d.br_als_m6_cell_max_inteday>=30.0 then 48.33
                 else -999 end 
            +
            case when (d.br_als_m6_id_bank_ret_orgnum is null or d.br_als_m6_id_bank_ret_orgnum in ('null')) then 65.76
                 when d.br_als_m6_id_bank_ret_orgnum is not null then 47.11
                 else -999 end
            +
            case when (e.dhbcse_bxf_scorea03 is null or e.dhbcse_bxf_scorea03 in ('null')) then 60.45
                 when e.dhbcse_bxf_scorea03 <547.0 then 22.67
                 when e.dhbcse_bxf_scorea03 >=547.0 then 158.44
                 else -999 end 
            +
            case when (f.dhbs_creditv2 <2.0 or f.dhbs_creditv2 is null or f.dhbs_creditv2 in ('null')) then 30.52
                 when f.dhbs_creditv2>=2.0 then 62.21
                 else -999 end 
            +
            case when (g.jg_risk_factors_app_v3_6_180 is null or g.jg_risk_factors_app_v3_6_180 in ('null')) then 57.32
                 when g.jg_risk_factors_app_v3_6_180<3.0 then 42.46
                 when g.jg_risk_factors_app_v3_6_180>=3.0 then 66.37
                 else -999 end 
            +
            case when h.r360_af_riskscore <70 then 75.7
                 when (h.r360_af_riskscore>=70 or h.r360_af_riskscore is null or h.r360_af_riskscore in ('null')) then 46.09
                 else -999 end 
            +
            case when (i.r360_br_feature04 is null or i.r360_br_feature04 in ('null')) then 16.25
                 when i.r360_br_feature04 in ('A','B','C','D') then 56.14
                 when i.r360_br_feature04 in ('E') then 93.76
                 else -999 end 
            +
            case when k.r360_fs_score<604.0 then 46.07
                 when (k.r360_fs_score>=604.0 or k.r360_fs_score is null or k.r360_fs_score in ('null') )then 69.65
                 else -999 end 
            +
            case when (l.r360_mla_feature_20 <27.0 or l.r360_mla_feature_20 is null or l.r360_mla_feature_20 in ('null')) then 48.11
                 when l.r360_mla_feature_20>=27.0 then 73.99
                 else -999 end 
            ),0) as xslhp_overdue_m30_with_a_score_backup
            from dm_outrisk.applicant_history_v20171225_cld a 
            left join dm_outrisk.xslhp_audit_result_v20180628_cld b on a.applthst_id=b.fk_xslhp_adtrs_applthst_id
            left join dm_outrisk.risk_info_v20171225_cld j on a.applthst_id=j.fk_rsk_applthst_id
            left join dm_outrisk.baihang_rl_loan_v20190929_cld c on a.applthst_id=c.fk_bh_rl_apply_id
            left join dm_outrisk.bairong_als_v20180514_cld d on a.applthst_id=d.fk_br_als_apply_id
            left join dm_outrisk.dianhuabang_cuishou_express_v20191219_cld e on a.applthst_id=e.fk_dhbcse_apply_id
            left join dm_outrisk.dianhuabang_shield_v20191219_cld f on a.applthst_id=f.fk_dhbs_apply_id
            left join dm_outrisk.jg_risk_factors_v20190627_cld g on a.applthst_id=g.fk_jg_risk_factors_apply_id
            left join dm_outrisk.rong360_agent_antifraud_v20190918_cld h on a.applthst_id=h.fk_r360_af_apply_id
            left join dm_outrisk.rong360_budget_report_v20190918_cld i on a.applthst_id=i.fk_r360_br_apply_id
            left join dm_outrisk.rong360_fenqi_solution_v20190917_cld k on a.applthst_id=k.fk_r360_fs_apply_id
            left join dm_outrisk.rong360_multiloan_antifraud_v20190918_cld l on a.applthst_id=l.fk_r360_mla_apply_id
           where ((to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))>=to_date('2020-05-09'))
              or (to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))>=to_date('2020-01-11') 
             and to_date(from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss'))<=to_date('2020-04-21')))
             and a.applthst_product_no in ('PD0006')''', con=conn)
        # xslhp_overdue_m30_with_a_score_backup切分分数段
        xslhp_overdue_m30_with_a_score_backup_bins = [-np.inf, 491, 582, 597, 606, 615, 621, 627, 634, 638, 643, 648, 653,658, 664, 669, 678, 685, 694, 707, 728, 851, np.inf]
        xslhp_overdue_m30_with_a_score_backup['xslhp_overdue_m30_with_a_score_backup_bins'] = pd.cut(xslhp_overdue_m30_with_a_score_backup['xslhp_overdue_m30_with_a_score_backup'],bins=xslhp_overdue_m30_with_a_score_backup_bins)
        # 聚合评分段件数
        data_xslhp_overdue_m30_with_a_score_backup_bins = xslhp_overdue_m30_with_a_score_backup.pivot_table(index='xslhp_overdue_m30_with_a_score_backup_bins', columns=['new_user_type', 'apply_month'], values='apply_no',aggfunc=len, fill_value=0)
        data_xslhp_overdue_m30_with_a_score_backup_bins = data_xslhp_overdue_m30_with_a_score_backup_bins.div(data_xslhp_overdue_m30_with_a_score_backup_bins.sum(axis=0), axis=1)
        return data_xslhp_overdue_m30_with_a_score_backup_bins
    except Exception as e:
        logger.error("psi数据获取出错")
        logger.error(e)
# 获取ks原始数据
def query_ks_data():
    try:
        logger.info("开始查询数据库-ks")
        conn = hive.Connection(**bigdb)
        xslhp_overdue_m30_with_a_score_backup = pd.read_sql('''
                select 
                a.applthst_apply_no as apply_no,
                trim(replace(SUBSTRING_INDEX(split(b.xslhp_adtrs_detail,'"user_type":')[1] ,',',1),'}','')) as user_type,
                case when trim(replace(SUBSTRING_INDEX(split(b.xslhp_adtrs_detail,'"user_type":')[1] ,',',1),'}',''))=4 and j.rsk_is_new_user=1 then 41
                     when trim(replace(SUBSTRING_INDEX(split(b.xslhp_adtrs_detail,'"user_type":')[1] ,',',1),'}',''))=4 and j.rsk_is_new_user=2 then 42
                     else trim(replace(SUBSTRING_INDEX(split(b.xslhp_adtrs_detail,'"user_type":')[1] ,',',1),'}','')) end as new_user_type,
                b.xslhp_adtrs_status,
                j.rsk_is_new_user,
                c.bh_rl_d360_creditlimitsum,
                d.br_als_m1_cell_nbank_nsloan_orgnum,
                d.br_als_m6_cell_max_inteday,
                d.br_als_m6_id_bank_ret_orgnum,
                e.dhbcse_bxf_scorea03,
                f.dhbs_creditv2,
                g.jg_risk_factors_app_v3_6_180,
                h.r360_af_riskscore,
                i.r360_br_feature04,
                k.r360_fs_score,
                l.r360_mla_feature_20,
                round((case when (c.bh_rl_d360_creditlimitsum <1800.0 or c.bh_rl_d360_creditlimitsum is null or c.bh_rl_d360_creditlimitsum in ('null')) then 53.72
                            when c.bh_rl_d360_creditlimitsum >=1800.0 then 73.07
                            else -999 end
                +
                case when (d.br_als_m1_cell_nbank_nsloan_orgnum is null or d.br_als_m1_cell_nbank_nsloan_orgnum in ('null')) then 52.7
                     when d.br_als_m1_cell_nbank_nsloan_orgnum <4.0 then 65.84
                     when d.br_als_m1_cell_nbank_nsloan_orgnum >=4.0 then 44.65
                     else -999 end
                +
                case when (d.br_als_m6_cell_max_inteday <30.0 or d.br_als_m6_cell_max_inteday is null or d.br_als_m6_cell_max_inteday in ('null')) then 67.7
                     when d.br_als_m6_cell_max_inteday>=30.0 then 48.33
                     else -999 end 
                +
                case when (d.br_als_m6_id_bank_ret_orgnum is null or d.br_als_m6_id_bank_ret_orgnum in ('null')) then 65.76
                     when d.br_als_m6_id_bank_ret_orgnum is not null then 47.11
                     else -999 end
                +
                case when (e.dhbcse_bxf_scorea03 is null or e.dhbcse_bxf_scorea03 in ('null')) then 60.45
                     when e.dhbcse_bxf_scorea03 <547.0 then 22.67
                     when e.dhbcse_bxf_scorea03 >=547.0 then 158.44
                     else -999 end 
                +
                case when (f.dhbs_creditv2 <2.0 or f.dhbs_creditv2 is null or f.dhbs_creditv2 in ('null')) then 30.52
                     when f.dhbs_creditv2>=2.0 then 62.21
                     else -999 end 
                +
                case when (g.jg_risk_factors_app_v3_6_180 is null or g.jg_risk_factors_app_v3_6_180 in ('null')) then 57.32
                     when g.jg_risk_factors_app_v3_6_180<3.0 then 42.46
                     when g.jg_risk_factors_app_v3_6_180>=3.0 then 66.37
                     else -999 end 
                +
                case when h.r360_af_riskscore <70 then 75.7
                     when (h.r360_af_riskscore>=70 or h.r360_af_riskscore is null or h.r360_af_riskscore in ('null')) then 46.09
                     else -999 end 
                +
                case when (i.r360_br_feature04 is null or i.r360_br_feature04 in ('null')) then 16.25
                     when i.r360_br_feature04 in ('A','B','C','D') then 56.14
                     when i.r360_br_feature04 in ('E') then 93.76
                     else -999 end 
                +
                case when k.r360_fs_score<604.0 then 46.07
                     when (k.r360_fs_score>=604.0 or k.r360_fs_score is null or k.r360_fs_score in ('null') )then 69.65
                     else -999 end 
                +
                case when (l.r360_mla_feature_20 <27.0 or l.r360_mla_feature_20 is null or l.r360_mla_feature_20 in ('null')) then 48.11
                     when l.r360_mla_feature_20>=27.0 then 73.99
                     else -999 end 
                ),0) as xslhp_overdue_m30_with_a_score_backup
                from dm_outrisk.applicant_history_v20171225_cld a 
                left join dm_outrisk.xslhp_audit_result_v20180628_cld b on a.applthst_id=b.fk_xslhp_adtrs_applthst_id
                left join dm_outrisk.risk_info_v20171225_cld j on a.applthst_id=j.fk_rsk_applthst_id
                left join dm_outrisk.baihang_rl_loan_v20190929_cld c on a.applthst_id=c.fk_bh_rl_apply_id
                left join dm_outrisk.bairong_als_v20180514_cld d on a.applthst_id=d.fk_br_als_apply_id
                left join dm_outrisk.dianhuabang_cuishou_express_v20191219_cld e on a.applthst_id=e.fk_dhbcse_apply_id
                left join dm_outrisk.dianhuabang_shield_v20191219_cld f on a.applthst_id=f.fk_dhbs_apply_id
                left join dm_outrisk.jg_risk_factors_v20190627_cld g on a.applthst_id=g.fk_jg_risk_factors_apply_id
                left join dm_outrisk.rong360_agent_antifraud_v20190918_cld h on a.applthst_id=h.fk_r360_af_apply_id
                left join dm_outrisk.rong360_budget_report_v20190918_cld i on a.applthst_id=i.fk_r360_br_apply_id
                left join dm_outrisk.rong360_fenqi_solution_v20190917_cld k on a.applthst_id=k.fk_r360_fs_apply_id
                left join dm_outrisk.rong360_multiloan_antifraud_v20190918_cld l on a.applthst_id=l.fk_r360_mla_apply_id
                where from_unixtime(unix_timestamp(a.applthst_create_time)+28800,'yyyy-MM-dd HH:mm:ss')>=to_date('2020-03-01')
                      and a.applthst_product_no in ('PD0006')
                ''', con=conn)

        xslhp_overdue_m30_with_a_score_backup_target = pd.read_sql('''
        select
        b1.apply_no,
        a1.lend_time,
        a1.lend_month,
        a1.target
        from(
        select 
        loan_id,
        lend_time,
        lend_month,
        case when overdue_days>=30 then 1 else 0 end as target
        from (
        select
        loan_id,
        lend_time,
        lend_month,
        max(overdue_days) as overdue_days
        from (
        select 
        loan_id,
        date(lend_time) as lend_time,
        concat(year(lend_time),'-',month(lend_time)) as lend_month,
        overdue_days
        from dm_asset.dm_asset_ar_repay_info
        where lend_time is not null
              and to_date(lend_time)<=to_date(date_sub(from_unixtime(unix_timestamp()),90))
              and to_date(lend_time)>=to_date('2020-05-01')
              and product_id  in ('10010')
              and period<=2) a group by loan_id,lend_time,lend_month) b) a1 
        inner join dm_asset.dm_asset_ar_apply_info b1 
        on a1.loan_id=b1.loan_id ''', con=conn)
        xslhp_overdue_m30_with_a_score_backup_target.columns = [i.split('.', 1)[1] for i in xslhp_overdue_m30_with_a_score_backup_target.columns]
        xslhp_overdue_m30_with_a_score_backup = xslhp_overdue_m30_with_a_score_backup[['apply_no', 'xslhp_overdue_m30_with_a_score_backup', 'new_user_type']]
        xslhp_overdue_m30_with_a_score_backup_target = xslhp_overdue_m30_with_a_score_backup_target[['apply_no', 'lend_time', 'lend_month', 'target']]
        xslhp_overdue_m30_with_a_score_backup_ks = pd.merge(xslhp_overdue_m30_with_a_score_backup_target,xslhp_overdue_m30_with_a_score_backup, how='inner',on='apply_no')
        return xslhp_overdue_m30_with_a_score_backup_ks
    except Exception as e:
        logger.error("ks数据获取出错")
        logger.error(e)
if __name__ == '__main__':
    sql = '''select product_id
       ,count(apply_no) as total_no
       ,sum(case when loan_id <> 'null' and current_step <> '归档/超时取消' and current_step <> '放款处理中' then 1 else 0 end ) as pass_no
       ,round(sum(case when loan_id <> 'null' and current_step <> '归档/超时取消' and current_step <> '放款处理中' then approve_money else 0 end )/10000,2) as approve_amt_W
        from  dm_asset.dm_asset_ar_apply_info
        where apply_date = date_sub(FROM_UNIXTIME(UNIX_TIMESTAMP()),1)
        and product_id in (
        '10010',
        '10011',
        '10016',
        '10023',
        '10025',
        '10029',
        '10030')
        group by product_id, product_name'''
    results = bigquery(sql)
    for i in results:
        print(i)
