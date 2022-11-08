import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()
with open('requirements.txt', 'r') as f:
    requirements = f.read().strip('\n').split('\n')

entry_points = {
    'console_scripts': [
        'eui_selektor_client=eui_selektor_client.cli:cli',
        ]
    }

setuptools.setup(
    name='eui_selektor_client',
    version='2022.11.08',
    author='Gabriel Pelouze',
    author_email='gabriel.pelouze@universite-paris-saclay.fr',
    description='Lightweight client for EUI Selektor',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gpelouze/eui_selektor_client',
    entry_points=entry_points,
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        ],
)