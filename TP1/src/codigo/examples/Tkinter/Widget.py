from BaseWidget import *
from Intermediarios.Pack import *
from Intermediarios.Place import *
from Intermediarios.Grid import *

class Widget(BaseWidget, Pack, Place, Grid):

    def metView():
        print("Widget metView")