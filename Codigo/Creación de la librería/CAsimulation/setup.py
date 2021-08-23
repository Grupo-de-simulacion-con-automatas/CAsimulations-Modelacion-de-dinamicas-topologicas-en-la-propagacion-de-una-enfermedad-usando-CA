import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'casimulation',
  version = '0.0.0.1',
  author = 'Jorge Ibañez - Isaac Zainea',
  author_email = 'jibanezh@ucentral.edu.co',  
  description = 'Paquete de simulación epidemiológica basada en autómatas celulares',
  url = 'https://github.com/Grupo-de-simulacion-con-automatas/CAsimulations', # use the URL to the github repo
  keywords = ['SIR models', 'Celular automaton'],
  packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
