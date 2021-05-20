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

    This will allow you to speed up or slow down the cycle based on simple
    inputs.

    To use:
    - Create anim cycle
    - Add relevant controls to a single anim layer
    - Run this function
    """
    # selects all rig controls in layer
    controls = getLayerObjects('Merged_Swim_Layer')
    # set rotateY to an expression which is the blend between animation pose and glide factor
    for control in controls:
        # store rotation values for animated swim cycle
        # where values is an array of 26 values with index 0 = frame 1
        values = [control.rotateY.get(time=t) for t in xrange(1, 26 + 1)]
        # free controls to allow application of expression
        control.rotateY.disconnect()
        # create expression to:
	    # 1. Allow attribute swimY to control position in swim cycle via index.
	    # where “0” references frame 1 and “1” references frame 26 of swim cycle
	    # 2. Let attribute glide override rotations to 0 at low swim speeds.
	    # where “0” indicates no glide and “1” suppresses all tail rotation
        expr = textwrap.dedent('''
        float $values[] = {values};
        float $exactIndex = SWIM_CONTROL.swimY * 25;
        int $index = int($exactIndex);
        float $diff = $exactIndex - $index;

        float $value = $values[$index] * (1 - $diff) + $values[$index + 1] * $diff;
        {control}.rotateY = $value * (1 - SWIM_CONTROL.glide);    
        '''.format(values='{%s}' % ','.join([str(v) for v in values]), control=control))
        pm.expression(name='{}_swimY_expression'.format(control), string=expr)

# Run function to create expressions.
setExpressionForLayerObjects()