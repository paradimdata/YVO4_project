# Object templates based on the work of Ali Rachidi for the McQueen lab.

### Imports ###

from gemd.entity.bounds import RealBounds
from gemd.entity.template import ProcessTemplate, MaterialTemplate, MeasurementTemplate
from attribute_templates import ATTR_TEMPL

OBJ_TEMPL = {}

### Material Templates ###

name = 'Purchased Raw Material'
OBJ_TEMPL[name] = MaterialTemplate(
    name,
    description='A raw material purchased from a manufacturer',
    properties=[
        ATTR_TEMPL['Form'],
        ATTR_TEMPL['Purity Percentage'],
    ]
)

name = 'Heated Material'
OBJ_TEMPL[name] = MaterialTemplate(
    name,
    description='A material produced from a Partlow heating process, whether for purification, synthesis or else',
    properties=[
        ATTR_TEMPL['Form'],
    ]
)

name = 'Ground Material'
OBJ_TEMPL[name] = MaterialTemplate(
    name,
    description='A material ground into a powder',
    properties=[
        ATTR_TEMPL['Form'],
    ]
)

name = 'Chunked Material'
OBJ_TEMPL[name] = MaterialTemplate(
    name,
    description='A material chunked into small pieces to attain specific mass and/or volume',
    properties=[
        ATTR_TEMPL['Form'],
    ]
)

name = 'Pressed Material'
OBJ_TEMPL[name] = MaterialTemplate(
    name,
    description='A material pressed into a rod or pellet using a press',
    properties=[
        ATTR_TEMPL['Form'],
    ]
)

### Process Templates ###

name = 'Purchasing Raw Material'
OBJ_TEMPL[name] = ProcessTemplate(
    name,
    description='Purchasing any particular raw material from a manufacturer',
    parameters=[
        ATTR_TEMPL['Manufacturer'],
        ATTR_TEMPL['Lot ID'],
        ATTR_TEMPL['CAS RN'],
    ]
)

#TODO: clarify box vs tube + add location
name = 'Heating'
OBJ_TEMPL[name] = ProcessTemplate(
    name,
    description='''Heating something in the box furnace with 
                   a max temperature and tuning of ramp up/down''',
    parameters=[
        [ATTR_TEMPL['Furnace Temperature'],RealBounds(0.,1050.,'degC')],
        [ATTR_TEMPL['Furnace Rate'],RealBounds(0.,100.,'degC')],
        ATTR_TEMPL['Duration'],
    ],
    conditions = [
        ATTR_TEMPL['Location']
    ]
)

name = 'Quenching Tube'
OBJ_TEMPL[name] = ProcessTemplate(
    name,
    description='''Removing tube from tube furnacew with tongs to grab the tube wrapped with wire and submerge in water''',
    conditions = [
        ATTR_TEMPL['Location']
    ],
    parameters=[
        ATTR_TEMPL['Equipment Used'],
        ATTR_TEMPL['Duration'],
    ],
)

name = 'Grinding Material'
OBJ_TEMPL[name] = ProcessTemplate(
    name,
    description='Grinding a material into a powder',
    conditions = [
        ATTR_TEMPL['Location']
    ],
    parameters=[
        ATTR_TEMPL['Equipment Used'],
    ],
)

name = 'Chunking Material'
OBJ_TEMPL[name] = ProcessTemplate(
    name,
    description='Chunking mass of a material to match some mass, volume or other characteristic'
)

name = 'Pressing Material'
OBJ_TEMPL[name] = ProcessTemplate(
    name,
    description='Pressing materials with pressing equipment to transform into rods or pellets',
    conditions = [
        ATTR_TEMPL['Location']
    ],
    parameters=[
        ATTR_TEMPL['Equipment Used'],
        ATTR_TEMPL['Duration'],
        ATTR_TEMPL['Pressure']
    ],
)

name = 'Setting Pellets'
OBJ_TEMPL[name] = ProcessTemplate(
    name,
    description='Setting up pellets for experience with appropriate location, distance, or equipment specifications  ',
    conditions = [
        ATTR_TEMPL['Location']
    ],
    parameters=[
        ATTR_TEMPL['Equipment Used'],
    ],
)

name = 'Sealing Vessel'
OBJ_TEMPL[name] = ProcessTemplate(
    name,
    description='Sealing vessel of reaction according to desired lay out',
    conditions = [
        ATTR_TEMPL['Location']
    ],
    parameters=[
        ATTR_TEMPL['Equipment Used'],
    ],
)

### Measurement Templates ###
name = 'X-Ray Diffraction'
OBJ_TEMPL[name] = MeasurementTemplate(
    name,
    description='Applying x-ray diffraction to discover structure and properties of a material ',
    conditions = [
        ATTR_TEMPL['Location'],
        ATTR_TEMPL['Duration'],
        ATTR_TEMPL['XRD Range']
    ]
)

name = 'Temperature Measurement'
OBJ_TEMPL[name] = MeasurementTemplate(
    name,
    description='Measuring the temperature of pellets (=temperature gradient of tube) in a tube furnace heating ',
    conditions = [
        ATTR_TEMPL['Location']
    ],
    parameters=[
        ATTR_TEMPL['Time of Event']
    ]
)