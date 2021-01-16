#!/usr/bin/env python3
from math import *

### Classe Solution
"""
Classe permettant de calculer le rang d'une solution dans l'algorithme global.
    - ROI: (float) ROI concernant l'investissement sur une des solutions
    éco-responsables.
    - TRP: (float) TRP conernant l'investissement sur une des solutions 
    éco-responsables
    - Visibilite: (float) Valeur arbitraire attribué à la visibilité d'une
    solution éco-responsable
    -rang: (float) Rang sur vingts que possède la solution
"""
class Solution:
    def __init__(self, ROI, TRP, Visibilite,rang):
        self.ROI = ROI
        self.TRP = TRP
        self.Visibilite = Visibilite
        self.rang = rang
    
    def getROI(self):
        return self.ROI
    
    def getTRP(self):
        return self.TRP
    
    def getRang(self):
        return self.rang
        
    def setVisibilite(self,Visibilite):
        self.Visibilite = Visibilite
    
    def getVisibilite(self):
        return self.Visibilite
    
    #Calcul du rang du ROI sur neuf    
    def calculROI(self,benefAn,coutInvestissement):
        ROI = (benefAn/coutInvestissement)
        self.ROI = round((1/(1+exp((-13*ROI)+5))) * 9,2)
        
    #Calcul du rang du TRP sur neuf
    def calculTRP(self,gainCO2An,coutInvestissement):
        self.TRP = round((gainCO2An/coutInvestissement)*9,2)
    
    def calculRang(self):
        self.rang = self.getROI() + self.getTRP() + self.getVisibilite()


"""
Calcul du rang d'une solution. Le rang = (ROI/9) + (TRP/9) + (Visibilite/2)
"""

def rangSolution(benefAn, coutInvestissement,gainCO2An):
    newSolution = Solution(None,None,None,None)
    newSolution.calculROI(benefAn,coutInvestissement)
    newSolution.calculTRP(gainCO2An,coutInvestissement)
    newSolution.setVisibilite(2)
    newSolution.calculRang()
    return newSolution
        


if __name__ == "__main__":
	A = Solution(None,None,None,None)
	A.calculROI(4000,8000)
	A.calculTRP(800,8000)
	A.setVisibilite(2)
	A.calculRang()
	print(A.getRang())
	B = rangSolution(1000,2000,500)
	print(B.getRang())