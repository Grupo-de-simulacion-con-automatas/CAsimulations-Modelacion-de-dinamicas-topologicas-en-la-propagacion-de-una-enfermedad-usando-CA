import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'casimulation',
  version = '1.0.1.5',
  author = 'Jorge Ibañez - Isaac Zainea',
  author_email = 'jonan0804@gmail.com',  
  description = 'Paquete de simulación epidemiológica basada en autómatas celulares',
  url = 'https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN', # use the URL to the github repo
  keywords = ['SIR models', 'Celular automaton','Simulación epidemiológica', 'modelo SIR', 'modelo SIS'],
  packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
