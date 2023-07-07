# Tools to build GEMD object specs

### Imports ###

from gemd import ProcessSpec,MaterialSpec,IngredientSpec,MeasurementSpec
from gemd.entity.value import NominalCategorical, NominalReal, UniformReal, NormalReal
from gemd.entity.attribute import Property, Parameter, Condition, PropertyAndConditions

from utils.templates.attribute_templates import ATTR_TEMPL
from utils.templates.object_templates import OBJ_TEMPL

import json
from utils.templates.attribute_templates import config,file_path

### Validate Attributes ###

def save_config(config):
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=2)

def attr_validate(attr,value):
    '''
    Validates that a categorical value exists and adds it to the attribute bounds config if requested.
    '''
    if value not in config['BOUNDS'][attr]['categories']:
        confirm = input(f'{value} does not exist in category {attr}. Would you like to add it? (y/n)')
        if confirm.lower() == 'y':
            config['BOUNDS'][attr]['categories'].append(value)
            print(f'Added {value} to category {attr}.')
            save_config(config)
        elif confirm.lower() == 'n':
            print(f'Please choose a different value for {attr}')
            return
        else:
            raise ValueError('Invalid response. Please answer y/n.')
    else:
        pass

### Process Spec Builders ###

PROCESS_SPECS = {}

def build_chunking_material_proc_spec():
    pass

def build_dissolving_material_proc_spec():
    pass

def build_filter_solution_proc_spec():
    pass

def build_grinding_material_proc_spec(name,location,equipment='Mortar and Pestle',notes=None):
    '''
    Builds a process spec for grinding a material.

    ### Parameters

    Name: Name of the Process, must be the same as associated material and ingredient
        ex: 'YVO4'
    Location: Location where a process was performed
        ex: 'Synthesis Tube Furnace', 'X-Ray Diffraction Panel'
    Equipment: Equipment used to perform an action. Default is mortar and pestle.
        ex: 'Mortar and Pestle'

    '''
    attr_validate('Equipment Used',equipment)
    attr_validate('Location',location)

    PROCESS_SPECS[f'Grinding {name} Spec'] = ProcessSpec(
        name=f'Grinding {name} Spec',
        template=OBJ_TEMPL['Grinding Material'],
        parameters=[
            Parameter(
                name='Equipment Used',
                template=ATTR_TEMPL['Equipment Used'],
                value=NominalCategorical(equipment)
                    )
                ],
        conditions=[
            Condition(
                name='Location',
                template=ATTR_TEMPL['Location'],
                value=NominalCategorical(location)
                    )
                ],
        notes=notes
    )

    return PROCESS_SPECS[f'Grinding {name} Spec']

def build_heating_material_proc_spec(name,temperature,rate,duration,location,notes=None):
    '''
    Builds a process spec for heating a material.

    ### Parameters

    Name: Name of the Process, must be the same as associated material and ingredient
        ex: 'YVO4'
    Temperature: Holding temperature of the heating process in degC
        ex: 750.
    Rate: The ramp rate in degC/hr of the heating/cooling of the material.
        ex: 100.
    Duration: Duration of the heating process in hours
        ex: 10.
    Location: Location where a process was performed
        ex: 'Synthesis Tube Furnace', 'X-Ray Diffraction Panel'

    '''
    attr_validate('Location',location)

    PROCESS_SPECS[f'Heating {name} Spec'] = ProcessSpec(
        name=f'Heating {name} Spec',
        template=OBJ_TEMPL['Heating Material'],
        parameters=[
            Parameter(
                name='Furnace Temperature',
                template=ATTR_TEMPL['Furnace Temperature'],
                value=NominalReal(temperature,'degC')
                    ),
            Parameter(
                name='Furnace Rate',
                template=ATTR_TEMPL['Furnace Rate'],
                value=NominalReal(rate,'degC')
                    ),
            Parameter(
                name='Duration',
                template=ATTR_TEMPL['Duration'],
                value=NominalReal(duration,'hr')
                    )
                ],
        conditions=[Condition(
                name='Location',
                template=ATTR_TEMPL['Location'],
                value=NominalCategorical(location)
                    ) 
                ],   
        notes=notes
    )

    return PROCESS_SPECS[f'Heating {name} Spec']

def build_ldfz_material_proc_spec(name,power,rate,duration,atmosphere,location,notes=None):
    '''
    Builds a process spec for heating a material.

    ### Parameters

    Name: Name of the Process, must be the same as associated material and ingredient
        ex: 'YVO4'
    Temperature: Holding temperature of the heating process in degC
        ex: 750.
    Rate: The ramp rate in degC/hr of the heating/cooling of the material.
        ex: 100.
    Duration: Duration of the heating process in hours
        ex: 10.
    Location: Location where a process was performed
        ex: 'Synthesis Tube Furnace', 'X-Ray Diffraction Panel'

    '''
    attr_validate('Location',location)
    attr_validate('Atmosphere',atmosphere)

    PROCESS_SPECS[f'LDFZ {name} Spec'] = ProcessSpec(
        name=f'LDFZ {name} Spec',
        template=OBJ_TEMPL['LDFZ Material'],
        parameters=[
            Parameter(
                name='Laser Power',
                template=ATTR_TEMPL['Laser Power'],
                value=NominalReal(power,'')
                    ),
            Parameter(
                name='Laser Rate',
                template=ATTR_TEMPL['Laser Rate'],
                value=NominalReal(rate,'')
                    ),
            Parameter(
                name='Duration',
                template=ATTR_TEMPL['Duration'],
                value=NominalReal(duration,'hr')
            )
                ],
        conditions=[
            PropertyAndConditions(
            Condition(
                name='Location',
                template=ATTR_TEMPL['Location'],
                value=NominalCategorical(location)
                    )
                ),
            PropertyAndConditions(
            Condition(
                name='Atmosphere',
                template=ATTR_TEMPL['Atmosphere'],
                value=NominalCategorical(atmosphere)
                    )
                )   
            ],   
        notes=notes
    )

    return PROCESS_SPECS[f'Purchasing {name} Spec']

def build_pressing_material_proc_spec():
    pass

def build_acquire_raw_material_proc_spec(name,manufacturer,lot_id,cas_rn=None,notes=None):
    '''
    Builds a process spec for acquiring a new material.

    ### Parameters

    Name: Name of the Process, must be the same as associated material and ingredient
        ex: 'YVO4'
    Manufacturer: The manufacturer from which the material was purchased
        ex: 'Thermo Scientific'
    Lot ID: Lot ID of the purchased material
        ex: '2134WX'
    CAS RN: CAS registry number of the purchased material (Optional)
        ex: '123-45-678'
    ''' 
    attr_validate('Manufacturer',manufacturer)
    attr_validate('Lot ID',lot_id)
    attr_validate('CAS RN',cas_rn)

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
        ],
        notes=notes
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

def build_ground_material_mat_spec(name,form='Powder',notes=None):
    '''
    Builds a material spec for a Ground Material.

    ### Parameters

    Name: Name of the Ingredient, must be the same as associated process and ingredient
        ex: 'YVO4'
    Form: Physical form of the ingredient. The default for ground materials is powder.
        ex: 'Powder', 'Rod'

    '''
    attr_validate('Form',form)

    MATERIAL_SPECS[f'{name} Material Spec'] = MaterialSpec(
        name=f'{name} Material Spec',
        template=OBJ_TEMPL['Ground Material'],
        process=PROCESS_SPECS[f'Grinding {name} Spec'],
        properties=[
            PropertyAndConditions(
                property=Property(
                name='Form',
                template=ATTR_TEMPL['Form'],
                value=NominalCategorical(form)
                )
            )
        ],
        notes=notes
    )

    return MATERIAL_SPECS[f'{name} Material Spec']

def build_heated_material_mat_spec(name,form,notes=None):
    '''
    Builds a material spec for a Ground Material.

    ### Parameters

    Name: Name of the Ingredient, must be the same as associated process and ingredient
        ex: 'YVO4'
    Form: Physical form of the ingredient. 
        ex: 'Powder', 'Rod'

    '''
    attr_validate('Form',form)

    MATERIAL_SPECS[f'{name} Material Spec'] = MaterialSpec(
        name=f'{name} Material Spec',
        template=OBJ_TEMPL['Heated Material'],
        process=PROCESS_SPECS[f'Heating {name} Spec'],
        properties=[
            PropertyAndConditions(
                property=Property(
                name='Form',
                template=ATTR_TEMPL['Form'],
                value=NominalCategorical(form)
                )
            )
        ],
        notes=notes
    )

    return MATERIAL_SPECS[f'{name} Material Spec']

def build_pressed_material_mat_spec():
    pass

def build_raw_material_mat_spec(name,form,purity,notes=None):
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
    attr_validate('Form',form)

    MATERIAL_SPECS[f'{name} Material Spec'] = MaterialSpec(
        name=f'{name} Material Spec',
        template=OBJ_TEMPL['Raw Material'],
        process=PROCESS_SPECS[f'Purchasing {name} Spec'],
        properties=[
            PropertyAndConditions(
                property=Property(
                name='Form',
                template=ATTR_TEMPL['Form'],
                value=NominalCategorical(form)
                    )
                ),
                    PropertyAndConditions(
                property=Property(
                name='Purity Percentage',
                template=ATTR_TEMPL['Purity Percentage'],
                value=NominalReal(purity,'')
                )
            )
        ],
        notes=notes
    )

            
    return MATERIAL_SPECS[f'{name} Material Spec']

def build_solution_material_mat_spec():
    pass

### Ingredient Spec Builders ###

INGREDIENT_SPECS = {}

def build_ingredient_spec(name,process,material,quantity,notes=None):
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
        process=process,
        material=material,
        absolute_quantity=quantity,
        notes=notes
    )

    return INGREDIENT_SPECS[f'{name} Ingredient Spec']

### Measurement Spec Builders ###

MEASUREMENT_SPECS = {}

def build_temperature_meas_spec():
    pass

def build_xrd_meas_spec(name,duration,range,adhesive,location='X-Ray Diffraction Panel',file=None,notes=None):
    '''
    Builds a measurement spec for X-Ray Diffraction

    ### Parameters

    Name: Name of the Measurement, must be the same as associated material and ingredient
        ex: 'YVO4'
    Duration: Duraiton of the XRD measurement in hours.
        ex: 0.25
    Range: Range of 2theta in degrees.
        ex: '15-60'
    Adhesive: The adhesive used to prepare a sample for XRD
        ex: 'Vaseline', 'Ethanol'
    Location: Location in which the measurement was taken. Default is XRD Panel.
        ex: 'XRD Panel'
    '''
    attr_validate('Location',location)
    attr_validate('XRD Adhesive',adhesive)

    MEASUREMENT_SPECS[f'{name} XRD Measurement Spec'] = MeasurementSpec(
        name=f'{name} XRD Measurement Spec',
        template=OBJ_TEMPL['X-Ray Diffraction'],
        parameters=[
            Parameter(
                name='Duration',
                template=ATTR_TEMPL['Duration'],
                value=NominalReal(duration,'hr')
                    ),
            Parameter(
                name='XRD Range',
                template=ATTR_TEMPL['XRD Range'],
                value=NominalCategorical(range)
                    ),
            Parameter(
                name='XRD Adhesive',
                template=ATTR_TEMPL['XRD Adhesive'],
                value=NominalCategorical(adhesive)
                    )
                ],
        conditions=[Condition(
                    name='Location',
                    template=ATTR_TEMPL['Location'],
                    value=NominalCategorical(location)
                )
            ],
        file_links=file,
        notes=notes
    )

    return MEASUREMENT_SPECS[f'{name} XRD Measurement Spec']