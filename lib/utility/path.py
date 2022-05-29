import inspect
import os
import sys


def get_root_path():
    '''
    获取当前脚本执行路径，在根目录下新建日志文件
    :return:
    '''
    file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
    parent_path = os.path.dirname(file_path)
    lib_path = os.path.dirname(parent_path)
    root_path = os.path.dirname(lib_path)
    return root_path


def create_var_path():
    root_path = get_root_path()
    var_path = root_path + "/var"
    if not os.path.exists(var_path):
        os.makedirs(var_path)
    return var_path


def create_log_path():
    data_path = create_var_path()
    log_path = data_path + "/log"
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    print(log_path)
    return log_path


LOG_PATH = create_log_path()

if __name__ == "__main__":
    create_log_path()

