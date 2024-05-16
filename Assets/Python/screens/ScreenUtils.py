def getNextWidgetName(screen):
    """Returns a unique ID for a widget in this screen"""
    assert hasattr(screen, "WIDGET_ID")
    assert hasattr(screen, "nWidgetCount")

    szName = screen.WIDGET_ID + str(screen.nWidgetCount)
    screen.nWidgetCount += 1
    return szName
