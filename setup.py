from setuptools import setup, find_packages
import os.path
import io

# read contents of README.md
this_dir = os.path.abspath(os.path.dirname(__file__))
README = io.open(os.path.join(this_dir, 'README.md'), encoding='utf8').read()

setup(name='dcim_fau',
      version='0.1',
      long_description=README,
      long_description_content_type='text/markdown',
      author='Henry Herzfeld',
      author_email='herzfeld2@gmail.com',
      keywords=['dcim', 'fau'],
      license='MIT',
      packages=find_packages(),
      python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
      include_package_data=True,
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'scaffold=dcim.command_line:bootstrap',
              'run=dcim.command_line:run',
              ]
          }
      )
