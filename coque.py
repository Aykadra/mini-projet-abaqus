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
from abaqusConstants import *

MODELE_POUTRE = 'Model-full-coque'
mdb.Model(modelType=STANDARD_EXPLICIT, name=MODELE_POUTRE)

## Chemin
mdb.models['Model-full-coque'].ConstrainedSketch(name='__sweep__', sheetSize=
    3000.0)
mdb.models['Model-full-coque'].sketches['__sweep__'].Line(point1=(-1500.0, 
    -1000.0), point2=(-1500.0, 0.0))
mdb.models['Model-full-coque'].sketches['__sweep__'].VerticalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-full-coque'].sketches['__sweep__'].geometry[2])
mdb.models['Model-full-coque'].sketches['__sweep__'].ArcByCenterEnds(center=(
    -900.0, 0.0), direction=CLOCKWISE, point1=(-1500.0, 0.0), point2=(-900.0, 
    600.0))
mdb.models['Model-full-coque'].sketches['__sweep__'].Line(point1=(-900.0, 
    600.0), point2=(1100.0, 600.0))
mdb.models['Model-full-coque'].sketches['__sweep__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-full-coque'].sketches['__sweep__'].geometry[4])
mdb.models['Model-full-coque'].sketches['__sweep__'].TangentConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-full-coque'].sketches['__sweep__'].geometry[3], entity2=
    mdb.models['Model-full-coque'].sketches['__sweep__'].geometry[4])

## Profil
mdb.models['Model-full-coque'].ConstrainedSketch(name='__profile__', sheetSize=
    3000.0, transform=(1.0, 0.0, 0.0, 0.0, 0.0, 1.0, -0.0, -1.0, -0.0, -1500.0, 
    -1000.0, 0.0))
mdb.models['Model-full-coque'].sketches['__profile__'].ConstructionLine(point1=
    (-1500.0, 0.0), point2=(1500.0, 0.0))
mdb.models['Model-full-coque'].sketches['__profile__'].ConstructionLine(point1=
    (0.0, -1500.0), point2=(0.0, 1500.0))
mdb.models['Model-full-coque'].sketches['__profile__'].CircleByCenterPerimeter(
    center=(0.0, 0.0), point1=(550.0, 0.0))
mdb.models['Model-full-coque'].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-full-coque'].sketches['__profile__'].vertices[1], 
    entity2=mdb.models['Model-full-coque'].sketches['__profile__'].geometry[2])
mdb.models['Model-full-coque'].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-full-coque'].sketches['__profile__'].vertices[0], 
    entity2=mdb.models['Model-full-coque'].sketches['__profile__'].geometry[2])
mdb.models['Model-full-coque'].Part(dimensionality=THREE_D, name='Coude', 
    type=DEFORMABLE_BODY)
mdb.models['Model-full-coque'].parts['Coude'].BaseShellSweep(path=
    mdb.models['Model-full-coque'].sketches['__sweep__'], sketch=
    mdb.models['Model-full-coque'].sketches['__profile__'])
del mdb.models['Model-full-coque'].sketches['__profile__']
del mdb.models['Model-full-coque'].sketches['__sweep__']


## creation des matériaux

mdb.models['Model-full-coque'].Material(name='Acier 304')
mdb.models['Model-full-coque'].materials['Acier 304'].Density(table=((7.9e-09, 
    ), ))
mdb.models['Model-full-coque'].materials['Acier 304'].Elastic(table=((200000.0, 
    0.3), ))
## Creation section
mdb.models['Model-full-coque'].HomogeneousShellSection(idealization=
    NO_IDEALIZATION, integrationRule=SIMPSON, material='Acier 304', name=
    'Section_coque', nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT
    , preIntegrate=OFF, temperature=GRADIENT, thickness=100.0, thicknessField=
    '', thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
## assignation section
mdb.models['Model-full-coque'].parts['Coude'].Set(faces=
    mdb.models['Model-full-coque'].parts['Coude'].faces.getSequenceFromMask((
    '[#7 ]', ), ), name='tube_complet')
mdb.models['Model-full-coque'].parts['Coude'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-full-coque'].parts['Coude'].sets['tube_complet'], sectionName=
    'Section_coque', thicknessAssignment=FROM_SECTION)

## Creation des sets

mdb.models['Model-full-coque'].parts['Coude'].Set(faces=
    mdb.models['Model-full-coque'].parts['Coude'].faces.getSequenceFromMask((
    '[#4 ]', ), ), name='tube_vertical')
mdb.models['Model-full-coque'].parts['Coude'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-full-coque'].parts['Coude'].sets['tube_vertical'], 
    sectionName='Section_coque', thicknessAssignment=FROM_SECTION)
mdb.models['Model-full-coque'].parts['Coude'].Set(faces=
    mdb.models['Model-full-coque'].parts['Coude'].faces.getSequenceFromMask((
    '[#2 ]', ), ), name='tube_coude')
mdb.models['Model-full-coque'].parts['Coude'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-full-coque'].parts['Coude'].sets['tube_coude'], 
    sectionName='Section_coque', thicknessAssignment=FROM_SECTION)
mdb.models['Model-full-coque'].parts['Coude'].Set(faces=
    mdb.models['Model-full-coque'].parts['Coude'].faces.getSequenceFromMask((
    '[#1 ]', ), ), name='tube_horizontal')
mdb.models['Model-full-coque'].parts['Coude'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-full-coque'].parts['Coude'].sets['tube_horizontal'], 
    sectionName='Section_coque', thicknessAssignment=FROM_SECTION)

## début assemblage
mdb.models['Model-full-coque'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-full-coque'].rootAssembly.Instance(dependent=OFF, name=
    'Coude-1', part=mdb.models['Model-full-coque'].parts['Coude'])
# mdb.models['Model-full-coque'].rootAssembly.makeIndependent(instances=(
#     mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'], ))

## Partitionnement
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#1 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[1], 
    MIDDLE), point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[0], 
    MIDDLE))
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#1 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[3]
    , point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[0])
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#4 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[0]
    , point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[4])
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#8 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[4]
    , point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[5])
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#8 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[8], 
    MIDDLE), point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[6], 
    MIDDLE))
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#8 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[1]
    , point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[7])

## Partitionnage milieu
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#1 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[0], 
    MIDDLE), point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[2], 
    MIDDLE))
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#1 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[3], 
    MIDDLE), point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[1], 
    MIDDLE))
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#4 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[9], 
    MIDDLE), point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[7], 
    MIDDLE))
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#80 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[8]
    , point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[9])
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#100 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[7]
    , point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[6])
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#2 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[9]
    , point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[6])
## cercles coude
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#1 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[3], 
    MIDDLE), point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[1], 
    MIDDLE))
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#8 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[11], 
    MIDDLE), point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[13], 
    MIDDLE))
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#1000 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[23], 
    MIDDLE), point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[21], 
    MIDDLE))
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#10 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[16], 
    MIDDLE), point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[14], 
    MIDDLE))
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#100 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[0]
    , point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[1])
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#400 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[7]
    , point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[6])
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#1000 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[9]
    , point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[8])
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#400 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[12]
    , point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[13])

## milleu appuis

mdb.models['Model-full-coque'].rootAssembly.deleteMesh(regions=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#30800 ]', ), ))
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#20000 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[39], 
    MIDDLE), point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[37], 
    MIDDLE))
mdb.models['Model-full-coque'].rootAssembly.deleteMesh(regions=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#100 ]', ), ))
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#20000 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[0]
    , point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[1])
mdb.models['Model-full-coque'].rootAssembly.deleteMesh(regions=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#220040 ]', ), ))
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#200000 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[41], 
    MIDDLE), point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].InterestingPoint(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges[42], 
    MIDDLE))
mdb.models['Model-full-coque'].rootAssembly.deleteMesh(regions=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#8000 ]', ), ))
mdb.models['Model-full-coque'].rootAssembly.PartitionFaceByShortestPath(faces=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].faces.getSequenceFromMask(
    ('[#40000 ]', ), ), point1=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[1]
    , point2=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].vertices[0])

## Steps de calcul
NOMBRE_MAX_DE_MODES = 20

mdb.models['Model-full-coque'].FrequencyStep(description='Analyse modale', 
    limitSavedEigenvectorRegion=None, name="Analyse modale", numEigen=NOMBRE_MAX_DE_MODES, previous=
    'Initial')

## Sets et conditions aux limites
mdb.models['Model-full-coque'].rootAssembly.Set(edges=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges.getSequenceFromMask(
    ('[#0 #24000 ]', ), ), name='Sol')
mdb.models['Model-full-coque'].EncastreBC(createStepName='Initial', localCsys=
    None, name='Encastrement', region=
    mdb.models['Model-full-coque'].rootAssembly.sets['Sol'])
mdb.models['Model-full-coque'].rootAssembly.Set(edges=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges.getSequenceFromMask(
    ('[#11 ]', ), ), name='milieu_tube_vertical')
mdb.models['Model-full-coque'].DisplacementBC(amplitude=UNSET, createStepName=
    'Initial', distributionType=UNIFORM, fieldName='', localCsys=None, name=
    'Cerceau_tube_vertical', region=
    mdb.models['Model-full-coque'].rootAssembly.sets['milieu_tube_vertical'], 
    u1=SET, u2=UNSET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-full-coque'].rootAssembly.Set(edges=
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'].edges.getSequenceFromMask(
    ('[#440 ]', ), ), name='Milieu_tube_horizontal')
mdb.models['Model-full-coque'].DisplacementBC(amplitude=UNSET, createStepName=
    'Initial', distributionType=UNIFORM, fieldName='', localCsys=None, name=
    'Cerceau_tube_horizontal', region=
    mdb.models['Model-full-coque'].rootAssembly.sets['Milieu_tube_horizontal'], 
    u1=UNSET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)

## Mesh
mdb.models['Model-full-coque'].rootAssembly.seedPartInstance(deviationFactor=
    0.1, minSizeFactor=0.1, regions=(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'], ), size=
    200.0)
mdb.models['Model-full-coque'].rootAssembly.generateMesh(regions=(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'], ))

## Job
mdb.models['Model-full-coque'].rootAssembly.generateMesh(regions=(
    mdb.models['Model-full-coque'].rootAssembly.instances['Coude-1'], ))
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-full-coque', modelPrint=OFF
    , multiprocessingMode=DEFAULT, name='Analyse-modale-coque', 
    nodalOutputPrecision=SINGLE, numCpus=1, numGPUs=0, numThreadsPerMpiProcess=
    1, queue=None, resultsFormat=ODB, scratch='', type=ANALYSIS, 
    userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs['Analyse-modale-coque'].submit(consistencyChecking=OFF)