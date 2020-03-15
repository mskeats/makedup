import poser
import re
import random


def eventCallbackFunc(iScene, iEventType):
    if(iEventType & poser.kEventCodeACTORSELECTIONCHANGED):

        if re.match("dragon.*",iScene.CurrentActor().Name()):
            oChildFigname = iScene.CurrentActor().CustomData("dragonchild")
            oFigure = iScene.Figure(oChildFigname)
            dVisibility = 1 - iScene.CurrentActor().CustomData("dragonVisibility")
            iScene.CurrentActor().SetCustomData("dragonVisibility", dVisibility, 0 ,0 )

            oFigure.SetOnOff(dVisibility)
            scene.DrawAll()
            
# ----------------------------------------------
# Returns a list of props based on a patter name
# ----------------------------------------------
def getPropbyName( sPattern ):
    oFoundProps = []

    for oActor in poser.Scene().Actors():
        if oActor.IsProp() and re.match(sPattern,oActor.Name()):
            oFoundProps.append(oActor)

    return oFoundProps

#-------------------------------------------------------
def copyParams (aParams, oSrc, oDest):
    
    for aParam in aParams:
        oDest.Parameter(aParam).SetValue(oSrc.Parameter(aParam).Value())
        
#---------------------------------------------------------
def Duplicate( oActor):
    scene.SelectActor(oActor)
    poser.ProcessCommand( 1568 )
    return scene.CurrentActor()

# --------------------------------------------------------
def FindBaseActor( oActor):
    
    if oActor.Parent():
        while oActor.Parent().Name() != "UNIVERSE":
            oActor = oActor.Parent()

    return oActor

# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
scene = poser.Scene()
oActor = FindBaseActor(scene.CurrentActor())
oProps = getPropbyName("dragon.*")


#while oActor.Parent().Name() != "UNIVERSE":
#     oActor = oActor.Parent()

ParamsToCopy = ["xTran","yTran","zTran","scale","xRotate","yRotate","zRotate"]

for oProp in oProps:
    
    sFigureName = oProp.CustomData("dragonchild")
    
    if sFigureName:
        
        oFigure = scene.Figure(sFigureName)
        oNewActor = FindBaseActor(oFigure.ParentActor())
        
    else:
        
        oNewActor = FindBaseActor(Duplicate(oActor))
        oFigure = oNewActor.ItsFigure()
        
        if oFigure:
            dFrameNum =random.randint(0,scene.NumFrames() - 1)
            scene.SetFrame(dFrameNum)
            oFigure.Memorize()
            scene.SetFrame(0)
            oFigure.Reset()
            oProp.SetCustomData("dragonchild", oFigure.Name(),0,0)
            oProp.SetCustomData("dragonVisibility", 0,0,0)
            
            oFigure.SetOnOff(0)
       
    copyParams(ParamsToCopy,oProp,oNewActor)
 
scene.DrawAll()
scene.SetEventCallback(eventCallbackFunc)

#for oProp in oProps:
#    print oProp.Name(),oProp.Parameter("scale").Value(),
#    print oProp.Parameter("xTran").Value(), oProp.Parameter("yTran").Value(), oProp.Parameter("zTran").Value()
#    print oProp.Parameter("xRotate").Value(), oProp.Parameter("yRotate").Value(), oProp.Parameter("zRotate").Value()
    





