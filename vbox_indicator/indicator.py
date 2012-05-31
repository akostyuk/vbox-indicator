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
        self.vms = self.get_vm_list()
        self.ind = appindicator.Indicator('vbox-indicator', 'vbox-indicator', appindicator.CATEGORY_APPLICATION_STATUS)
        self.venv = self.check_paths(self.ind)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_icon('vbox-indicator')
        # create a menu
        self.menu = gtk.Menu()

        # Create VMs menu items:
        if len(self.vms) > 0:
            for v in self.vms:
                item = gtk.MenuItem(label=v, use_underline=False)
                item.connect('activate', self.run_vm, v)
                item.show()
                self.menu.append(item)

        # Create separator (hr line)
        if len(self.vms) > 0:
            hr = gtk.SeparatorMenuItem()
            hr.show()
            self.menu.append(hr)

        # Create VirtualBox menu item
        vbox = gtk.MenuItem(label='VirtualBox')
        vbox.connect('activate', self.run_virtual_box)
        vbox.show()
        self.menu.append(vbox)

        # Create about menu item
        about = gtk.MenuItem(label='About')
        about.connect('activate', self.about)
        about.show()
        self.menu.append(about)

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

    def check_paths(self, indicator):
        venv = os.environ.get('VIRTUAL_ENV')
        if venv:
            icon_path = os.path.abspath(os.path.join(venv,
                'usr/share/icons/ubuntu-mono-dark/apps/22/'))
        else:
            icon_path = '/usr/share/icons/ubuntu-mono-dark/apps/22/'

        indicator.set_icon_theme_path(icon_path)
        return venv

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

    def run_virtual_box(self, widget):
        subprocess.call(['/usr/bin/VirtualBox'])

    def test_callback(self, widget):
        print widget.get_label()

    def about(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name("vbox-indicator")
        about.set_version("0.1")
        about.set_copyright("(c) Alexey Kostyuk")
        about.set_comments("Simple indicator for VirtualBox")
        about.set_website("https://github.com/akostyuk/vbox-indicator")
        if self.venv:
            logo = os.path.join(self.venv,
                'usr/share/vbox-indicator/vbox-indicator.png')
        else:
            logo = '/usr/share/vbox-indicator/vbox-indicator.png'
        about.set_logo(gtk.gdk.pixbuf_new_from_file(logo))
        about.run()
        about.destroy()

    def quit(self, widget, data=None):
        gtk.main_quit()


def main():
    gtk.main()
    return 0


def start():
    VBoxIndicator()
    main()


if __name__ == '__main__':
    indicator = VBoxIndicator()
    main()
