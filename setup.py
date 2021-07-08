from setuptools import setup

setup(
    name='FotoOrg',
    version='0.0.8',
    packages=['fotorg', 'fotorg.info', 'fotorg.info.data'],
    url='https://github.com/dolikemc/',
    license='http://www.apache.org/licenses/LICENSE-2.0',
    author='christoph',
    author_email='dolikemc@gmail.com',
    description='Organize your Fotos',
    install_requires=[
        'sqlalchemy>=1.4.20',
        'Pillow>=8.3.0',
        'geopy>=2.1.0',
    ],
)
