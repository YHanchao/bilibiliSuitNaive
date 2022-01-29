from requests import get as rqGet
from os.path import exists as osPathExists
from os import makedirs as osMakedirs
import errors
from json import dumps, loads
from math import ceil


def get_all_suit(query=None, refresh=0, page=0):
    '''
    获取所有装扮

    输入:
        - query: 查询条件，指名字或装扮ID
        - refresh: 是否刷新，若刷新(refresh = 1)则重新获取装扮列表，默认为0
    返回值: 用以渲染页面的列表
    '''
    base_list = list()
    if (refresh == 1 or not osPathExists('suit_list.json')):
        try:
            res = rqGet('https://api.bilibili.com/x/garb/mall/suit/all')
        except:
            errors._show_error(1)
            return list(), 0, 0, 1

        res = res.json()
        for cat in res['data']['category']:
            for suit in cat['suits']:
                base_list.append({
                    'name': suit['name'],
                    'item_id': suit['item_id'],
                    'category': cat['name'],
                    'desc': suit['properties']['desc'],
                    'cover': suit['properties']['image_cover']
                })
        try:
            with open('suit_list.json', 'w', encoding='utf-8') as json_file:
                json_file.write(dumps(base_list, ensure_ascii=False))
        except:
            return list(), 0, 0, 2
    else:
        try:
            with open('suit_list.json', 'r', encoding='utf-8') as json_file:
                base_list = loads(json_file.read())
        except:
            return list(), 0, 0, 5

    # 假定json文件没有被修改
    if (query is not None):
        res_list = list()
        if (isinstance(query, str)):
            for obj in base_list:
                if (obj['name'].find(query) >= 0):
                    res_list.append(obj)
        else:
            errors._show_error(3)
        base_list = res_list

    total_page = ceil(len(base_list) / 10)
    if (page == total_page - 1):
        base_list = base_list[10 * page:]
    elif (page < total_page - 1):
        base_list = base_list[10 * page:10 * (page + 1)]

    # 图片缓存
    temp_dir = './static/temp/'
    if not osPathExists(temp_dir):
        osMakedirs(temp_dir)
    for item in base_list:
        img_url = item['cover']
        item['cover'] = item['cover'].split('/')[-1]
        if not osPathExists(temp_dir + item['cover']):
            try:
                temp_img = rqGet(img_url)
                with open(temp_dir + item['cover'], 'wb') as temp_pic:
                    temp_pic.write(temp_img.content)
            except OSError:
                errors._show_error(2)
                return list(), 0, 0, 2
            except:
                errors._show_error(1)
                return list(), 0, 0, 1
    return base_list, total_page, page, 100


def get_suit(suit_id, base_dir='./src/'):
    '''
    获取单个装扮素材

    输入:
        - suit_id: 装扮ID
        - base_dir: 存储路径
    输出: 素材文件夹
    '''
    final_status = 100
    try:
        rq_get = rqGet(
            'https://api.bilibili.com/x/garb/mall/item/suit/v2?&part=suit&item_id='
            + str(suit_id))
    except:
        errors._show_error(1)
        return dict(), 1

    res = rq_get.json()

    if res['data']['item']['item_id'] == 0:
        errors._show_error(0)
        return dict(), 0

    base_dir += res['data']['item']['name']

    # Save suit !!
    if not osPathExists(base_dir):
        osMakedirs(base_dir)
    with open(base_dir + '/suit_info.json', 'w', encoding='utf-8') as suit_json_file:
        suit_json_file.write(rq_get.text)

    # part 1. Emoji
    emoji_list = [
        (item['name'][1:-1], item['properties']['image'])
        for item in res['data']['suit_items']['emoji_package'][0]['items']
    ]
    if not osPathExists(base_dir + '/emoji/'):
        osMakedirs(base_dir + '/emoji/')

    for i, item in enumerate(emoji_list):
        img_name = item[0]
        try:
            with open(base_dir + '/emoji/' + img_name + '.png',
                      'wb') as emoji_file:
                emoji_file.write(rqGet(item[1]).content)
        except OSError:
            errors._show_error(4)
            img_name = img_name.split('_')[0] + '_{}'.format(i)
            try:
                with open(base_dir + '/emoji/' + img_name + '.png', 'wb') as emoji_file:
                    emoji_file.write(rqGet(item[1]).content)
            except:
                pass
            final_status = 101
        except:
            errors._show_error(1)
            return dict(), 1

    # part 2. Background
    bg_dict = res['data']['suit_items']['space_bg'][0]['properties']
    bg_list = list()

    for key, value in bg_dict.items():
        if key[0] == 'i':
            bg_list.append((key, value))

    if not osPathExists(base_dir + '/background/'):
        osMakedirs(base_dir + '/background/')

    for item in bg_list:
        try:
            with open(base_dir + '/background/' + item[0] + '.jpg',
                      'wb') as bg_file:
                bg_file.write(rqGet(item[1]).content)
        except:
            errors._show_error(1)
            return dict(), 1

    # part 3. Others
    if not osPathExists(base_dir + '/properties/'):
        osMakedirs(base_dir + '/properties/')
    pro_list = [
        ('properties.zip',
         res['data']['suit_items']['skin'][0]['properties']['package_url']),
        ('fan_share_image.jpg',
         res['data']['item']['properties']['fan_share_image']),
        ('image_cover.jpg', res['data']['item']['properties']['image_cover']),
        ('avatar.jpg', res['data']['fan_user']['avatar']),
        ('thumbup.jpg',
         res['data']['suit_items']['thumbup'][0]['properties']['image_preview']
         )
    ]
    for item in pro_list:
        try:
            with open(base_dir + '/properties/' + item[0], 'wb') as pro_file:
                pro_file.write(rqGet(item[1]).content)
        except:
            errors._show_error(1)
            return dict(), 1

    return res, final_status
