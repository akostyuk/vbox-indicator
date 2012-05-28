#!/usr/bin/env python

import os
import re
import sys
import subprocess
import pygtk
pygtk.require('2.0')
import gtk
import appindicator


class VBoxIndicator:
    def __init__(self):
        self.check_vbox_manage_program()
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.vms = self.get_vm_list()
        self.ind = appindicator.Indicator('vbox-indicator', 'vbox-indicator', appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_icon_theme_path(self.path)
        self.ind.set_icon('vbox-indicator')
        # create a menu
        self.menu = gtk.Menu()

        # create items for the menu - labels, checkboxes, radio buttons and images are supported:
        if len(self.vms) > 0:
            for v in self.vms:
                item = gtk.MenuItem(label=v, use_underline=False)
                item.connect('activate', self.run_vm, v)
                item.show()
                self.menu.append(item)
        else:
            pass

        # Quit menu item
        image = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        image.connect('activate', self.quit)
        image.show()
        self.menu.append(image)

        self.menu.show()

        self.ind.set_menu(self.menu)

    def check_vbox_manage_program(self):
        if not os.path.exists('/usr/bin/VBoxManage'):
            raise RuntimeError('Could not find VBoxManage '
                                'at /usr/bin is it installed?')
            sys.exit()

    def get_vm_list(self):
        o = subprocess.check_output(['/usr/bin/VBoxManage', 'list', 'vms'])
        vms = o.strip().split('\n')
        regex = re.compile('^(\".+\") (\{.+\})')
        vms_list = []
        for v in vms:
            r = regex.search(v)
            if r:
                vms_list.append(r.groups()[0].replace('\"', ''))
        return vms_list

    def run_vm(self, widget, data=None):
        vm = data if data is not None else widget.get_label()
        subprocess.call(['/usr/bin/VBoxManage', 'startvm', '%s' % vm])

    def test_callback(self, widget):
        print widget.get_label()

    def quit(self, widget, data=None):
        gtk.main_quit()


def main():
    gtk.main()
    return 0

if __name__ == '__main__':
    indicator = VBoxIndicator()
    main()
