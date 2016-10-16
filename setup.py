from setuptools import setup

requires = [
    'pyramid',
]

setup(name='avalon',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = avalon:main
      """,
)