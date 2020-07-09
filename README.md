
# pytrnsys : the python TRNSYS Tool-kit 
 
The pytrnsys tool provides basic functionality written in python to run and process, plot and report TRNSYS simulations.
Nevertheless, many functions can be used to process and plot other kind of data such as those extracted from monitoring systems
or exported from other softwares like Polysun.

##### Main developer: 
- Daniel Carbonell : Institut für Solartechnik SPF, Rapperswil, Switzerland.
- To be able to commit contact : dani.carbonell@spf.ch
##### Collaborators:
- Mattia Battaglia : Institut für Solartechnik SPF, Rapperswil, Switzerland.
- Jeremias Schmidli : Institut für Solartechnik SPF, Rapperswil, Switzerland.

This code was not initially developed with the intention to be shared with others, 
but after realizing that it could help the community to have a better workflow with TRNSYS 
we decided to share it. Currently this code is in testing phase under the European project 
TRI-HP with Grant Agreement No. 81488. 
 
## Aknowledgements
 
A first version of this package was first created in 2013 and since then it has evolved considerably. 
We would like to thank the Swiss Federal Office Of Energy (SFOE) 
who supported many projects related to simulations of renewable energy systems where this code has been developed. We would also like to thank the European Union’s Horizon 2020 research and innovation programme
We also would like to tank the EU Commission for the funding received in TRI-HP under the Grant Agreement No.  81488. 
This project allowed to decicate efforts in sharing the code with the consortium and to make the code usable for the others.  

  
## Installation of python 3.5 and needed libraries

- Install python 3.5 with numpy, scipy, matplotlib and pandas and Tk
    - in conda enviroment you can 
- CoolProp package is nedded if physical properties of fluids need to be used, otherwise it's not mandatory
- We recommend to install anaconda with default installation packages
- Choose the python editor you like, such as PyCharm, Spyder or alike. This readme file is automatically processed by PyCharm in a html visual style   

## Installation of LaTeX for reporting
- For all processing cases, a pdf made with LaTeX will be generated.
Therefore LaTeX is highly recommended. We suggest MiKTeX, but other packages can be used.
- In order to use the LaTeX class for preparing the pdf, the enviromental variables 
  that tell LaTeX where to find local files need to  be specified
- Create an enviromental variable named TEXINPUTS and give a path to it 

```
TEXINPUTS => ....\pytrnsys\pytrnsys\reporting\latex_doc
```
 
## Activate the import of the spfPythonTool package into python environment


- Modify the pytrnsysPath.pth file according to your paths 
- Copy the pytrnsysPath.pth this file to ...\Lib\site-packages. 

For example copy the pytrnsysPath.pth to: 
```
...\Users\dcarbone\AppData\Local\Continuum\anaconda2\Lib\site-packages
```



