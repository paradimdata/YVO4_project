# Tools to build GEMD object specs

### Imports ###

from gemd import ProcessSpec,MaterialSpec,IngredientSpec,MeasurementSpec,FileLink
from gemd.entity.value import NominalCategorical, NominalReal, UniformReal, NormalReal, NominalComposition, NominalInteger
from gemd.entity.attribute import Property, Parameter, Condition, PropertyAndConditions

from utils.templates.attribute_templates import ATTR_TEMPL
from utils.templates.object_templates import OBJ_TEMPL

import json
from utils.templates.attribute_templates import config,file_path

### Validate Attributes ###

def save_config(config):
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=2)

def attr_validate(attr:str,value):
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

def build_dissolving_material_proc_spec(name:str,location:str,equipment:str,tags:list=[],notes:str=None):
    '''
    Builds a process spec for dissolving a material.

    ### Parameters

    Name: Name of the Process, must be the same as associated material and ingredient
        ex: 'YVO4'
    Location: Location where a process was performed
        ex: 'Synthesis Tube Furnace', 'X-Ray Diffraction Panel'
    Equipment: Equipment used to perform an action. In this case it is the vessel in which it is dissolved
        ex: 'Mortar and Pestle'

    '''
    attr_validate('Equipment Used',equipment)
    attr_validate('Location',location)

    PROCESS_SPECS[f'Dissolving {name} Spec'] = ProcessSpec(
        name=f'Dissolving {name} Spec',
        template=OBJ_TEMPL['Dissolving Material'],
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
        tags=tags,
        notes=notes
    )

    return PROCESS_SPECS[f'Dissolving {name} Spec']

def build_filtering_material_proc_spec(name:str,location:str='Wet Lab',equipment:str='Vacuum Filter',solvent:str=None,tags:list=[],notes:str=None):
    '''
    Builds a process spec for filtering a material.

    ### Parameters

    Name: Name of the Process, must be the same as associated material and ingredient
        ex: 'YVO4'
    Location: Location where a process was performed. The default is 'Wet Lab'
        ex: 'Synthesis Tube Furnace', 'X-Ray Diffraction Panel'
    Equipment: Equipment used to perform an action. The default is 'vacuum filter'.
        ex: 'Mortar and Pestle'
    Solvent: Solvent used to wash/dissolve during the filtration (Optional).
        ex: 'Water', 'Ethanol'

    '''
    attr_validate('Equipment Used',equipment)
    attr_validate('Location',location)
    attr_validate('Solvent',solvent)

    PROCESS_SPECS[f'Filtering {name} Spec'] = ProcessSpec(
        name=f'Filtering {name} Spec',
        template=OBJ_TEMPL['Filtering Material'],
        parameters=[
            Parameter(
                name='Equipment Used',
                template=ATTR_TEMPL['Equipment Used'],
                value=NominalCategorical(equipment)
                    ),
            Parameter(
                name='Solvent',
                template=ATTR_TEMPL['Solvent'],
                value=NominalCategorical(solvent)
                    )
                ],
        conditions=[
            Condition(
                name='Location',
                template=ATTR_TEMPL['Location'],
                value=NominalCategorical(location)
                    )
                ],
        tags=tags,
        notes=notes
    )

    return PROCESS_SPECS[f'Filtering {name} Spec']

def build_grinding_material_proc_spec(name:str,location:str,equipment:str='Mortar and Pestle',tags:list=[],notes:str=None):
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
        tags=tags,
        notes=notes
    )

    return PROCESS_SPECS[f'Grinding {name} Spec']

"""
Newer version below with dynamic step input

def build_heating_material_proc_spec(name:str,temperature:str,rate:float,duration:float,location:str,notes:str=None):
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
"""

def heating_program_step(type:str,temp:float,duration:float):
    '''
    Type: The type of heating step. 
        ex: 'Init','Ramp','Hold','End'
    Temp: The target end temperature of a ramp or the temperature maintained during a hold. Enter 0 for 'Init' or 'End' type steps. (degC)
        ex: 250
    Duration: Duration of the ramp or hold in hours.
        ex: 24, 6.5
    '''
    return (type,temp,duration)

def build_heating_program(program:list[tuple]):
    '''
    Argument should be a list of heating_program_step() functions.
    '''

    PROGRAM = []
    i = 0

    for step in program:
        PROGRAM.append(
            {
            'Type':step[0],
            'Temp':step[1],
            'Duration':step[2]
            }
        )

        attr_validate('Step Type',PROGRAM[i]['Type'])
        
        i += 1
    
    return PROGRAM

def build_heating_material_proc_spec(name:str,program:list[dict],location:str='Hot Lab',tags:list=[],notes:str=None):

    '''
    Dynamically builds a process spec for heating a material in a multi-step temperature program.

    ### Parameters

    Name: Name of the Process, must be the same as associated material and ingredient
        ex: 'YVO4'
    Steps: An integer number of steps in the temperature program.
        ex: 3
    Location: Location where a process was performed. Default is 'Hot Lab'
        ex: 'Hot Lab' 'Synthesis Tube Furnace', 'X-Ray Diffraction Panel'.
    '''

    attr_validate('Location',location)

    PROCESS_SPECS[f'Heating {name} Spec'] = ProcessSpec(
        name=f'Heating {name} Spec',
        template=OBJ_TEMPL['Improved Heating Material'],
        parameters=[],
        conditions=[Condition(
                name='Location',
                template=ATTR_TEMPL['Location'],
                value=NominalCategorical(location)
                    ) 
                ],   
        tags=tags,
        notes=notes
    )

    i = 0

    for step in program:

        PROCESS_SPECS[f'Heating {name} Spec'].parameters.append(Parameter(
            name=f'Step {i+1}',
            template=ATTR_TEMPL['Step'],
            value=NominalComposition(
                quantities=program[i]
                )
            )
        )

        i += 1

    return PROCESS_SPECS[f'Heating {name} Spec']    

def ldfz_program_step(type:str,power:float,duration:float,rotation:tuple,rate:float,tags:list=[],notes:str=None):
    '''
    Type: The type of heating step. 
        ex: 'Init','Ramp','Hold','End'
    Temp: The target end temperature of a ramp or the temperature maintained during a hold. Enter 0 for 'Init' or 'End' type steps. (degC)
        ex: 250
    Duration: Duration of the ramp or hold in hours.
        ex: 24, 6.5
    '''
    return (type,power,rotation,rate,duration,notes)

def build_ldfz_program(program:list[tuple]):
    '''
    Argument should be a list of heating_program_step() functions.
    '''

    PROGRAM = []
    i = 0

    for step in program:
        PROGRAM.append(
            {
            'Type':step[0],
            'Power':step[1],
            'Rotation':step[2],
            'Rate':step[3],
            'Duration':step[4],
            'Notes':step[5]
            }
        )

        attr_validate('Step Type',PROGRAM[i]['Type'])
        
        i += 1
    
    return PROGRAM

def build_ldfz_proc_spec(name:str,program:list[dict],atmosphere,location:str='PARADIM',tags:list=[],notes:str=None):
    '''
    Dynamically builds a process spec for heating a material in a multi-step temperature program.

    ### Parameters

    Name: Name of the Process, must be the same as associated material and ingredient
        ex: 'YVO4'
    Steps: An integer number of steps in the temperature program.
        ex: 3
    Location: Location where a process was performed. Default is 'Hot Lab'
        ex: 'Hot Lab' 'Synthesis Tube Furnace', 'X-Ray Diffraction Panel'.
    '''
    attr_validate('Location',location),
    attr_validate('Atmosphere',atmosphere)

    PROCESS_SPECS[f'LDFZ {name} Spec'] = ProcessSpec(
        name=f'LDFZ {name} Spec',
        template=OBJ_TEMPL['LDFZ Material'],
        parameters=[],
        conditions=[Condition(
                name='Location',
                template=ATTR_TEMPL['Location'],
                value=NominalCategorical(location)
                    ),
                    Condition(
                name='Atmosphere',
                template=ATTR_TEMPL['Atmosphere'],
                value=NominalCategorical(atmosphere)
                    )
                ],   
        tags=tags,
        notes=notes
    )

    i = 0

    for step in program:

        PROCESS_SPECS[f'LDFZ {name} Spec'].parameters.append(Parameter(
            name=f'Step {i+1}',
            template=ATTR_TEMPL['Step'],
            value=NominalComposition(
                quantities=program[i]
                )
            )
        )

        i += 1

    return PROCESS_SPECS[f'LDFZ {name} Spec'] 

def build_pressing_material_proc_spec(name:str,equipment:str,pressure,duration:float,location:str,tags:list=[],notes:str=None):
    '''
    Builds a process spec for filtering a material.

    ### Parameters

    Name: Name of the Process, must be the same as associated material and ingredient
        ex: 'YVO4'
    Location: Location where a process was performed. The default is 'Wet Lab'
        ex: 'Synthesis Tube Furnace', 'X-Ray Diffraction Panel'
    Equipment: Equipment used to perform an action. The default is 'vacuum filter'.
        ex: 'Mortar and Pestle'
    Solvent: Solvent used to wash/dissolve during the filtration (Optional).
        ex: 'Water', 'Ethanol'

    '''
    attr_validate('Equipment Used',equipment)
    attr_validate('Location',location)

    PROCESS_SPECS[f'Pressing {name} Spec'] = ProcessSpec(
        name=f'Pressing {name} Spec',
        template=OBJ_TEMPL['Pressing Material'],
        parameters=[
            Parameter(
                name='Equipment Used',
                template=ATTR_TEMPL['Equipment Used'],
                value=NominalCategorical(equipment)
                    ),
            Parameter(
                name='Duration',
                template=ATTR_TEMPL['Duration'],
                value=NominalReal(duration,'hr')
                ),
            Parameter(
                name='Pressure',
                template=ATTR_TEMPL['Pressure'],
                value=NominalReal(pressure,'MPa')
            )
                ],
        conditions=[
            Condition(
                name='Location',
                template=ATTR_TEMPL['Location'],
                value=NominalCategorical(location)
                    )
                ],
        tags=tags,
        notes=notes
    )

    return PROCESS_SPECS[f'Pressing {name} Spec']

def build_evacuating_proc_spec(name:str,equipment:str,duration:float,location:str,tags:list=[],notes:str=None):
    '''
    Builds a process spec for putting a material under vacuum.

    ### Parameters

    Name: Name of the Process, must be the same as associated material and ingredient
        ex: 'YVO4'
    Location: Location where a process was performed. The default is 'Wet Lab'
        ex: 'Synthesis Tube Furnace', 'X-Ray Diffraction Panel'
    Equipment: Equipment used to perform an action. The default is 'vacuum filter'.
        ex: 'Mortar and Pestle'

    '''
    attr_validate('Equipment Used',equipment)
    attr_validate('Location',location)

    PROCESS_SPECS[f'Evacuating {name} Spec'] = ProcessSpec(
        name=f'Evacuating {name} Spec',
        template=OBJ_TEMPL['Evacuating Material'],
        parameters=[
            Parameter(
                name='Equipment Used',
                template=ATTR_TEMPL['Equipment Used'],
                value=NominalCategorical(equipment)
                    ),
            Parameter(
                name='Duration',
                template=ATTR_TEMPL['Duration'],
                value=NominalReal(duration,'hr')
                )
                ],
        conditions=[
            Condition(
                name='Location',
                template=ATTR_TEMPL['Location'],
                value=NominalCategorical(location)
                    )
                ],
        tags=tags,
        notes=notes
    )

    return PROCESS_SPECS[f'Evacuating {name} Spec']

def build_acquire_raw_material_proc_spec(name:str,manufacturer:str,lot_id:str,cas_rn:str=None,tags:list=[],notes:str=None):
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
        tags=tags,
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

def build_filtered_material_mat_spec(name:str,form:str,process:ProcessSpec,tags:list=[],notes:str=None):
    '''
    Builds a material spec for a Ground Material.

    ### Parameters

    Name: Name of the Ingredient, must be the same as associated process and ingredient
        ex: 'YVO4'
    Form: Physical form of the ingredient. 
        ex: 'Powder', 'Rod'
    '''
    attr_validate('Form',form)

    MATERIAL_SPECS[f'{name} Filtered Material Spec'] = MaterialSpec(
        name=f'{name} Filtered Material Spec',
        template=OBJ_TEMPL['Filtered Material'],
        process=process,
        properties=[
            PropertyAndConditions(
                property=Property(
                name='Form',
                template=ATTR_TEMPL['Form'],
                value=NominalCategorical(form)
                )
            )
        ],
        tags=tags,
        notes=notes
    )

    return MATERIAL_SPECS[f'{name} Filtered Material Spec']

def build_ground_material_mat_spec(name:str,process_spec:ProcessSpec,form:str='Powder',tags:list=[],notes:str=None):
    '''
    Builds a material spec for a Ground Material.

    ### Parameters

    Name: Name of the Ingredient, must be the same as associated process and ingredient
        ex: 'YVO4'
    Form: Physical form of the ingredient. The default for ground materials is powder.
        ex: 'Powder', 'Rod'

    '''
    attr_validate('Form',form)

    MATERIAL_SPECS[f'{name} Ground Material Spec'] = MaterialSpec(
        name=f'{name} Ground Material Spec',
        template=OBJ_TEMPL['Ground Material'],
        properties=[
            PropertyAndConditions(
                property=Property(
                name='Form',
                template=ATTR_TEMPL['Form'],
                value=NominalCategorical(form)
                )
            )
        ],
        process=process_spec,
        tags=tags,
        notes=notes
    )

    return MATERIAL_SPECS[f'{name} Ground Material Spec']

def build_heated_material_mat_spec(name:str,form:str,process:ProcessSpec,tags:list=[],notes:str=None):
    '''
    Builds a material spec for a Ground Material.

    ### Parameters

    Name: Name of the Ingredient, must be the same as associated process and ingredient
        ex: 'YVO4'
    Form: Physical form of the ingredient. 
        ex: 'Powder', 'Rod'

    '''
    attr_validate('Form',form)

    MATERIAL_SPECS[f'{name} Heated Material Spec'] = MaterialSpec(
        name=f'{name} Heated Material Spec',
        template=OBJ_TEMPL['Heated Material'],
        process=process,
        properties=[
            PropertyAndConditions(
                property=Property(
                name='Form',
                template=ATTR_TEMPL['Form'],
                value=NominalCategorical(form)
                )
            )
        ],
        tags=tags,
        notes=notes
    )

    return MATERIAL_SPECS[f'{name} Heated Material Spec']

def build_pressed_material_mat_spec(name:str,form:str,process:ProcessSpec,tags:list=[],notes:str=None):
    '''
    Builds a material spec for a pressed Material.

    ### Parameters

    Name: Name of the Ingredient, must be the same as associated process and ingredient
        ex: 'YVO4'
    Form: Physical form of the ingredient. 
        ex: 'Powder', 'Rod'

    '''
    attr_validate('Form',form)

    MATERIAL_SPECS[f'{name} Pressed Material Spec'] = MaterialSpec(
        name=f'{name} Pressed  Material Spec',
        template=OBJ_TEMPL['Pressed Material'],
        process=process,
        properties=[
            PropertyAndConditions(
                property=Property(
                name='Form',
                template=ATTR_TEMPL['Form'],
                value=NominalCategorical(form)
                )
            )
        ],
        tags=tags,
        notes=notes
    )

    return MATERIAL_SPECS[f'{name} Pressed Material Spec']

def build_evacuated_material_mat_spec(name:str,form:str,process:ProcessSpec,tags:list=[],notes:str=None):
    '''
    Builds a material spec for a pressed Material.

    ### Parameters

    Name: Name of the Ingredient, must be the same as associated process and ingredient
        ex: 'YVO4'
    Form: Physical form of the ingredient. 
        ex: 'Powder', 'Rod'

    '''
    attr_validate('Form',form)

    MATERIAL_SPECS[f'{name} Evacuated Material Spec'] = MaterialSpec(
        name=f'{name} Evacuated  Material Spec',
        template=OBJ_TEMPL['Evacuated Material'],
        process=process,
        properties=[
            PropertyAndConditions(
                property=Property(
                name='Form',
                template=ATTR_TEMPL['Form'],
                value=NominalCategorical(form)
                )
            )
        ],
        tags=tags,
        notes=notes
    )

    return MATERIAL_SPECS[f'{name} Evacuated Material Spec']

def build_raw_material_mat_spec(name:str,form:str,purity:float,tags:list=[],notes:str=None):
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

    MATERIAL_SPECS[f'{name} Raw Material Spec'] = MaterialSpec(
        name=f'{name} Raw Material Spec',
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
        tags=tags,
        notes=notes
    )

            
    return MATERIAL_SPECS[f'{name} Raw Material Spec']

def build_dissolved_material_mat_spec(name:str,form:str='Solution',process:ProcessSpec=None,tags:list=[],notes:str=None):
    '''
    Builds a material spec for a dissolved Material (solution).

    ### Parameters

    Name: Name of the Ingredient, must be the same as associated process and ingredient
        ex: 'YVO4'
    Form: Physical form of the ingredient. Default is 'Solution' 
        ex: 'Powder', 'Rod'

    '''
    attr_validate('Form',form)

    MATERIAL_SPECS[f'{name} Dissolved Material Spec'] = MaterialSpec(
        name=f'{name} Dissolved Material Spec',
        template=OBJ_TEMPL['Solution Material'],
        process=process,
        properties=[
            PropertyAndConditions(
                property=Property(
                name='Form',
                template=ATTR_TEMPL['Form'],
                value=NominalCategorical(form)
                )
            )
        ],
        tags=tags,
        notes=notes
    )

    return MATERIAL_SPECS[f'{name} Dissolved Material Spec']

def build_terminal_material_spec(name:str,form:str,process:ProcessSpec,tags:list=[],notes:str=None):
    '''
    Builds a material spec for a pressed Material.

    ### Parameters

    Name: Name of the Ingredient, must be the same as associated process and ingredient
        ex: 'YVO4'
    Form: Physical form of the ingredient. 
        ex: 'Powder', 'Rod'

    '''
    attr_validate('Form',form)

    MATERIAL_SPECS[f'{name} Terminal Material Spec'] = MaterialSpec(
        name=f'{name} Terminal Material Spec',
        template=OBJ_TEMPL['Terminal Material'],
        process=process,
        properties=[
            PropertyAndConditions(
                property=Property(
                name='Form',
                template=ATTR_TEMPL['Form'],
                value=NominalCategorical(form)
                )
            )
        ],
        tags=tags,
        notes=notes
    )

    return MATERIAL_SPECS[f'{name} Terminal Material Spec']

def build_ldfz_material_spec(name:str,form:str,process:ProcessSpec,tags:list=[],notes:str=None):
    '''
    Builds a material spec for a Material grown in an LDFZ.

    ### Parameters

    Name: Name of the Ingredient, must be the same as associated process and ingredient
        ex: 'YVO4'
    Form: Physical form of the ingredient. 
        ex: 'Powder', 'Rod'

    '''
    attr_validate('Form',form)

    MATERIAL_SPECS[f'{name} LDFZ Material Spec'] = MaterialSpec(
        name=f'{name} LDFZ Material Spec',
        template=OBJ_TEMPL['LDFZ Material'],
        process=process,
        properties=[
            PropertyAndConditions(
                property=Property(
                name='Form',
                template=ATTR_TEMPL['Form'],
                value=NominalCategorical(form)
                )
            )
        ],
        tags=tags,
        notes=notes
    )

    return MATERIAL_SPECS[f'{name} LDFZ Material Spec']

### Ingredient Spec Builders ###

INGREDIENT_SPECS = {}

def build_ingredient_spec(name:str,process:ProcessSpec,material:MaterialSpec,quantity,tags:list=[],notes:str=None):
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
        tags=tags,
        notes=notes
    )

    return INGREDIENT_SPECS[f'{name} Ingredient Spec']

### Measurement Spec Builders ###

MEASUREMENT_SPECS = {}

def build_temperature_meas_spec():
    pass

def build_xrd_meas_spec(name:str,duration:float,range:str,adhesive:str,location:str='X-Ray Diffraction Panel',file=None,tags:list=[],notes:str=None):
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
        tags=tags,
        notes=notes
    )

    return MEASUREMENT_SPECS[f'{name} XRD Measurement Spec']

def build_photo_meas_spec(name:str,equipment,location:str,file=None,tags:list=[],notes:str=None):
    '''
    Builds a measurement spec for sample photography

    ### Parameters

    Name: Name of the Measurement, must be the same as associated material and ingredient
        ex: 'YVO4'
    Location: Location in which the measurement was taken.
        ex: 'XRD Panel'
    '''
    attr_validate('Location',location)
    attr_validate('Equipment Used',equipment)

    MEASUREMENT_SPECS[f'{name} Photo Measurement Spec'] = MeasurementSpec(
        name=f'{name} Photo Measurement Spec',
        template=OBJ_TEMPL['Photography'],
        parameters=[
            Parameter(
                name='Equipment Used',
                template=ATTR_TEMPL['Equipment Used'],
                value=NominalCategorical(equipment)
                    )
            ],
        conditions=[Condition(
                    name='Location',
                    template=ATTR_TEMPL['Location'],
                    value=NominalCategorical(location)
                )
            ],
        file_links=file,
        tags=tags,
        notes=notes
    )

    return MEASUREMENT_SPECS[f'{name} Photo Measurement Spec']