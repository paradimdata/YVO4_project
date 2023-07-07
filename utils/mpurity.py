# Tool to convert molarity of a solution into a %wt

class Solution():

    def __init__(self,mm):
        '''
        Parameters
        Molar Mass: Molar mass of the solution in g/mol
        '''
        self.mm = mm

    def mpurity(self,molarity):
        '''
        Converts molarity to %wt
        Parameters
        Molarity: Molarity of the solution in mol/L
        Assumes a density of 1 g/mL
        '''
        percent_wt = round(((molarity * self.mm) / 10),5)
        return percent_wt
        
SOLNS = {}

name = 'HCl'
SOLNS[name] = Solution(
    mm = 36.46
)

name = 'HNO3'
SOLNS[name] = Solution(
    mm = 63.013
)