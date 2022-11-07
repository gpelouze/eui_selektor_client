import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()
with open('requirements.txt', 'r') as f:
    requirements = f.read().strip('\n').split('\n')

setuptools.setup(
    name='eui_selektor_client',
    version='2022.11.07',
    author='Gabriel Pelouze',
    author_email='gabriel.pelouze@universite-paris-saclay.fr',
    description='Lightweight client for EUI Selektor',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gpelouze/eui_selektor_client',
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