# Relevant starting reagent information

REAGENTS = {}

class Reagent():

    def __init__(self,name,manufacturer,purity,form,lot,cas_rn=None,notes=None):
        self.name = name
        self.manufacturer = manufacturer,
        self.purity = purity,
        self.form = form
        self.lot = lot,
        self.cas_rn = cas_rn,
        self.notes = notes

name='Y2O3'
REAGENTS[name] = Reagent(
    name=name,
    manufacturer='Strem Chemicals',
    purity=99.99,
    form='Powder',
    lot='23195800',
    cas_rn='1314-36-9',
    notes='Yttrium Oxide'
        )

name='V2O5'
REAGENTS[name] = Reagent(
    name=name,
    manufacturer='Noah Technologies Corporation',
    purity=99.6,
    form='Powder',
    lot='0198917/2.1',
    cas_rn='1314-62-1',
    notes='Vanadium Oxide'
        )

name='LiCO3'
REAGENTS[name] = Reagent(
    name=name,
    manufacturer='Alfa Aesar',
    purity=99.998,
    form='Powder',
    lot='23765',
    cas_rn='554-13-2',
    notes='Lithium Carbonate, distributed by Puratronic'
        )