from setuptools import setup

setup(
    name='pinotify',
    version='0.1',
    description='Notification system for raspberry pi, for displaying notifications on character LCD screens',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Notification'
    ],
    url='https://github.com/robehickman/raspi_notification',
    author='Robert Hickman',
    author_email='robehickman@gmail.com',
    license='MIT',
    packages=['pinotify', 'pinotify.plugins'],
    install_requires=[
    ],
    scripts=['script/pinotify'],
    zip_safe=False)

