import os

def get_project_root()->str:
    #当前工程所在的绝对路径
    current_path = os.path.abspath(__file__)
    #获取工程的根目录，先获取当前文件所在目录，再获取上一级目录，即为项目根目录
    project_root = os.path.dirname(current_path)
    project_root = os.path.dirname(project_root)
    return project_root

def get_abs_path(relative_path:str)->str:
    """传递相对路径，返回绝对路径
    :param relative_path: 相对路径
    :return: 绝对路径
    """
    return os.path.join(get_project_root(), relative_path)

if __name__ == '__main__':
    print(get_abs_path('data/test_data.xlsx'))