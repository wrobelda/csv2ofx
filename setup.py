from distutils.core import setup

setup(
 name='csv2ofx.py',
 author = "Dennis Muhlestein",
 version='0.2',
 packages=['csv2ofx.py'],
 package_dir={'csv2ofx.py':'src/csv2ofx.py'},
 scripts=['csv2ofx.py'],
 package_data={'csv2ofx.py':['*.xrc']}
)

