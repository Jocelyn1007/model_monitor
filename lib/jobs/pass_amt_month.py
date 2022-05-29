from lib.utility.big_db import bigquery
import pandas as pd
from lib.properties.product_prop import product_map

def apply_data_month():
    apply_sql = '''select date_format(apply_date, 'yyyy-MM') as month
       ,product_id
       ,count(apply_no) as total_no
       ,sum(case when loan_id <> 'null' and current_step <> '归档/超时取消' and current_step <> '放款处理中' then 1 else 0 end ) as pass_no
       ,round(sum(case when loan_id <> 'null' and current_step <> '归档/超时取消' and current_step <> '放款处理中' then approve_money else 0 end )/10000,2) as approve_amt_W
        from  dm_asset.dm_asset_ar_apply_info
        where date_format(apply_date, 'yyyy-MM') = FROM_UNIXTIME(UNIX_TIMESTAMP(), 'yyyy-MM')
        and product_id in (
        '10010',
        '10011',
        '10016',
        '10023',
        '10025',
        '10029',
        '10030')
        group by date_format(apply_date, 'yyyy-MM'), product_id, product_name'''

    results = bigquery(apply_sql)
    # results = [{'product_id': '10010',
    #   'total_no': 1549,
    #   'pass_no': 1002,
    #   'approve_amt_w': 837.1},
    #  {'product_id': '10011', 'total_no': 5, 'pass_no': 1, 'approve_amt_w': 1.0},
    #  {'product_id': '10016',
    #   'total_no': 731,
    #   'pass_no': 485,
    #   'approve_amt_w': 411.4},
    #  {'product_id': '10025',
    #   'total_no': 1495,
    #   'pass_no': 122,
    #   'approve_amt_w': 65.27}]
    df = pd.DataFrame(results, columns=results[0].keys())
    df.insert(1, 'product_name', df['product_id'].map(product_map))
    return df
