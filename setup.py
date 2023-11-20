from setuptools import setup, find_packages

setup(
    name='pcase',
    version='0.0.1',
    description='A tool for generate test csse',
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=["pcase"],
    include_package_data=False,
    install_requires=[
        "pyDOE2>=1.3.0",
        "xlrd>=2.0.1",
        "xlwt>=1.3.0",
    ],
    # 这样配置生成可执行脚本，caseCreate.py中 具体定义的主函数名称
    # entry_points={
    #     'console_scripts': [
    #         'hat = pcase.caseCreate:sample',
    #     ],
    # },
)