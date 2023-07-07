# Attribute templates based on the work of Ali Rachidi for the McQueen lab.

### Imports ###

from gemd.entity.template import PropertyTemplate, ParameterTemplate, ConditionTemplate
from gemd.entity.bounds import CategoricalBounds, RealBounds
import json
import os

### Load Bounds Config ###

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
file_path = os.path.join(script_dir, 'bounds_config.json')

def load_config():
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

config = load_config()

ATTR_TEMPL = {}

### Property Templates ###

name = 'Form'
ATTR_TEMPL[name] = PropertyTemplate(
    name,
    bounds=CategoricalBounds(config['BOUNDS'][name]['categories']),
    description='The form of a particular material'
)

name = 'Purity Percentage'
ATTR_TEMPL[name] = PropertyTemplate(
    name,
    bounds=RealBounds(0.0,100.0,''),
    description='The purity of a particular material as a percentage, also known as percent weight'
)

### Parameter Templates ###

name = 'XRD Adhesive'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=CategoricalBounds(config['BOUNDS'][name]['categories']),
    description='The adhesive agent used to prepare a sample for XRD'
)

# TODO: Maybe add categorical bounds like in Lot ID?
name = 'CAS RN'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=CategoricalBounds(config['BOUNDS'][name]['categories']),
    description='The CAS Registry Number (RN) for a particular reagent'
)

name = 'Duration'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(0,96,'hr'),
    description='Duration of any process, measurement, etc. In our case, it is often used for durations of dwell and ramp up/down times in heating phases, but can also be used to specify measurement/process duration',
    
)

name = 'Equipment Used'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=CategoricalBounds(config['BOUNDS'][name]['categories']),
    description='A parameter describing the equipment used in a particular process or measurement',
)

name = 'Furnace Rate'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(0,100,'degC'),
    description='The rate at which the furnace is heated/cooled during a heating phase expressed in degC/hr',
)

name = 'Furnace Temperature'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(0,1100,'degC'),
    description="The temperature of a heating phase in a furnace. Can be dynamic with a schedule or fixed like a pre-heating temperature",
)

name = 'Laser Power'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(0.,100.,''),
    description='The power of the diode lasers in the LDFZ expressed as a percentage'
)

name = 'Laser Rate'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(0.,100.,''),
    description='The power ramp rate of the diode lasers in the LDFZ expressed as a percentage/hr'
)

name = 'Lot ID'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=CategoricalBounds(config['BOUNDS'][name]['categories']),
    description='The particular Lot of a material purchased from a manufacturer',
)

name = 'Manufacturer'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=CategoricalBounds(config['BOUNDS'][name]['categories']),
    description='The name of the manufacturer from which a raw material was ordered'
)

name = 'Pressure'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(0,500,'MPa'),
    description='The pressure at which a sample is held during a given process. In our case, it is often used for pressing rods or pellets',
)

name = 'Time of Event'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(0,96,'hr'),
    description='Time at which an event occurs. Can be relative to the start/end of a process, or absolute, however specified',
)

name = 'XRD Range'
ATTR_TEMPL[name] = ParameterTemplate(
    name,
    bounds=RealBounds(5,90,'deg'),
    description='The range of angles at which an X-ray Diffraction measurement is taken, usually expressed as 2*theta',
)

### Condition Templates ###

name = 'Atmosphere'
ATTR_TEMPL[name] = ConditionTemplate(
    name,
    bounds=CategoricalBounds(config['BOUNDS'][name]['categories']),
    description='A condition describing the atmosphere in which a process occurs',
)

name = 'Location'
ATTR_TEMPL[name] = ConditionTemplate(
    name,
    bounds=CategoricalBounds(config['BOUNDS'][name]['categories']),
    description='A condition describing the location in which a process or measurement is performed',
)
