from setuptools import setup

req = open('./requirements.txt').read().split('\n')

setup(name='seo_tools',
      version='0.0.1',
      description='DME Simple SEO Tools',
      url='https://git-codecommit.us-east-1.amazonaws.com/v1/repos/seo_tools',
      author='Tristan Smith',
      author_email='tristan.smith@perficient.com',
      license='MIT',
      packages=['seo_tools'],
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'blighthouse = seo_tools.__main__:blighthouse',
              'convert_crawlreport = seo_tools.crawl_report:main'
          ]
      },
      install_requires=req,
      zip_safe=True
)
