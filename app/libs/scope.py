class Scope:
    allow_api = []
    allow_module = []
    forbidden = []

    def __add__(self, other):
        # 运算符重载
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))

        return self


class UserScope(Scope):
    # allow_api = ['v1.user/get_user', 'v1.user/delete_user']
    # allow_module = ['v1.gift']
    forbidden = ['v1.user/super_get_user', 'v1.user/super_delete_user']

    def __init__(self):
        self + AdminScope()
        # pass


class AdminScope(Scope):
    # allow_api = ['v1.user/super_get_user', 'v1.user/super_delete_user']
    allow_module = ['v1.user', 'v1.gift', 'v1.menu', 'v1.article']

    def __init__(self):
        # self + UserScope()
        pass


# class SuperScope(Scope):
#     allow_module = []
#
#     def __init__(self):
#         self + AdminScope() + UserScope()


def is_in_scope(scope, endpoint):
    # scope()
    # 反射
    # globals
    # v1.red_name/view_func
    scope = globals()[scope]()
    splits = endpoint.split('/')
    red_name = splits[0]
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False
