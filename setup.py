import os
import subprocess
from distutils.core import setup
from distutils.command.install_data import install_data

# Hack for virtualenv
venv = os.environ.get('VIRTUAL_ENV')
if venv:
    usr_prefix = os.path.join(venv, 'usr')
else:
    usr_prefix = '/usr/'


class post_install(install_data):
    def run(self):
        # Call parent
        install_data.run(self)
        # Execute commands
        if os.path.exists('%sshare/icons/ubuntu-mono-dark/.icon-theme.cache' %
                            usr_prefix):
            print "Updating icons cache"
            subprocess.call(['/usr/bin/gtk-update-icon-cache',
                            '-f', '-t', '%sshare/icons/ubuntu-mono-dark' %
                            usr_prefix])


setup(name='vbox-indicator',
    cmdclass={"install_data": post_install},
    version = '0.1',
    description = 'Simple application indicator for VirtualBox',
    author = 'Alexey Kostyuk',
    author_email = 'unitoff@gmail.com',
    url = 'https://github.com/akostyuk/vbox-indicator',

    packages = ['vbox_indicator'],
    package_data = {'': ['bin/vbox-indicator']},
    scripts = ['bin/vbox-indicator'],
    data_files = [
        ('%sshare/icons/ubuntu-mono-dark/apps/22' % usr_prefix, [
            'vbox_indicator/images/vbox-indicator.svg']),
        ('%sshare/vbox-indicator' % usr_prefix, [
            'vbox_indicator/images/vbox-indicator.png']),
    ],

    classifiers = [
        'Programming Language :: Python :: 2.7',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Intended Audience :: Users',
        'Operating System :: Ubuntu',
        'Topic :: Desktop',
    ],

)