# YVO<sub>4</sub> Project
The purpose of this project is to grow YVO<sub>4</sub> crystals by a variety of methods, documenting all relevant data and metadata using the GEMD framework. This process will produce scientifically relevant information about the crystals, but also serve as a proof-of-concept for the end-to-end implementation of GEMD and demonstrate the value of the methodology. 

## Overview 

This project provides a framework for the instantiation of materials metadata through Jupyter [`Notebooks`](#Notebooks). Each of these Notebooks builds a dictionary of [`Blocks`](#Block) using helper functions, called [`Builders`](#Builders). Blocks contain [`BaseNodes`](#BaseNode) and link them appropriately. BaseNodes contain all of the GEMD objects for a given process. After each Notebook is instantiated, the contents can be Dumped to a series of JSON files, which [`GEMDModeller`](#GemdModeller) can convert into Networkx graphs. 

## Notebooks

In this project, notebooks serve two purposes. First they serve as a tool to document the details of an experiment, similar to an electronic lab notebook. In fact, it is plausible to envision a workflow in which an experiment is recorded directly into a similar notebook in the laboratory. The notebook should be easily navigated and understood by a human reader. 

Second, and perhaps more importantly, the notebooks serve as an interface with which one can interact with the rest of the codebase. The notebook utilizes helper functions to instantiate experimental data into Python objects in a simple, repeatable way. It can also be used to pre-process the data for later use.

### Structure

Below is the basic structure for the notebooks already used in this project. There are many other possible configurations based on user needs. The point of the notebooks is to make instantiation easier, so use the structure that works best for you.

#### Imports

As with any Python-based project, the notebooks start with a list of imports. Some of the key modules are `GEMD` and its sub-packages, `utils` and the various helper functions within, and `tools` from [OpenMSIModel](https://github.com/openmsi/gemd_tools/tree/main). 

It may also be necessary to import materials from previous notebooks. The following is one method to achieve this. See [Workflow](#workflow) for more information about the Workflow dictionary. 
```python
import import_ipynb
from FILE import WORKFLOW
```

#### Header & Provenance

Next, it is important to make sure that the contents of the notebook can be easily understood without digging into the code. A simple Markdown header with important experiment information can be used.
```Markdown
### Example Title
This is a *very* brief description of the experiment.

The purpose of the experiment was to be an example.

Performed YYYY-MM-DD @ LOCATION by PERSONNEL
```

The `Provenance` package from `utils` provides an easy way to create an object containing details about the experiment that can be referenced later. Many of the helper functions require a `Provenance` type object as an argument.

#### Experiment Codeblocks

Once the foundation is set, we can start actually recording the experiment. This is done by calling a series of helper functions in order to create serialiazble objects containing experimental data. Generally one codeblock will describe one process or step in the experimental procedure.

For each codeblock, helper functions will create [BaseNode](#basenode) objects for a `Process`, `Material`, `Ingredients`, and possibly `Measurement`. These objects will be stored in a [`Block`](#block), which is in turn stored in a [`Workflow`](#workflow). More information about helper functions can be found in [Builders](#builders). 

Below is an example of a generic experimental codeblock:

```python
### Process Block ###

process = build_process_base(
    name='Name',
    location='Location',
    equipment='Equipment',
    parameters=[Parameter()],
    conditions=[Condition()],
    prv=Provenance()
)

material = build_material_base(
    name='Name',
    process_spec=process.spec,
    process_run=process.run,
    prv=Provenance()
)

ingredients = [
    build_ingredient_base(
        name='Name',
        material_spec=WORKFLOW['previous_material'].material.spec,
        material_run=WORKFLOW['previous_material'].material.run,
        process_spec=process.spec,
        process_run=process.run,
        quantity_spec=BaseValue(),
        quantity_run=BaseValue()
    )
]

measurements = [
    build_measurement_base(
        parameters=[Parameter()],
        conditions=[Condition()],
        material=material.run,
        prv=Provenance(),
        file=FileLink()
    )
]

WORKFLOW['current_process'] = Block(
    name=' Current Process Block',
    ingredients=ingredients,
    process=process,
    material=material,
    measurements = measurement
)
``` 

#### Pre-Processing

Once all of the data is stored in serializable objects, it is possible to reference, interact with, and process it in a programmatic fashion. One of the best ways to do this is by writing the objects to JSON files. See [JSON Dumping](#json-dumping) for more details.

## GEMD Structure

This section outlines the structure of the data schema from basic GEMD Objects up to Workflows. More detailed documentation about any of these objects can be found in [Related Documents](#related-documents).  

### GEMD Objects

GEMD (Graphical Expression of Materials Data) is an open source format for storing interconnected Data Objects, including `Materials`, `Processes`, `Measurements`, and `Ingredients`. 

Data Objects exist in `Template`, `Spec`, and `Run` states. 

- A `Template` indicates the general features of an object, such as the physical form of a material. 

- A `Spec` indicates the intention of an experimental procedure, such as the intent to use 100.00 mg of an ingredient. 

- A `Run` records the experimental reality and any deviation from the Spec, such as the use of 100.14 mg of said ingredient due to error. 

Data Objects can have Attributes in three categories: `Properties`, `Parameters`, and `Conditions`. Templates are used to  specify Attribute Bounds.

For more information, see [GEMD Docs](https://github.com/CitrineInformatics/gemd-docs) and [GEMD Python Docs](https://citrineinformatics.github.io/citrine-python/getting_started/index.html).

### BaseNode

`BaseNodes` are objects that contain all of the state data related to a GEMD Data Object. BaseNodes have the same four types as GEMD Data Objects, and each contains and links Template, Spec, and Run data. 

### Block

`Blocks` are objects that contain a set of related BaseNodes. Blocks are very process-oriented and usually include BaseNodes for a Process, the Material created by that process, Ingredients consumed in that process, and any Measurements performed on the material. Blocks contain methods to link their constituent objects to one another, and to objects in other Blocks. 

### Workflow

A `Workflow` is an object that contains a series of Blocks and describes an entire experimental procedure from start to finish. OpenMSIModel contains a Workflow class with helpful methods and functionalities, but due to limited support this project uses simple dictionaries to contain and access Blocks. Block object values in a Workflow dictionary are accessed by unique, descriptive string keys. 

For example:

```python
WORKFLOW['process_material'] = Block()
```

For more information on `BaseNodes`, `Blocks`, and `Workflows` see [OpenMSIModel](https://github.com/openmsi/gemd_tools/tree/main).

## Builders

One of the key design goals for this project is to make repetitive data entry fast and simple. Helper functions that create common objects is one way to help achieve this. Robust helper functions allow users to work at high abstraction levels (writing Blocks, not GEMD Objects). 

This project uses helper functions to instantiate GEMD objects, BaseNodes, and Blocks (limited support). These `Builder` functions exist in scripts in the `utils` directory.  Generic examples are provided below.

### Spec Builders

Each `Spec Builder` instantiates a Spec for a given GEMD Data Object and validates arguments against Templates and Bounds. 

The following function is an example of a generic Spec Builder:

```python
def build_gemd_object_spec(
    name:str,
    attribute:any,
    notes:str=None):
    '''
    Builds a spec for a GEMD Data Object.

    ### Parameters

    Name: Name of the object
    Attributes: Parameters, Properties, or Conditions
    Notes: Notes about the object as a string

    '''
    attr_validate('Attribute',attribute)

    OBJECT_SPECS[f'{name} Spec'] = ObjectSpec(
        name=f'{name} Spec',
        template=OBJ_TEMPL['Object Template'],
        parameters=[
            Parameter(
                name='Parameter',
                template=ATTR_TEMPL['Parameter Teplate'],
                value=BaseValue
                    )
                ],
        conditions=[
            Condition(
                name='Condition',
                template=ATTR_TEMPL['Condition Template'],
                value=BaseValue
                    )
                ],
        notes=notes
    )

    return OBJECT_SPECS[f'{name} Spec']
```

### Base Builders

Each `Base Builder` instantiates a BaseNode by first building a Spec and creating a Run from that Spec. A BaseNode class is defined and the Spec and Run are passed to the `.from_spec_or_run()` method to create an instance.

The following function is an example of a generic Base Builder:

```python
def build_grinding_process_base(name:str,attributes:any,notes:str,workflow:Workflow,prv:Provenance):
    """
    Builds a BaseNode.

    ### Parameters:

    Name: Name of the material being acquired
    Attributes: Variables related to attributes.
    Workflow: Workflow to which the Block belongs 
    Provenance: Provenance object describing the personnel involved
    """

    object_spec = build_gemd_object_spec(
        name,
        attributes,
        notes
        )

    object_run = ObjectRun( 
        name=name,
        spec=object_spec,
        conditions=object_spec.conditions,
        parameters=object_spec.parameters,
        source= PerformedSource(prv.email,prv.date)
    )

    class ObjectBase(BaseNode):

        TEMPLATE: ClassVar[ObjectTemplate] = ObjectTemplate(name=__name__,)
        _ATTRS: ClassVar[AttrsDict] = {'conditions':{},'parameters':{},'properties':{}}

        define_attribute(
            _ATTRS,
            template=AttributeTemplate(
                name='Attribute', bounds=ATTR_TEMPL['Attribute'].bounds
            )      
        )

        finalize_template(_ATTRS, TEMPLATE)

    base = ObjectBase.from_spec_or_run(
                name=f'{name} Base',
                run=object_run,
                spec=object_spec
            )

    return base
```

### Block Builders

Each `Block Builder` instantiates a Block by instantiating BaseNodes and adding them to Block objects. There are several challenges that make this approach somewhat impractical from a Notebook. 

The only Block Builder that is supported is `build_acquiring_material_block()`. This function is intended to be used at the beginning of a Workflow and instantiates data about stock starting materials.

## JSON Dumping

Since Blocks are serializable objects, they can be dumped to a collection of JSON files for further processing. Blocks have a `.thin_dumps()` method which will write all appropriate thin JSON files to a specified directory using a JSON encoder. The GEMD framework comes with its own encoder, which can be imported as a module. The notebooks use a codeblock like the following to call the `Block.thin_dumps()` method for an entire workflow.

```python
from gemd.json import GEMDJson
import os

encoder = GEMDJson()
fp = f'./path/to/directory/'
os.mkdir(fp)

for block in WORKFLOW.values():
    block.thin_dumps(encoder,fp)
```
*Note: Once the contents of a notebook has been dumped, it is helpful to comment out or otherwise disable that codeblock. This prevents the notebook from trying to dump its contents again if you import it, which returns an error.* 

## OpenMSIModel

[OpenMSIModel](https://github.com/openmsi/gemd_tools/tree/main) is a set of tools and utilities for GEMD developed by Ali Rachidi and Soren Bear. A modified version of OpenMSIModel has been forked as `tools`. This module enables the use of `Block` and `Workflow` classes. The latest version can be cloned and installed with `pip`, allowing it to be easily accessed from the command line. 

ONe of the most powerful tools available in OPenMSIModel is the `gemdmodeller` script. Once installed, the following command can be used to create an interactive graph of a material history:

```bash
bash$ gemd_modeller ./path/to/json/dump/ --launch_notebook
```

This graph not only provides convenient data visualiztion, but also creates the potential for applying machine learning models and enables advanced queryability.

*Note: gemd_modeller has many dependencies, including networkx, pygraphviz, and yFiles. Make sure to properly install all dependencies before running gemd_modeller. Be aware that pygraphviz is notoriously difficult to install on Windows 10, though it is possible using a Conda distribution.*

## Related Documents
[GEMD Overview](https://citrineinformatics.github.io/gemd-docs/high-level-overview/)

[GEMD Docs](https://github.com/CitrineInformatics/gemd-docs)

[GEMD Python Docs](https://citrineinformatics.github.io/citrine-python/getting_started/index.html)

[OpenMSIModel](https://github.com/openmsi/gemd_tools/tree/main)

## Glossary

### Notebooks
In this project, notebooks serve two purposes. First, they serve as a tool to document the details of an experiment, similar to an electronic lab notebook. Second, they serve as an interface to interact with the rest of the codebase. [Read more](#notebooks).

### GEMD Objects
GEMD (Graphical Expression of Materials Data) is an open-source format for storing interconnected Data Objects, including Materials, Processes, Measurements, and Ingredients. Data Objects exist in Template, Spec, and Run states. [Read more](#gemd-objects).

### BaseNode
BaseNodes are objects that contain all of the state data related to a GEMD Data Object. BaseNodes have the same four types as GEMD Data Objects and each contains and links Template, Spec, and Run data. [Read more](#basenode).

### Block
Blocks are objects that contain a set of related BaseNodes. Blocks are very process-oriented and usually include BaseNodes for a Process, the Material created by that process, Ingredients consumed in that process, and any Measurements performed on the material. Blocks contain methods to link their constituent objects to one another and to objects in other Blocks. [Read more](#block).

### Workflow
A Workflow is an object that contains a series of Blocks and describes an entire experimental procedure from start to finish. It is represented using a dictionary with unique, descriptive string keys to access Block objects. [Read more](#workflow).

### Builders
Builders are helper functions used to instantiate GEMD objects, BaseNodes, and Blocks. They simplify repetitive data entry and allow users to work at high abstraction levels. [Read more](#builders).

### Spec Builders
Spec Builders are functions that instantiate a Spec for a given GEMD Data Object and validate arguments against Templates and Bounds. [Read more](#spec-builders).

### Base Builders
Base Builders are functions that instantiate a BaseNode by first building a Spec and creating a Run from that Spec. [Read more](#base-builders).

### Block Builders
Block Builders are functions that instantiate a Block by instantiating BaseNodes and adding them to Block objects. [Read more](#block-builders).

### JSON Dumping
JSON Dumping refers to the process of converting Blocks, which are serializable objects, into a collection of JSON files for further processing and analysis. [Read more](#json-dumping).

### OpenMSIModel
OpenMSIModel is a set of tools and utilities for GEMD developed by Ali Rachidi and Soren Bear. It enables the use of Block and Workflow classes for advanced data visualization and analysis. [Read more](#openmsimodel).

### gemd_modeller
gemd_modeller is a powerful tool available in OpenMSIModel that creates an interactive graph of a material's history using JSON files generated from Blocks. It provides convenient data visualization, machine learning model application, and advanced queryability. [Read more](#gemd-modeller).

### Related Documents
Links to additional documentation and resources related to GEMD, GEMD Python, and OpenMSIModel. [Read more](#related-documents).
