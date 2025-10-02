import os
from cudatext import *
import random
import locale
import cuda_addonman

class Command:

    def __init__(self):
        self.h_tree = app_proc(PROC_GET_CODETREE, '')
        self.lexer_def = 'Text with indentation'
        self.lexer_def_ = 'Text_with_indentation'

        self.packets = cuda_addonman.work_remote.get_remote_addons_list(cuda_addonman.opt.ch_def + cuda_addonman.opt.ch_user)
        print(self.packets)
        for packet in self.packets:
            if (packet['name'] == self.lexer_def_):
                fn = cuda_addonman.work_remote.get_plugin_zip(packet['url'])
                if os.path.isfile(fn):
                    file_open(fn, options='/silent')

    def update_tree(self):
        ed.set_prop(PROP_CODETREE, False)
        tree_proc(self.h_tree, TREE_ITEM_DELETE, 0)
        res = self.get_random_line()
        if res:
            for line in res:
                tree_proc(self.h_tree, TREE_ITEM_ADD, 0, index = -1, text = line)

    def check_and_update(self):
        if ed.get_prop(PROP_LEXER_FILE) == '':
            ed.set_prop(PROP_LEXER_FILE, self.lexer_def)
        if ed.get_prop(PROP_LEXER_FILE) == self.lexer_def:
            self.update_tree()

    def on_open(self, ed_self):
        self.check_and_update()

    def on_tab_change(self, ed_self):
        self.check_and_update()

    def get_random_line(self):
        fn = 'data_ru.txt' if 'ru' in locale.getlocale()[0] else 'data_en.txt'
        path = os.path.dirname(os.path.realpath(__file__)) + os.sep + fn
        try:
            with open(path, 'r', encoding = 'utf-8') as file:
                lines = file.readlines()
                if not lines:
                    return None
                line = random.choice(lines).rstrip('\n')
                words = line.split()
                i = 0
                words_ = ''
                res = []
                for word in words:
                    i = i + 1
                    words_ = words_ + word + ' '
                    if i == 3:
                        res.append(words_)
                        i = 0
                        words_ = ''
                len_ = len(words) - len(res) * 3
                if (len_ > 0):
                    words_ = ''
                    for word_ in words[len(words) - len_:len(words)]:
                        words_ = words_ + word_ + ' '
                    res.append(words_)

                return res
        except FileNotFoundError:
            print(f"error: file '{fn}' not found")
            return None