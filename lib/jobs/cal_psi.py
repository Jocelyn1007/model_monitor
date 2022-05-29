from lib.utility.big_db import query_psi_data
import pandas as pd
import numpy as np

#计算psi函数
def cal_psi_df():
    def unpack_tuple(x):
            if len(x) == 1:
                return x[0]
            else:
                return x

    def psi(no_base, base, return_frame=False):
        '''
        psi计算
        :param no_base: 非基准数据集
        :param base: 基准数据集
        :param return_frame: 是否返回详细的psi数据集
        :return:
        '''
        psi = list()
        frame = list()

        if isinstance(no_base, pd.DataFrame):
            for col in no_base:
                p, f = calc_psi(no_base[col], base[col])
                psi.append(p)
                frame.append(f)

            psi = pd.Series(psi, index=no_base.columns)

            frame = pd.concat(
                frame,
                keys=no_base.columns,
                names=['columns', 'id'],
            ).reset_index()
            frame = frame.drop(columns='id')
        else:
            psi, frame = calc_psi(no_base, base)

        res = (psi,)

        if return_frame:
            res += (frame,)

        return unpack_tuple(res)

    def calc_psi(base_prop, no_base_prop):
        '''
        psi计算的具体逻辑
        :param no_base: 非基准数据集
        :param base: 基准数据集
        :return:
        '''
        #no_base_prop = pd.Series(no_base).value_counts(normalize=True, dropna=False)
        #base_prop = pd.Series(base).value_counts(normalize=True, dropna=False)
        base_prop.replace({0:0.000000001}, inplace=True)
        no_base_prop.replace({0:0.000000001}, inplace=True)

        psi = np.sum((no_base_prop - base_prop) * np.log(no_base_prop / base_prop))

        frame = pd.DataFrame({
            'no_base': no_base_prop,
            'base': base_prop,
        })
        frame.index.name = 'value'

        return psi, frame.reset_index()
    #新用户&量化派新用户xslhp_overdue_m30_with_a_score_backup
    data_xslhp_overdue_m30_with_a_score_backup_bins=query_psi_data()
    data_xslhp_overdue_m30_with_a_score_backup_bins.columns = ['_'.join(col).strip() for col in data_xslhp_overdue_m30_with_a_score_backup_bins.columns.values]
    psi_data_new_cust_new_long_term_backup=pd.DataFrame()
    user_41_cols = [i for i in data_xslhp_overdue_m30_with_a_score_backup_bins.columns if i.startswith('41_')]
    user_41_df = data_xslhp_overdue_m30_with_a_score_backup_bins[user_41_cols]
    for i,value in enumerate(user_41_cols):
        psi, frame = calc_psi(user_41_df.iloc[:,0], user_41_df.iloc[:,i])
        del frame['base']
        frame=frame.rename(columns={'no_base':value})
        frame['psi']=round(psi,4)
        frame=frame[['psi']].drop_duplicates()
        frame=frame.rename(columns={'psi':value})
        psi_data_new_cust_new_long_term_backup=pd.concat([psi_data_new_cust_new_long_term_backup,frame],axis=1)

    psi_data_new_cust_new_long_term_backup=psi_data_new_cust_new_long_term_backup[psi_data_new_cust_new_long_term_backup.columns].T.drop_duplicates().T


    del psi_data_new_cust_new_long_term_backup['41_2020-04-21']
    psi_data_new_cust_new_long_term_backup_temp=psi_data_new_cust_new_long_term_backup.T
    psi_data_new_cust_new_long_term_backup_temp.reset_index(inplace=True)
    psi_data_new_cust_new_long_term_backup_temp.rename(columns = {"index": "month",0:"psi"}, inplace=True)
    psi_data_new_cust_new_long_term_backup_temp['month'] = psi_data_new_cust_new_long_term_backup_temp['month'].map(lambda x: x.replace('41_', ''))

    #量化派纯新客长期限模型备份版数据排序
    psi_data_new_cust_new_long_term_backup_temp['month1'] = psi_data_new_cust_new_long_term_backup_temp['month'].map(lambda x: x[:7] if len(x)>6 else x )
    psi_data_new_cust_new_long_term_backup_temp['month2'] = psi_data_new_cust_new_long_term_backup_temp['month1'].map(lambda x: x.replace('-', ''))
    psi_data_new_cust_new_long_term_backup_temp.sort_values(by=['month2'],inplace=True)
    del psi_data_new_cust_new_long_term_backup_temp['month1']
    del psi_data_new_cust_new_long_term_backup_temp['month2']
    #量化派纯新客长期限模型备份版数据处理
    psi_data_new_cust_new_long_term_backup_temp.fillna('-',inplace=True)
    psi_data_new_cust_new_long_term_backup_temp.rename(columns = {"month": "apply_month"}, inplace=True)
    #重排索引
    psi_data_new_cust_new_long_term_backup_temp.reset_index(drop = True,inplace=True)
    return psi_data_new_cust_new_long_term_backup_temp
