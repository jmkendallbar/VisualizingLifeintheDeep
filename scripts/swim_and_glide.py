import textwrap
import pymel.core as pm

def getLayerObjects(layer):
    pm.mel.eval('string $layers[]={"%s"}; layerEditorSelectObjectAnimLayer($layers);' % layer)
    return pm.selected()

# This function creates expressions linking swimY and glide controllers to model's rig controls
def setExpressionForLayerObjects():
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
	    # where “0” references frame 1 and “1” references frame 25 of swim cycle
	    # 2. Let attribute glide override rotations to 0 at low swim speeds.
	    # where “0” indicates no glide and “1” suppresses all tail rotation
        # FIXME: Add interpolation between samples to smooth out slow cycles
        expr = textwrap.dedent('''
        float $values[] = {values};
        int $index = int(SWIM_CONTROL.swimY * 25);
        {control}.rotateY = $values[$index] * (1 - SWIM_CONTROL.glide);
        '''.format(values='{%s}' % ','.join([str(v) for v in values]), control=control))
        pm.expression(name='{}_swimY_expression'.format(control), string=expr)

# Run function to create expressions.
setExpressionForLayerObjects()