import schedule
import os
import matplotlib.pyplot as plt
import time
import matplotlib
from lib.jobs.pass_amt_daily import apply_data_daily
from lib.jobs.pass_amt_month import apply_data_month
from lib.jobs.cal_psi import cal_psi_df
from lib.jobs.build_ks import build_ks_df
from lib.utility.writeTable import render_mpl_table
from lib.utility.wxwork import send_images
from lib.utility.writelog import log
from datetime import datetime, timedelta

logger = log()
matplotlib.use('agg')
pass_daily_file_path='results/pass_daily/'
pass_month_file_path='results/pass_month/'
psi_daily_file_path='results/psi_daily/'
ks_daily_file_path='results/ks_daily/'

os.makedirs(pass_daily_file_path, exist_ok=True)
os.makedirs(pass_month_file_path, exist_ok=True)
os.makedirs(psi_daily_file_path, exist_ok=True)
os.makedirs(ks_daily_file_path, exist_ok=True)

def apply_pass_amt_daily():
    date = time.strftime("%Y-%m-%d", time.localtime())
    # 获取数据
    data = apply_data_daily()
    # 转换图片
    render_mpl_table(data, title_name='昨日申请-放款情况', header_columns=0, col_width=3.0)
    file_path = pass_daily_file_path + '{0}.png'.format(date)
    plt.savefig(file_path)
    logger.info('保存图片结束')
    # 发送微信
    send_images(file_path)

def apply_pass_amt_month():
    date = time.strftime("%Y-%m-%d", time.localtime())
    # 获取数据
    data = apply_data_month()
    # 转换图片
    render_mpl_table(data, title_name='当月申请-放款情况', header_columns=0, col_width=3.0)
    file_path = pass_month_file_path + '{0}.png'.format(date)
    plt.savefig(file_path)
    logger.info('保存图片结束')
    # 发送微信
    send_images(file_path)

def apply_get_ks():
    date = time.strftime("%Y-%m-%d", time.localtime())
    # 获取数据
    data = build_ks_df()
    # 转换图片
    render_mpl_table(data, title_name='量化派新客长期限模型ks放款截至{}日'.format((datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")),header_columns=0, col_width=3.0)
    file_path = ks_daily_file_path+'{0}.png'.format(date)
    plt.savefig(file_path)
    logger.info('保存图片结束')
    # 发送微信
    send_images(file_path)
def apply_cal_psi():
    date = time.strftime("%Y-%m-%d", time.localtime())
    # 获取数据
    data = cal_psi_df()
    # 转换图片
    render_mpl_table(data, title_name=u'量化派新客长期限模型psi',
                     header_columns=0, col_width=3.0)
    file_path = psi_daily_file_path+'{0}.png'.format(date)
    plt.savefig(file_path)
    logger.info('保存图片结束')
    # 发送微信
    send_images(file_path)

def jobs():
    apply_pass_amt_daily()
    apply_pass_amt_month()
    apply_get_ks()
    apply_cal_psi()

# def apply_get_ks():
#     body = build_ks_df()
#     msg = send_wx_md(body, msgtype='markdown')
#     return msg

if __name__ == '__main__':
    jobs()  # 启动时运行一次
    #schedule.every(5).minutes.do(jobs)
    schedule.every().day.at("09:00").do(jobs)  # 每天9点运行一次
    # apply_cal_psi()
    # apply_get_ks()  # 启动时运行一次
    # schedule.every().day.at("17:50").do(apply_get_ks)  # 每天9点30运行一次
    # # # print('启动apply_get_ks成功')
    # schedule.every().day.at("14:05").do(apply_get_ks)  # 每周一 8:00执行一次任务
    # schedule.every(5).minutes.do(apply_pass_amt)
    # schedule.every(5).minutes.do(apply_get_ks)


    while True:
        schedule.run_pending()
