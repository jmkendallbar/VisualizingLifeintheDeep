import textwrap
import pymel.core as pm

def getLayerObjects(layer):
    pm.mel.eval('string $layers[]={"%s"}; layerEditorSelectObjectAnimLayer($layers);' % layer)
    return pm.selected()

def setExpressionForLayerObjects():
    # get all rig controls in layer
    controls = getLayerObjects('Merged_Swim_Layer')
    # set rotateY to an expression which is the blend between anim pose and glide factor
    for control in controls:
        # array of 26 samples, 0 index is frame 1
        values = [control.rotateY.get(time=t) for t in xrange(1, 26 + 1)]
        control.rotateY.disconnect()
        # FIXME: Add interpolation between samples to smooth out slow cycles
        expr = textwrap.dedent('''
        float $values[] = {values};
        int $index = int(SWIM_CONTROL.swimY * 25);
        {control}.rotateY = $values[$index] * (1 - SWIM_CONTROL.glide);
        '''.format(values='{%s}' % ','.join([str(v) for v in values]), control=control))
        pm.expression(name='{}_swimY_expression'.format(control), string=expr)

setExpressionForLayerObjects()