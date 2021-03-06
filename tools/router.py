__author__ = 'Tang'
from static import get_static, get_permanent

class RuleTree:
    sub = None
    handle = None

    def __init__(self, handle):
        self.sub = {}
        self.handle = handle


def __traverse__(node, name, depth):
    print(depth * '  ' + name+':'+node.handle.func_name)
    for sub_node_name in node.sub:
        __traverse__(node.sub[sub_node_name], sub_node_name, depth+1)


class Router:
    root = None

    def __init__(self):
        self.root = RuleTree(None)

    def route(self, url, handle):
        cur_pos = self.root
        url_list = filter(None, url.split('/'))
        for seg in url_list:
            if seg not in cur_pos.sub:
                cur_pos.sub[seg] = RuleTree(None)
            cur_pos = cur_pos.sub[seg]
        cur_pos.handle = handle

    def match(self, url):
        cur_pos = self.root
        url_list = filter(None, url.split('/'))
        if url_list and url_list[0] == 'static':
            return None
        if url_list and url_list[0] == 'link':
            return None
        for seg in url_list:
            if seg not in cur_pos.sub:
                return None
            cur_pos = cur_pos.sub[seg]
        return cur_pos.handle

    @staticmethod
    def static(url):
        url_list = filter(None, url.split('/'))
        if url_list and url_list[0] == 'static':
            return get_static

        return None

    @staticmethod
    def permanent_link(url):
        url_list = filter(None, url.split('/'))
        if url_list and url_list[0] == 'link':
            return get_permanent

    def p_tree(self):
        __traverse__(self.root, '/', 0)




