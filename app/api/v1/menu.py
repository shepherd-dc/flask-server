import time

from flask import request
from sqlalchemy import or_

from app.libs.error_code import Success, ParameterException, DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.restful_json import restful_json
from app.libs.token_auth import auth
from app.models.base import db
from app.models.menu import Menu
from app.models.submenu import Submenu
from app.validators.forms import MenuForm, SubmenuForm

api = Redprint('menu')


@api.route('')
def get_menu():
    nav = request.values.get('nav', '')
    type = request.values.get('type', '')
    menus = Menu.query

    if type:
        menus = menus.all()
    else:
        menus = menus.filter_by(status=1).all()

    if nav=='nav':
        for menu in menus:
            for submenu in menu.submenu:
                submenu.hide('pic', 'description', 'official_doc', 'status')
    elif nav and nav != 'nav':
        return ParameterException()

    return restful_json(menus)

@api.route('/detail')
def get_menu_detail():
    id = request.values.get('id', '')
    en_name = request.values.get('en_name', '')

    menu = Menu.query.filter(or_(Menu.id==id, Menu.en_name==en_name)).first_or_404()

    return restful_json(menu)

@api.route('/add', methods=['POST'])
@auth.login_required
def add_menu():
    form = MenuForm().validate_for_api()
    with db.auto_commit():
        menu = Menu()
        menu.menu_name = form.menu_name.data
        menu.en_name = form.en_name.data
        menu.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        db.session.add(menu)
    return restful_json(menu)

@api.route('/edit', methods=['PUT'])
@auth.login_required
def edit_menu():
    data = request.get_json()
    id = data['id']
    with db.auto_commit():
        menu = Menu.query.get(id)
        menu.menu_name = data['menu_name']
    return Success()

@api.route('/disable', methods=['POST'])
@auth.login_required
def disable_menu():
    data = request.get_json()
    id = data['id']
    type = data['type']
    with db.auto_commit():
        menu = Menu.query.get(id)
        menu.status = type
    return Success()

@api.route('/delete', methods=['DELETE'])
@auth.login_required
def delete_menu():
    data = request.get_json()
    with db.auto_commit():
        menu = Menu.query.get(data['id'])
        db.session.delete(menu)
    return Success()


@api.route('/submenu')
def get_submenu():
    page_index = int(request.args.get('page', 1))
    page_size = int(request.args.get('limit', 20))
    menu_id = request.args.get('menu_id', '')
    name = request.args.get('name', '')
    status = request.args.get('status', 1)

    submenus = Submenu.query.order_by(Submenu.id.desc())

    if status == 1:
        submenus = submenus.filter(Submenu.status == 1)

    if name:
        submenus = submenus.filter(Submenu.name.like('%' + name + '%'))

    if menu_id:
        submenus = submenus.filter(Submenu.menu_id == menu_id)

    total = submenus.count()
    submenus = submenus.limit(page_size).offset((page_index - 1) * page_size).all()
    data = {
        "total": total,
        "data": submenus
    }

    return restful_json(data)

@api.route('/submenu/<name>')
def get_submenu_detail(name):
    submenu =Submenu.query.filter_by(name=name).first_or_404()
    return restful_json(submenu)

@api.route('/submenu/save', methods=['POST'])
@auth.login_required
def save_submenu():
    form = SubmenuForm().validate_for_api()
    menu = Menu.query.filter_by(id=form.menu_id.data).first_or_404()

    id = form.id.data
    if id:
        with db.auto_commit():
            submenu = Submenu.query.get(id)
            submenu.name = form.name.data
            submenu.path = form.path.data
            submenu.pic = form.pic.data
            submenu.menu_id = form.menu_id.data
            submenu.menu_name = menu.menu_name
            submenu.description = form.description.data
            submenu.official_doc = form.official_doc.data
            submenu.status = form.status.data
        return Success()

    with db.auto_commit():
        submenu = Submenu()
        submenu.name = form.name.data
        submenu.path = form.path.data
        submenu.pic = form.pic.data
        submenu.menu_id = form.menu_id.data
        submenu.menu_name = menu.menu_name
        submenu.description = form.description.data
        submenu.official_doc = form.official_doc.data
        submenu.status = form.status.data
        submenu.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        db.session.add(submenu)

    return restful_json(submenu)

@api.route('/submenu/delete', methods=['POST', 'DELETE'])
@auth.login_required
def delete_submenu():
    data = request.get_json('id')
    submenu = Submenu.query.get(data['id'])

    if request.method == 'POST':
        with db.auto_commit():
            submenu.status = 0

    if request.method == 'DELETE':
        with db.auto_commit():
            db.session.delete(submenu)

    return DeleteSuccess()

