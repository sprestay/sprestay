from app import app, db
from flask import render_template, g, request, redirect, url_for, session
from functools import wraps
from user import User
from functions import yearsago, get_user_tags
from datetime import datetime
import random, re 
from operator import attrgetter
from geopy import Nominatim

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def need_profile_info(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.age<18 or not g.user.gender:
            return redirect(url_for('profile'))
        return f(*args, **kwargs)
    return decorated_function
            
@app.before_request
def g_tester():
    if 'username' in session and session['username']:
        g.user = User.get_filter(username=session['username'])[0] #надо ли эТО?
    else:
        g.user = None

@app.route('/update_date', methods=['GET','POST'])
def update_date():
    if request.method == 'POST' and g.user is not None:# тогда не надо и это
        g.user.update(last_seen=datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")) 
        return ('ok')
    return redirect('/')



@app.route('/', methods=['GET', 'POST'])
@login_required
@need_profile_info
def index():
    dic = {}
    dic['username!'] = session['username']
    dic['JUST_ADD'] = " AND id NOT IN (SELECT whom FROM blacklist WHERE who={})".format(g.user.id)  ### КУДА ВСТАВИТЬ?
    dic['JUST_ADD'] = " AND birth IS NOT NULL AND gender IS NOT NULL"

    if (g.user.orient == "hetero"):
        dic['gender!'] = g.user.gender
    if (g.user.orient == "homo"):
        dic['gender'] = g.user.gender

    if request.args:
        things_must_to_be = ['min_age', 'max_age', 'min_distance', 'max_distance', 'pop_radio', 'min_tags', 'max_tags', 'for_sort', 'search_tags', 'age_gap', 'fame_gap', 'loc_search']
        if list(request.args) == things_must_to_be:
            a = request.args
            if a['min_age'].isdecimal() and a['max_age'].isdecimal() and a['min_distance'].isdecimal() and a['max_distance'].isdecimal() and a['min_tags'].isdecimal() and a['max_tags'].isdecimal() and a['age_gap'].isdecimal() and a['fame_gap'].isdecimal():
                pop_list = ['all', 'low', 'medium', 'high']
                sort_list = ['common_tag', 'no', 'fame', 'age', 'distance']
                if 18 <= int(a['min_age']) <= 100 and 18 <= int(a['max_age']) <= 100 and 0 <= int(a['min_distance']) <= 30000 and 0 <= int(a['max_distance']) <= 30000 \
                and 0 <= int(a['min_tags']) <= 20 and 0 <= int(a['max_tags']) <= 20 and re.match(r'^[A-zА-я\s]*$', a['search_tags']) and a['pop_radio'] in pop_list and a['for_sort'] in sort_list \
                and 0 <= int(a['age_gap']) <= 100 and 0 <= int(a['fame_gap']) <= 100:
                    dic['birth<'] = yearsago(int(a['min_age']))
                    dic['birth>'] = yearsago(int(a['max_age']))

                    if a['loc_search']:
                        geo = Nominatim(timeout=5)
                        location = geo.geocode(a['loc_search'])
                        if location and 'boundingbox' in location.raw:
                            coords = location.raw['boundingbox']
                            dic['JUST_ADD'] = " AND `X` BETWEEN {} AND {} AND `Y` BETWEEN {} AND {}".format(coords[0], coords[1], coords[2], coords[3])
                    if (a['age_gap']):
                        gap_min = int(g.user.age) - int(a['age_gap']) if int(g.user.age) - int(a['age_gap']) > int(a['min_age']) else int(a['min_age'])
                        gap_max = int(g.user.age) + int(a['age_gap']) if int(g.user.age) - int(a['age_gap']) < int(a['max_age']) else int(a['max_age'])
                        dic['birth<'] = yearsago(gap_min)
                        dic['birth>'] = yearsago(gap_max)
                    if (a['pop_radio'] == 'low'):
                        dic['fame<'] = "(SELECT MAX(fame) FROM account)/5"
                    if (a['pop_radio'] == 'medium'):
                        dic['fame>'] = "(SELECT MAX(fame) FROM account)/5"
                        dic['fame<'] = "(SELECT MAX(fame) FROM account)*0.8"
                    if (a['pop_radio'] == 'high'):
                        dic['fame>'] = "(SELECT MAX(fame) FROM account)*0.8"
                    if (a['fame_gap']):
                        dic['fame>'] = "((SELECT fame FROM account WHERE username='{}')-(SELECT MAX(fame) FROM account)*{})".format(g.user.username, int(a['fame_gap']) / 100)
                        dic['fame<'] = "((SELECT fame FROM account WHERE username='{}')+(SELECT MAX(fame) FROM account)*{})".format(g.user.username, int(a['fame_gap']) / 100)
                    without_distance = User.get_filter(**dic)
                    users = []
                    with_distance = []
                    for i in without_distance: # фильтр - диапазон дистанции
                        if i.distance >= int(a['min_distance']) and i.distance <= int(a['max_distance']):
                            with_distance.append(i)

                    tags_for_search = [i for i in a['search_tags'].split(' ') if i]
                    words = set(tags_for_search)
                    user_tags = get_user_tags(g.user.id)
                    for i in with_distance: # фильтр по количеству общих тегов
                        tags = set(get_user_tags(i.id)) 
                        if words <= tags: #поиск по тэгам
                            s = sum(1 for j in tags if j in user_tags)
                            if s >= int(a['min_tags']) and s <= int(a['max_tags']):
                                i.common_tag = s
                                users.append(i)

                    if a['for_sort'] != 'no':
                        if a['for_sort'] == "fame" or a['for_sort'] == "common_tag":
                            users = sorted(users, key = attrgetter(a['for_sort']), reverse=True)
                        else:
                            users = sorted(users, key = attrgetter(a['for_sort']))
                    else:
                        users = sorted(users, key=attrgetter("clever")) # нужна ли она здесь?
                    return render_template('index.html', users=users)
                else: return redirect('/') # ВНИМАНИЕ!
            else: return redirect('/')
        else: return redirect('/')
    users = User.get_filter(**dic)
    users = sorted(users, key=attrgetter("clever"), reverse=True)### умная сортировка по заданию
    return render_template('index.html', users=users)