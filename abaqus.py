# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
## Création du modèle
mdb.Model(modelType=STANDARD_EXPLICIT, name='Model-3D-poutre')
## Création  de l'esquisse
# Tube vertical
mdb.models['Model-3D-poutre'].ConstrainedSketch(name='__profile__', sheetSize=
    200.0)
mdb.models['Model-3D-poutre'].sketches['__profile__'].Line(point1=(0.0, -50.0), 
    point2=(0.0, 50.0))
mdb.models['Model-3D-poutre'].sketches['__profile__'].VerticalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-3D-poutre'].sketches['__profile__'].geometry[2])
mdb.models['Model-3D-poutre'].Part(dimensionality=THREE_D, name='Tube_vertical'
    , type=DEFORMABLE_BODY)
mdb.models['Model-3D-poutre'].parts['Tube_vertical'].BaseWire(sketch=
    mdb.models['Model-3D-poutre'].sketches['__profile__'])
del mdb.models['Model-3D-poutre'].sketches['__profile__']
# tube horizontal
mdb.models['Model-3D-poutre'].ConstrainedSketch(name='__profile__', sheetSize=
    200.0)
mdb.models['Model-3D-poutre'].sketches['__profile__'].Line(point1=(-100.0, 0.0)
    , point2=(100.0, 0.0))
mdb.models['Model-3D-poutre'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-3D-poutre'].sketches['__profile__'].geometry[2])
mdb.models['Model-3D-poutre'].Part(dimensionality=THREE_D, name='Part-2', type=
    DEFORMABLE_BODY)
mdb.models['Model-3D-poutre'].parts['Part-2'].BaseWire(sketch=
    mdb.models['Model-3D-poutre'].sketches['__profile__'])
del mdb.models['Model-3D-poutre'].sketches['__profile__']
# coude
mdb.models['Model-3D-poutre'].ConstrainedSketch(name='__profile__', sheetSize=
    200.0)
mdb.models['Model-3D-poutre'].sketches['__profile__'].ArcByCenterEnds(center=(
    0.0, 0.0), direction=CLOCKWISE, point1=(-50.0, 0.0), point2=(0.0, 50.0))
mdb.models['Model-3D-poutre'].Part(dimensionality=THREE_D, name='Part-3', type=
    DEFORMABLE_BODY)
mdb.models['Model-3D-poutre'].parts['Part-3'].BaseWire(sketch=
    mdb.models['Model-3D-poutre'].sketches['__profile__'])
del mdb.models['Model-3D-poutre'].sketches['__profile__']
## Matériaux
mdb.models['Model-3D-poutre'].Material(name='Acier 304')
mdb.models['Model-3D-poutre'].materials['Acier 304'].Density(table=((7.9e-05, 
    ), ))
mdb.models['Model-3D-poutre'].materials['Acier 304'].Elastic(table=((200000.0, 
    0.3), ))
## Sections
mdb.models['Model-3D-poutre'].PipeProfile(name='Profil-circulaire-creux', r=
    50.0, t=10.0)
mdb.models['Model-3D-poutre'].BeamSection(beamSectionOffset=(0.0, 0.0), 
    consistentMassMatrix=False, integration=DURING_ANALYSIS, material=
    'Acier 304', name='Section-circulaire-poutre', poissonRatio=0.0, profile=
    'Profil-circulaire-creux', temperatureVar=LINEAR)
# Association coude
 mdb.models['Model-3D-poutre'].parts['Part-3'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    edges=mdb.models['Model-3D-poutre'].parts['Part-3'].edges.getSequenceFromMask(
    mask=('[#1 ]', ), )), sectionName='Section-circulaire-poutre', 
    thicknessAssignment=FROM_SECTION)
# Association tube vertical
mdb.models['Model-3D-poutre'].parts['Tube_vertical'].SectionAssignment(offset=
    0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    edges=mdb.models['Model-3D-poutre'].parts['Tube_vertical'].edges.getSequenceFromMask(
    mask=('[#1 ]', ), )), sectionName='Section-circulaire-poutre', 
    thicknessAssignment=FROM_SECTION)
# Association tube horizontal
mdb.models['Model-3D-poutre'].parts['Part-2'].Set(edges=
    mdb.models['Model-3D-poutre'].parts['Part-2'].edges.getSequenceFromMask((
    '[#1 ]', ), ), name='tige horizontale')
mdb.models['Model-3D-poutre'].parts['Part-2'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-3D-poutre'].parts['Part-2'].sets['tige horizontale'], 
    sectionName='Section-circulaire-poutre', thicknessAssignment=FROM_SECTION)

## Assembly
# initier assemblage
mdb.models['Model-3D-poutre'].rootAssembly.DatumCsysByDefault(CARTESIAN)
# import des pièces
mdb.models['Model-3D-poutre'].rootAssembly.Instance(dependent=ON, name=
    'Tube_vertical-1', part=
    mdb.models['Model-3D-poutre'].parts['Tube_vertical'])
mdb.models['Model-3D-poutre'].rootAssembly.Instance(dependent=ON, name=
    'Part-3-1', part=mdb.models['Model-3D-poutre'].parts['Part-3'])
mdb.models['Model-3D-poutre'].rootAssembly.Instance(dependent=ON, name=
    'Part-2-1', part=mdb.models['Model-3D-poutre'].parts['Part-2'])
# déplacement des pièces
mdb.models['Model-3D-poutre'].rootAssembly.translate(instanceList=('Part-3-1', 
    ), vector=(50.0, 50.0, 0.0))
mdb.models['Model-3D-poutre'].rootAssembly.translate(instanceList=('Part-2-1', 
    ), vector=(150.0, 100.0, 0.0))
