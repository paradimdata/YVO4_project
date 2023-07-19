# YVO<sub>4</sub> Project
The purpose of this project is to grow YVO<sub>4</sub> crystals by a variety of methods, documenting all relevant data and metadata using the GEMD framework. This process will produce scientifically relevant information about the crystals, but also serve as a proof-of-concept for the end-to-end implementation of GEMD and demonstrate the value of the methodology. 

## Overview 

This project provides a framework for the instantiation of materials metadata through Jupyter [`Notebooks`](#Notebooks). Each of these Notebooks builds a dictionary of [`Blocks`](#Block) using helper functions, called [`Builders`](#Builders). Blocks contain [`BaseNodes`](#BaseNode) and link them appropriately. BaseNodes contain all of the GEMD objects for a given process. After each Notebook is instantiated, the contents can be Dumped to a series of JSON files, which [`GEMDModeller`](#GemdModeller) can convert into Networkx graphs. 

## Notebooks

### Structure

### Usage

## GEMD Structure

This section outlines the structure of the data schema from basic GEMD Objects up to Workflows. More detailed documentation about any of these objects can be found in [Related Documents](#related-documents).  

### GEMD Objects

GEMD (Graphical Expression of Materials Data) is an open source format for storing interconnected Data Objects, including `Materials`, `Processes`, `Measurements`, and `Ingredients`. Data Objects exist in `Template`, `Spec`, and `Run` states, representing generalization, intent, and actual results, respectively.

Data Objects can have Attributes in three categories: `Properties`, `Parameters`, and `Conditions`. Templates are used to  specify Attribute Bounds.

For more information, see [GEMD Docs](https://github.com/CitrineInformatics/gemd-docs) and [GEMD Python Docs](https://citrineinformatics.github.io/citrine-python/getting_started/index.html).

### BaseNode

`BaseNodes` are objects that contain all of the state data related to a GEMD Data Object. BaseNodes have the same four types as GEMD Data Objects, and each contains and links Template, Spec, and Run data. 

### Block

`Blocks` are objects that contain a set of related BaseNodes. Blocks are very process-oriented and usually include BaseNodes for a Process, the Material created by that process, Ingredients consumed in that process, and any Measurements performed on the material. Blocks contain methods to link their constituent objects to one another, and to objects in other Blocks. 

### Workflow

A `Workflow` is an object that contains a series of Blocks and describes an entire experimental procedure from start to finish. GEMD Tools contains a Workflow class with helpful methods and functionalities, but due to limited support this project uses simple dictionaries to contain and access Blocks. 

For more information on `BaseNodes`, `Blocks`, and `Workflows` see [GEMD Tools](https://github.com/openmsi/gemd_tools/tree/main).

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

## GEMDModeller

## Requirements

## Related Documents
[GEMD Overview](https://citrineinformatics.github.io/gemd-docs/high-level-overview/)

[GEMD Docs](https://github.com/CitrineInformatics/gemd-docs)

[GEMD Python Docs](https://citrineinformatics.github.io/citrine-python/getting_started/index.html)

[GEMD Tools](https://github.com/openmsi/gemd_tools/tree/main)
