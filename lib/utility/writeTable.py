import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six
import matplotlib
from lib.properties.product_prop import product_map

from lib.utility.writelog import log
# 导入字体库函数
from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname=r"simsun.ttc", size=15)
logger = log()
matplotlib.use('agg')
def render_mpl_table(data,title_name, col_width=4.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    logger.info("开始绘制图形")
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 3])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    ax.set_title(title_name, weight='bold',fontsize=16,FontProperties=font_set)
    logger.info("图形绘制完毕")
    return ax


if __name__ == '__main__':
    columns = [('product_id', 'STRING_TYPE', None, None, None, None, True),
                 ('total_no', 'BIGINT_TYPE', None, None, None, None, True),
                 ('pass_no', 'BIGINT_TYPE', None, None, None, None, True),
                 ('approve_amt_w', 'DOUBLE_TYPE', None, None, None, None, True)]
    results = [('10010',  1549, 1002, 837.1)]
    # ,
    #              ('10011',  5, 1, 1.0),
    #              ('10016', 731, 485, 411.4),
    #              ('10025', 1495, 122, 65.27)]

    results = [dict(zip([col[0] for col in columns], row)) for row in results]
    df = pd.DataFrame(results, columns=results[0].keys())
    df.insert(1, 'product_name', df['product_id'].map(product_map))
    data  = df
    render_mpl_table(df, title_name='pass_daily',header_columns=0, col_width=3.0)
    plt.show()
    plt.savefig('results/pass_daily/20201026.png')