import textwrap
import pymel.core as pm

def getLayerObjects(layer):
    """Get all the objects in an AnimLayer"""
    pm.mel.eval('string $layers[]={"%s"}; layerEditorSelectObjectAnimLayer($layers);' % layer)
    return pm.selected()


def setExpressionForLayerObjects():
    """
    Translate a hand animated swim cycle into a series of expressions that link
    the animated controls to simple swimY and glide controls.

    This will allow you to speed up or slow down the cycle based on simple inputs.

    To use on a new rig and swim cycle:
    - Create animation cycle
    - Add relevant controls to a single animation layer
    - Create an object called SWIM_CONTROL and create two extra attributes: swim and 
      glide which range from 0 to 1. Or, you can export SWIM_CONTROL object our sample 
      scene, Example_SwimController_ElephantSeal.ma and import into yours.
    - Run this function
    """
    # selects all rig controls in layer
    controls = getLayerObjects('Swim_Cycle')
    # set rotateY to an expression which is the blend between animation pose and glide factor
    for control in controls:
        # store rotation values for animated swim cycle
        # where values is an array of 26 values with index 0 = frame 1
        values = [control.rotate.get(time=t) for t in xrange(1, 26 + 1)]
        # free controls to allow application of expression
        control.rotateX.disconnect()
        control.rotateY.disconnect()
        control.rotateZ.disconnect()
        # create expression to:
        # 1. Allow attribute swim to control position in swim cycle via index.
        # where 0 references frame 1 and 1 references frame 26 of swim cycle
        # 2. Let attribute glide override rotations to 0 at low swim speeds.
        # where 0 indicates no glide and 1 suppresses all tail rotation

        def arrayString(i):
            return '{%s}' % ','.join([str(v[i]) for v in values])

        values_X = arrayString(0)
        values_Y = arrayString(1)
        values_Z = arrayString(2)

        expr = textwrap.dedent('''
        float $values_X[] = {values_X};
        float $values_Y[] = {values_Y};
        float $values_Z[] = {values_Z};
        
        float $exactIndex = SWIM_CONTROL.swim * 25;
        int $index = int($exactIndex);
        float $diff = $exactIndex - $index;
        
        float $value_X = $values_X[$index] * (1 - $diff) + $values_X[$index + 1] * $diff;
        {control}.rotateX = $value_X * (1 - SWIM_CONTROL.glide);  
        float $value_Y = $values_Y[$index] * (1 - $diff) + $values_Y[$index + 1] * $diff;
        {control}.rotateY = $value_Y * (1 - SWIM_CONTROL.glide);  
        float $value_Z = $values_Z[$index] * (1 - $diff) + $values_Z[$index + 1] * $diff;
        {control}.rotateZ = $value_Z * (1 - SWIM_CONTROL.glide);    
        '''.format(values_X=values_X, values_Y=values_Y, values_Z=values_Z, control=control))
        pm.expression(name='{}_swim_expression'.format(control), string=expr)

# Run function to create expressions.
setExpressionForLayerObjects()