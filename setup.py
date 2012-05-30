from distutils.core import setup

setup(name='vbox-indicator',
    version = '0.1',
    description = 'Simple application indicator for VirtualBox',
    author = 'Alexey Kostyuk',
    author_email = 'unitoff@gmail.com',
    url = 'https://github.com/akostyuk/vbox-indicator',

    packages = ['vbox_indicator'],
    package_data = {'': ['images/*', 'bin/vbox-indicator']},
    scripts = ['bin/vbox-indicator'],
    data_files = [
        ('usr/share/icons/ubuntu-mono-dark/apps/22', [
            'vbox_indicator/images/vbox-indicator.svg']),
        ('usr/share/vbox-indicator', [
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