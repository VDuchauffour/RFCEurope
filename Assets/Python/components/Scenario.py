from CoreTypes import Civ, Scenario


try:
    from CvPythonExtensions import CyGlobalContext

    gc = CyGlobalContext()

except ImportError:
    gc = None


# duplicates with RFCUtils
def get_scenario():
    if gc is not None and gc.getPlayer(Civ.BURGUNDY.value).isPlayable():
        return Scenario.i500AD
    return Scenario.i1200AD
