from lib.utility.big_db import query_ks_data
import pandas as pd


def build_ks_df():
    def get_ks(target, y_pred):
        df = pd.DataFrame({
            'y_pred': y_pred,
            'target': target,
        })
        df = df.sort_values(by='y_pred', ascending=False)
        df['good'] = 1 - df['target']
        df['bad_rate'] = df['target'].cumsum() / df['target'].sum()
        df['good_rate'] = df['good'].cumsum() / df['good'].sum()
        df['ks'] = df['bad_rate'] - df['good_rate']
        return max(abs(df['ks']))

    month_ks_list = []
    for lend_month, df_month in query_ks_data().groupby(['lend_month', 'new_user_type']):
        month_ks_dict = {}
        ks = round(get_ks(df_month['target'], df_month['xslhp_overdue_m30_with_a_score_backup']),2)
        month_ks_dict['lend_month'] = lend_month[0]
        month_ks_dict['user_type'] = lend_month[1]
        month_ks_dict['ks'] = ks
        month_ks_list.append(month_ks_dict)
    ks_result = pd.DataFrame(month_ks_list)
    ks_result = ks_result[ks_result['user_type'] == '41']
    ks_result_new_cust_long_term_ks_backup = ks_result[['lend_month', 'ks']]
    return ks_result_new_cust_long_term_ks_backup


