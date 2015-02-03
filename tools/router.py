__author__ = 'Tang'


class RuleTree:
    sub = None
    handle = None

    def __init__(self, handle):
        self.sub = {}
        self.handle = handle


def __traverse__(node, name, depth):
    print(depth * '  ' + name)
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
        if url_list[0] == 'static':
            return None
        for seg in url_list:
            if seg not in cur_pos.sub:
                return None
        return cur_pos.handle

    def p_tree(self):
        __traverse__(self.root, '/', 0)




