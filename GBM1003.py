#Script Version of GBM1003

### Imports ###

from tools.attr_utils import *
from tools.block.Block import Block
from tools.utilities import *

from utils.block_builders import *
from utils.base_builders import *
from utils.provenance import Provenance

from gemd import FileLink
from gemd.json import GEMDJson
import gemd

import os

### Provenance ###

prv = Provenance(
    name='Gannon Murray',
    email='gmurra12@jh.edu',
    tag='GBM',
    page='1003',
    title='Crucible Growth of YVO4',
    date='2023-06-09'
)

### Workflow ###

GBM1003 = {}

### Acquisition Blocks ###

GBM1003['get_Y2O3'] = build_acquiring_material_block(
    name='Y2O3',
    manufacturer='Strem Chemicals',
    lot_id='23195800',
    cas_rn='1314-36-9',
    form='Powder',
    purity=99.99,
    notes='Chalky white powder',
    prv=prv
)

GBM1003['get_V2O5'] = build_acquiring_material_block(
    name='V2O5',
    manufacturer='Noah Technologies Corporation',
    lot_id='0198917/2.1',
    cas_rn='1314-62-1',
    form='Powder',
    purity=99.6,
    notes='Grainy orange powder',
    prv=prv
)

### Grinding Blocks ###

sample = 'GBM1003A'

process = build_grinding_process_base(
    name=sample,
    location='Hot Lab',
    equipment='Mortar and Pestle',
    prv=prv
)

material = build_ground_material_base(
    name=sample,
    process_spec=process.spec,
    process_run=process.run,
    prv=prv
)

ingredients = [
    build_ingredient_base(
        name='Y2O3',
        material_spec=GBM1003['get_Y2O3'].material.spec,
        material_run=GBM1003['get_Y2O3'].material.run,
        process_spec=process.spec,
        process_run=process.run,
        quantity_spec=NominalReal(276.9,'mg'),
        quantity_run = UniformReal(277.0-0.5,277.0+0.5,'mg')
    ),
    build_ingredient_base(
        name='V2O5',
        material_spec=GBM1003['get_V2O5'].material.spec,
        material_run=GBM1003['get_V2O5'].material.run,
        process_spec=process.spec,
        process_run=process.run,
        quantity_spec=NominalReal(223.1,'mg'),
        quantity_run = UniformReal(223.8-0.5,223.8+0.5,'mg')
    )
]

GBM1003[f'grind_{sample}'] = Block(
    name=f'{sample} Grinding Block',
    ingredients=ingredients,
    process=process,
    material=material
)


sample = 'GBM1003B'

process = build_grinding_process_base(
    name=sample,
    location='Hot Lab',
    equipment='Mortar and Pestle',
    prv=prv
)

material = build_ground_material_base(
    name=sample,
    process_spec=process.spec,
    process_run=process.run,
    prv=prv
)

ingredients = [
    build_ingredient_base(
        name='Y2O3',
        material_spec=GBM1003['get_Y2O3'].material.spec,
        material_run=GBM1003['get_Y2O3'].material.run,
        process_spec=process.spec,
        process_run=process.run,
        quantity_spec=NominalReal(283.3,'mg'),
        quantity_run = UniformReal(283.1-0.5,283.1+0.5,'mg')
    ),
    build_ingredient_base(
        name='V2O5',
        material_spec=GBM1003['get_V2O5'].material.spec,
        material_run=GBM1003['get_V2O5'].material.run,
        process_spec=process.spec,
        process_run=process.run,
        quantity_spec=NominalReal(216.7,'mg'),
        quantity_run = UniformReal(216.1-0.5,216.1+0.5,'mg')
    )
]

GBM1003[f'grind_{sample}'] = Block(
    name=f'{sample} Grinding Block',
    ingredients=ingredients,
    process=process,
    material=material
)


sample = 'GBM1003C'

process = build_grinding_process_base(
    name=sample,
    location='Hot Lab',
    equipment='Mortar and Pestle',
    prv=prv
)

material = build_ground_material_base(
    name=sample,
    process_spec=process.spec,
    process_run=process.run,
    prv=prv
)

ingredients = [
    build_ingredient_base(
        name='Y2O3',
        material_spec=GBM1003['get_Y2O3'].material.spec,
        material_run=GBM1003['get_Y2O3'].material.run,
        process_spec=process.spec,
        process_run=process.run,
        quantity_spec=NominalReal(270.9,'mg'),
        quantity_run = UniformReal(270.1-0.5,270.1+0.5,'mg')
    ),
    build_ingredient_base(
        name='V2O5',
        material_spec=GBM1003['get_V2O5'].material.spec,
        material_run=GBM1003['get_V2O5'].material.run,
        process_spec=process.spec,
        process_run=process.run,
        quantity_spec=NominalReal(229.1,'mg'),
        quantity_run = UniformReal(229.2-0.5,229.2+0.5,'mg')
    )
]

GBM1003[f'grind_{sample}'] = Block(
    name=f'{sample} Grinding Block',
    ingredients=ingredients,
    process=process,
    material=material
)

### Heating Blocks ###

for sample in ['GBM1003A','GBM1003B','GBM1003C']:
    
    process = build_heating_process_base(
        name=sample,
        steps=5,
        location='Hot Lab',
        notes='All samples heated simultaneously',
        prv=prv
    )

    material = build_heated_material_base(
        name=sample,
        process_spec=process.spec,
        process_run=process.run,
        form='Powder',
        prv=prv
    )

    ingredients = [
        build_ingredient_base(
            name=sample,
            material_spec=GBM1003[f'grind_{sample}'].material.spec,
            material_run=GBM1003[f'grind_{sample}'].material.run,
            quantity_spec=NominalReal(500.,'mg'),
            quantity_run=NominalReal(500.,'mg'),
            process_spec=process.spec,
            process_run=process.run,
        )
    ]

    measurements = [
        build_xrd_measurement_base(
        name=sample,
        duration=0.25,
        range='5-60',
        adhesive='Vaseline',
        material=material.run,
        prv=prv,
        file=[
            FileLink('GBM1003A Powder XRD','https://occamy.chemistry.jhu.edu/data/XRD/Gannon/ML_Dukie_20230609_1_GBM_0_GBM1003A_YVO4_5-60_15min.raw'),
            FileLink('GBM1003B Powder XRD','https://occamy.chemistry.jhu.edu/data/XRD/Gannon/ML_Dukie_20230609_2_GBM_0_GBM1003B_YV0p95O4_5-60_15min.raw'),
            FileLink('GBM1003C Powder XRD','https://occamy.chemistry.jhu.edu/data/XRD/Gannon/ML_Dukie_20230609_3_GBM_0_GBM1003C_YV1p05O4_5-60_15min.raw')
        ]
    )
    ]
    GBM1003[f'heat_{sample}'] = Block(
        name=f'{sample} Heating Block',
        ingredients=ingredients,
        process=process,
        material=material,
        measurements=measurements
    )

### Dump blocks to JSONs ###
'''
encoder = GEMDJson()

fp = f'./dumps/GBM1003'
os.mkdir(fp)

for block in GBM1003.values():
    block.thin_dumps(encoder,fp)

'''
