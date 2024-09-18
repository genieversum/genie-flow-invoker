import os
from setuptools import setup, find_packages

version = os.getenv('CI_COMMIT_TAG', '0.0.0')
PAT_TOKEN = os.getenv('CI_JOB_TOKEN')

setup(
    name='genie_flow_invoker',
    version=version,
    description='TODO',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/your_username/your_project',
    author='Willem Van Asperen',
    author_email='willem.van.asperen@paconsulting.com',
    license='MIT',  # Or any other license
    packages=find_packages(),
    dependency_links=[
        f'https://__token__:{PAT_TOKEN}@gitlab.stopstaringatme.org/api/v4/projects/165/packages/pypi/simple'
    ],
    install_requires=[
        'loguru~=0.7.2',
        'openai~=1.28.1',
        'PyYAML~=6.0.1',
        'requests~=2.31.0',
        'dependency-injector~=4.41.0',
        'weaviate-client~=4.6.5',
        'neo4j~=5.22.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='~=3.11.0',
)
