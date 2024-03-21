from setuptools import setup, find_packages

setup(
    name="llm_eval",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "llm_eval = llm_eval.main2:main"
        ]
    },
    install_requires=[
        'llm_party',
        'md_jinja',
        'pyyaml'
    ],
)