import os
from src.db import DB
from src.main import message_processor, KEYWORDS
from src.utils import get_object_values

user_1 = 123456789
user_2 = 987654321
group = 123

k = get_object_values(KEYWORDS)
print(k)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def wrap(user: int, message: str, at_qq: int = None, comment: str = None):
    if comment:
        print(bcolors.OKGREEN + "------" + comment + "------" + bcolors.ENDC)
    message_processor(
        message=message,
        qq=user,
        group=group,
        at_qq=at_qq
    )


base_db_path = os.path.join(os.path.dirname(__file__), 'src', 'data')
for file in os.listdir(base_db_path):
    os.remove(os.path.join(base_db_path, file))


def test2():
    wrap(user_1, '打胶', comment='没注册')
    wrap(user_1, '牛子', comment='注册')
    wrap(user_1, '打胶', user_2, comment='打胶别人失败')
    wrap(user_1, 'pk', user_2, comment='pk 别人失败')
    wrap(user_1, '🔒', user_2, comment='🔒别人失败')
    wrap(user_1, '牛子', comment='查牛子信息')

    wrap(user_2, '牛子', comment='对方注册')
    wrap(user_2, '牛子', comment='user 2 查牛子信息')
    wrap(user_2, '打胶', comment='user 2 自己打胶 l+1')
    wrap(user_2, '🔒我', comment='user 2 自己🔒自己 s+1')
    wrap(user_2, '牛子', user_1, comment='user 2 查牛子是否短了')
    wrap(user_2, 'pk', comment='None')
    wrap(user_2, '🔒', comment='None')
    wrap(user_2, '打胶', user_1, comment='user 2 打胶 user 1 l+2')
    wrap(user_2, '🔒', user_1, comment='user 2 🔒 user 1 s+2')
    wrap(user_2, 'pk', user_1, comment='user 2 pk user p+1')
    wrap(user_1, '牛子', user_1, comment='user 1 查牛子是否变了')

    # cd
    wrap(user_2, 'pk', user_1, comment='user 2 反复 pk p+2')
    wrap(user_2, 'pk', user_1, comment='user 2 反复 pk p+3')
    wrap(user_2, 'pk', user_1, comment='user 2 反复 pk p+4')
    wrap(user_2, 'pk', user_1, comment='user 2 反复 pk p+5 cd')
    wrap(user_2, 'pk', user_1, comment='user 2 反复 pk p+6 cd')
    wrap(user_2, '🔒', user_1, comment='user 2 反复 🔒 s+3')
    wrap(user_2, '🔒', user_1, comment='user 2 反复 🔒 s+4')
    wrap(user_2, '🔒', user_1, comment='user 2 反复 🔒 s+5 cd')
    wrap(user_2, '🔒', user_1, comment='user 2 反复 🔒 s+6 cd')
    wrap(user_2, '打胶', user_1, comment='user 2 反复 打胶 l+3')
    wrap(user_2, '打胶', user_1, comment='user 2 反复 打胶 l+4')
    wrap(user_2, '打胶', user_1, comment='user 2 反复 打胶 l+5 cd')
    wrap(user_2, '打胶', user_1, comment='user 2 反复 打胶 l+6 cd')

    wrap(user_1, '牛子', comment='user 1 查牛子是否变了')
    wrap(user_1, '打胶', comment='user 1 反复自己打胶 l+1')
    wrap(user_1, '打胶', comment='user 1 反复自己打胶 l+2')
    wrap(user_1, '打胶', comment='user 1 反复自己打胶 l+3')
    wrap(user_1, '打胶', comment='user 1 反复自己打胶 l+4')
    wrap(user_1, '打胶', comment='user 1 反复自己打胶 l+5 cd')
    wrap(user_1, '🔒我', comment='user 1 反复自己🔒自己 s+1')
    wrap(user_1, '🔒我', comment='user 1 反复自己🔒自己 s+2')
    wrap(user_1, '🔒我', comment='user 1 反复自己🔒自己 s+3')
    wrap(user_1, '🔒我', comment='user 1 反复自己🔒自己 s+4')
    wrap(user_1, '🔒我', comment='user 1 反复自己🔒自己 s+5 cd')

    # self
    wrap(user_1, 'pk', user_1, 'user 1 pk 自己 p+1')
    wrap(user_1, '🔒', user_1, 'user 1 🔒 自己 s+6 cd')
    wrap(user_1, '打胶', user_1, 'user 1 打胶 自己 l+6 cd')

    # 查信息
    wrap(user_1, '牛子', comment='user 1 查牛子信息')
    wrap(user_2, '牛子', comment='user 2 查牛子信息')

    # 隔日
    data = DB.load_data(user_1)
    data['latest_daily_lock'] = '2020-01-01 00:00:01'
    data['pked_time'] = '2020-01-01 00:00:01'
    DB.write_data(user_1, data)
    wrap(user_1, '牛子', comment='user 1 隔日查牛子信息')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+1')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+2')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+3')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+4')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+5 cd')

    # 大额惩罚机制
    data = DB.load_data(user_1)
    data['length'] = 25
    data['latest_daily_lock'] = '2020-01-01 00:00:01'
    DB.write_data(user_1, data)
    wrap(user_1, '牛子', comment='大额惩罚机制 user 1 查牛子信息')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+1')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+2')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+3')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+4')
    wrap(user_1, '🔒我', comment='user 1 🔒自己 l+5 cd')
    wrap(user_1, '🔒', user_2, comment='user 1 🔒别人 l+6 cd')

    # max
    data = DB.load_data(user_1)
    data['daily_lock_count'] = 6
    data['daily_glue_count'] = 5
    data['latest_daily_glue'] = '2023-01-25 01:00:00'
    data['daily_pk_count'] = 6
    data['latest_daily_pk'] = '2023-01-25 01:00:00'
    DB.write_data(user_1, data)
    wrap(user_1, '🔒', user_2, comment='user 1 🔒 user 2 max')
    wrap(user_1, '打胶', user_2, comment='user 1 打胶 user 2')
    wrap(user_1, '打胶', user_2, comment='user 1 打胶 user 2 max')
    wrap(user_1, 'pk', user_2, comment='user 1 pk user 2 max')

    # 看别人牛子
    wrap(user_1, '看他牛子', user_2, comment='user 1 查 user 2 牛子信息')
    wrap(user_1, '看他牛子', comment='None')

test2()
