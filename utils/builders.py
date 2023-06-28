# Tools to build GEMD object specs

### Imports ###

from gemd import ProcessSpec,MaterialSpec,IngredientSpec
from gemd.entity.value import NominalCategorical, NominalReal, UniformReal, NormalReal
from gemd.entity.attribute import Property, Parameter, Condition, PropertyAndConditions


from templates.attribute_templates import ATTR_TEMPL
from templates.object_templates import OBJ_TEMPL

### Process Spec Builders ###

PROCESS_SPECS = {}

def build_chunking_material_proc_spec():
    pass

def build_dissolving_material_proc_spec():
    pass

def build_filter_solution_proc_spec():
    pass

def build_grinding_material_proc_spec():
    pass

def build_heating_material_proc_spec():
    pass

def build_pressing_material_proc_spec():
    pass

def build_acquire_raw_material_proc_spec(name,manufacturer,lot_id,cas_rn):
    '''
    Builds a process spec for acquiring a new material.

    ### Parameters

    Name: Name of the Process, must be the same as associated material and ingredient
        ex: 'YVO4'
    Manufacturer: Manufacturer of the material purchased
        ex: 'Alfa Aesar', 'Thermo Scientific' 
    Lot ID: Lot ID  of the purchased material
        ex: 'W19F006','R10H008'
    CAS RN: CAS Registry Number of the purchased material

    '''
    PROCESS_SPECS[f'Purchasing {name} Spec'] = ProcessSpec(
        name=f'Purchasing {name} Spec',
        template=OBJ_TEMPL['Purchasing Raw Material'],
        parameters=[
            Parameter(name='Manufacturer',
                template=ATTR_TEMPL['Manufacturer'],
                value=NominalCategorical(manufacturer)
                ),
            Parameter(name='Lot ID',
                template=ATTR_TEMPL['Lot ID'],
                value=NominalCategorical(lot_id)
                ),
            Parameter(name='CAS RN',
                template=ATTR_TEMPL['CAS RN'],
                value=NominalCategorical(cas_rn)
                )
        ]
    )

    return PROCESS_SPECS[f'Purchasing {name} Spec']

def build_quenching_tube_proc_spec():
    pass

def build_sealing_vessel_proc_spec():
    pass

def build_setting_pellets_proc_spec():
    pass

### Material Spec Builders ###

MATERIAL_SPECS = {}

def build_chunked_material_mat_spec():
    pass

def build_ground_material_mat_spec():
    pass

def build_heated_material_mat_spec():
    pass

def build_pressed_material_mat_spec():
    pass

def build_raw_material_mat_spec(name,form,purity):
    '''
    Builds a material spec for a Raw Material.

    ### Parameters

    Name: Name of the Ingredient, must be the same as associated process and ingredient
        ex: 'YVO4'
    Form: Physical form of the ingredient
        ex: 'Powder', 'Rod'
    Purity: Purity of the material as a percent
        ex: 99.996

    '''
    MATERIAL_SPECS[f'{name} Material Spec'] = MaterialSpec(
        name=f'{name} Material Spec',
        template=OBJ_TEMPL['Raw Material'],
        process=PROCESS_SPECS[f'Purchasing {name} Spec'],
        properties=[
            Property(
                name='Purity Percentage',
                template=ATTR_TEMPL['Purity Percentage'],
                value=NominalReal(purity,'')
                ),
            Property(
                name='Form',
                template=ATTR_TEMPL['Form'],
                value=NominalCategorical(form)
            )
        ]
    )

            
    return MATERIAL_SPECS[f'{name} Material Spec']

def build_solution_material_mat_spec():
    pass

### Ingredient Spec Builders ###

INGREDIENT_SPECS = {}

def build_ingredient_spec(name,quantity,unc,units):
    '''
    Builds an ingredient spec.

    ### Parameters

    Name: Name of the Ingredient, must be the same as associated process and materials
        ex: 'YVO4'
    Quantity: Amount of ingredient produced from a material
        ex: 12.3
    Uncertainty: Uncertainty in the amount, usually from instrument precision
        ex: 0.1
    Units: Units of quantity 
        ex: g, mL, mm
    '''
    INGREDIENT_SPECS[f'{name} Ingredient Spec'] = IngredientSpec(
        name=f'{name} Ingredient Spec',
        process=PROCESS_SPECS[f'Purchasing {name} Spec'],
        material=MATERIAL_SPECS[f'{name} Material Spec'],
        absolute_quantity=UniformReal(
                            lower_bound=quantity-unc,
                            upper_bound=quantity+unc,
                            units=units
        )
    )

    return INGREDIENT_SPECS[f'{name} Ingredient Spec']

### Measurement Spec Builders ###

def build_temperature_meas_spec():
    pass

def build_xrd_meas_spec():
    pass


my_proccess = build_acquire_raw_material_proc_spec(
    name='V2O5',
    manufacturer='Alfa Aesar',
    lot_id='W19F006',
    cas_rn=''
)

my_material = build_raw_material_mat_spec(
    name='V2O5',
    form='Powder',
    purity=54.66
)

my_ingredients = [build_ingredient_spec(
    name='V2O5',
    quantity=10.0,
    unc=0.1,
    units='g'
    )
]