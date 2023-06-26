# Attribute templates based on the work of Ali Rachidi for the McQueen lab.

### Imports ###

from gemd.entity.template import PropertyTemplate, ParameterTemplate, ConditionTemplate
from gemd.entity.bounds import CategoricalBounds, RealBounds

ATTR_TEMPL = {}

### Property Templates ###

name = 'Form'
ATTR_TEMPL[name] = PropertyTemplate(
    name,
    bounds=CategoricalBounds(['Powder -325 mesh','Powder','Pieces', 'Pellet', 'resublimed crystals', 'Amorphous','Ingot','Solid','Crystal','Chunk','Chunk and Powder','Solution']),
    description='The form of a particular material'
)

name = 'Purity Percentage'
ATTR_TEMPL[name] = PropertyTemplate(
    name,
    bounds=RealBounds(0.0,100.0,'%'),
    description='The purity of a particular material as a percentage'
)

### Parameter Templates ###

# TODO: Maybe add categorical bounds like in Lot ID?
name = 'CAS RN'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=None,
    description='The CAS Registry Number (RN) for a particular reagent'
)

name = 'Manufacturer'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=CategoricalBounds(['Alfa Aesar','Thermo Scientific','Yeemeida Technology Co. LTD']),
    description='The name of the manufacturer from which a raw material was ordered'
)

name = 'Lot ID'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=CategoricalBounds(['W19F006','R10H008','X17C007', 'R04D028']),
    description='The particular Lot of a material purchased from a manufacturer',
)

name = 'Equipment Used'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=CategoricalBounds(['Mortar and Pestle', 'Pellet Press Set', 'Quartz Tube', 'Quartz Wool', 'Nichrome Wire', 'Tube Sealing Station', 'Torch', 'Thermocouple', 'Tongs']),
    description='A parameter describing the equipment used in a particular process or measurement',
)

name = 'Furnace Temperature'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(0,1100,'degC'),
    description="The temperature of a heating phase in a furnace. Can be dynamic with a schedule or fixed like a pre-heating temperature",
)

name = 'Furnace Rate'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(0,100,'degC/hr'),
    description='The rate at which the furnace is heated/cooled during a heating phase',
)

name = 'Duration'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(0,96,'hr'),
    description='Duration of any process, measurement, etc. In our case, it is often used for durations of dwell and ramp up/down times in heating phases, but can also be used to specify measurement/process duration',
    
)

name = 'Time of Event'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(0,96,'hr'),
    description='Time at which an event occurs. Can be relative to the start/end of a process, or absolute, however specified',
)

name = 'Pressure'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(0,500,'MPa'),
    description='The pressure at which a sample is held during a given process. In our case, it is often used for pressing rods or pellets',
)

name = 'XRD Range'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(5,90,'deg'),
    description='The range of angles at which an X-ray Diffraction measurement is taken, usually expressed as 2*theta',
)

### Condition Templates ###

name = 'Location'
ATTR_TEMPL[name] = ConditionTemplate(
    name,
    bounds=CategoricalBounds(['Purification Tube Furnace', 'Synthesis Tube Furnace','Three Zones Tube Furnace', 'X-Ray Diffraction Panel', 'Bucket']),
    description='A condition describing the location in which a process or measurement is performed',
)

name = 'Atmosphere'
ATTR_TEMPL[name] = ConditionTemplate(
    name,
    bounds=CategoricalBounds(['Inner Atmosphere Glovebox', 'Air']),
    description='A condition describing the atmosphere in which a process occurs',
)