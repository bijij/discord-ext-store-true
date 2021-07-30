from setuptools import setup
import re

version = ''
with open('discord/ext/store_true/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

if version.endswith(('a', 'b', 'rc')):
    # append version identifier based on commit count
    try:
        import subprocess
        p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += out.decode('utf-8').strip()
        p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += '+g' + out.decode('utf-8').strip()
    except Exception:
        pass

setup(name='discord-ext-store-true',
      author='Bijij',
      url='https://github.com/bijij/discord-ext-store-true',
      version=version,
      packages=['discord.ext.store_true'],
      license='MIT',
      description='An extension module to allow store-true like behaviour with discord.py flag converters.',
      install_requires=['discord.py>=2.0.0a'],
      python_requires='>=3.8.0'
)