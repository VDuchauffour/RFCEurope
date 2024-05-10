import CvEventManager
import CvRFCEventHandler
import RiseAndFall
import Crusades
import Religions
import Barbs
import Modifiers
import Locations


class CvRFCEventManager(CvEventManager.CvEventManager, object):

    """Extends the standard event manager by adding support for multiple
    handlers for each event.

    Methods exist for both adding and removing event handlers.  A set method
    also exists to override the default handlers.  Clients should not depend
    on event handlers being called in a particular order.

    This approach works best with mods that have implemented the design
    pattern suggested on Apolyton by dsplaisted.

    http://apolyton.net/forums/showthread.php?s=658a68df728b2719e9ebfe842d784002&threadid=142916

    The example given in the 8th post in the thread would be handled by adding
    the following lines to the CvCustomEventManager constructor.  The RealFort,
    TechConquest, and CulturalDecay classes can remain unmodified.

            self.addEventHandler("unitMove", rf.onUnitMove)
            self.addEventHandler("improvementBuilt", rf.onImprovementBuilt)
            self.addEventHandler("techAcquired", rf.onTechAcquired)
            self.addEventHandler("cityAcquired", tc.onCityAcquired)
            self.addEventHandler("EndGameTurn", cd.onEndGameTurn)

    Note that the naming conventions for the event type strings vary from event
    to event.  Some use initial capitalization, some do not; some eliminate the
    "on..." prefix used in the event handler function name, some do not.  Look
    at the unmodified CvEventManager.py source code to determine the correct
    name for a particular event.

    Take care with event handlers that also extend CvEventManager.  Since
    this event manager handles invocation of the base class handler function,
    additional handlers should not also call the base class function themselves.

    """

    def __init__(self, *args, **kwargs):
        super(CvRFCEventManager, self).__init__(*args, **kwargs)
        # map the initial EventHandlerMap values into the new data structure
        Locations.setup()
        Modifiers.setup()

        for eventType, eventHandler in self.EventHandlerMap.iteritems():
            self.setEventHandler(eventType, eventHandler)

        self.CustomEvents = {
            7614: ("RiseAndFallPopupEvent", self.rnfEventApply7614, self.rnfEventBegin7614),
            7615: ("FlipPopupEvent", self.rnfEventApply7615, self.rnfEventBegin7615),
            7616: ("CrusadeInitVoteEvent", self.crusadeApply7616, self.crusadeBegin7616),
            7617: ("InformForLeaderPopup", self.crusadeApply7617, self.crusadeBegin7617),
            7618: ("HumanVotePopup", self.crusadeApply7618, self.crusadeBegin7618),
            7619: ("HumanDeviate", self.crusadeApply7619, self.crusadeBegin7619),
            7620: ("ChoseNewCrusadeTarget", self.crusadeApply7620, self.crusadeBegin7620),
            7621: ("Under Attack", self.crusadeApply7621, self.crusadeBegin7621),
            7622: ("ResurrectionEvent", self.rnfEventApply7622, self.rnfEventBegin7622),
            7624: (
                "ReformationEvent",
                self.relEventApply7624,
                self.relEventBegin7624,
            ),  ### Reformation Begin ###
            7625: ("DefensiveCrusadeEvent", self.crusadeApply7625, self.crusadeBegin7625),
            7626: ("CounterReformationEvent", self.relEventApply7626, self.relEventBegin7626),
            7627: ("CounterReformationEvent", self.barbEventApply7627, self.barbEventBegin7627),
            7628: (
                "Religious Persecution",
                self.relEventApply7628,
                self.relEventBegin7628,
            ),  # Absinthe: persecution popup
            7629: (
                "Free Religious Revolution",
                self.relEventApply7629,
                self.relEventBegin7629,
            ),  # Absinthe: free religion change
        }

        # --> INSERT EVENT HANDLER INITIALIZATION HERE <--
        CvRFCEventHandler.CvRFCEventHandler(self)
        self.rnf = RiseAndFall.RiseAndFall()
        self.crus = Crusades.Crusades()
        self.rel = Religions.Religions()
        self.barb = Barbs.Barbs()

    def setPopupHandler(self, eventType, handler):
        """Removes all previously installed popup handlers for the given
        event type and installs a new pair of handlers.

        The eventType should be an integer.  It must be unique with respect
        to the integers assigned to built in events.  The popupHandler should
        be a list made up of (name, applyFunction, beginFunction).  The name
        is used in debugging output.  The begin and apply functions are invoked
        by beginEvent and applyEvent, respectively, to manage a popup dialog
        in response to the event.
        """

        self.Events[eventType] = handler

    def setPopupHandlers(self, eventType, name, beginFunction, applyFunction):
        """Builds a handler tuple to pass to setPopupHandler()."""

        self.setPopupHandler(eventType, (name, applyFunction, beginFunction))

    def removePopupHandler(self, eventType):
        """Removes all previously installed popup handlers for the given
        event type.

        The eventType should be an integer. It is an error to fire this
        eventType after removing its handlers.
        """

        if eventType in self.Events:
            del self.Events[eventType]

    def addEventHandler(self, eventType, eventHandler):
        """Adds a handler for the given event type.

        A list of supported event types can be found in the initialization
        of EventHandlerMap in the CvEventManager class.

        """
        self.EventHandlerMap[eventType].append(eventHandler)

    def removeEventHandler(self, eventType, eventHandler):
        """Removes a handler for the given event type.

        A list of supported event types can be found in the initialization
        of EventHandlerMap in the CvEventManager class.  It is an error if
        the given handler is not found in the list of installed handlers.

        """
        self.EventHandlerMap[eventType].remove(eventHandler)

    def setEventHandler(self, eventType, eventHandler):
        """Removes all previously installed event handlers for the given
        event type and installs a new handler .

        A list of supported event types can be found in the initialization
        of EventHandlerMap in the CvEventManager class.  This method is
        primarily useful for overriding, rather than extending, the default
        event handler functionality.

        """
        self.EventHandlerMap[eventType] = [eventHandler]

    def handleEvent(self, argsList):
        """Handles events by calling all installed handlers."""
        self.origArgsList = argsList
        flagsIndex = len(argsList) - 6
        (
            self.bDbg,
            self.bMultiPlayer,
            self.bAlt,
            self.bCtrl,
            self.bShift,
            self.bAllowCheats,
        ) = argsList[flagsIndex:]
        eventType = argsList[0]
        return {
            "kbdEvent": self._handleConsumableEvent,
            "mouseEvent": self._handleConsumableEvent,
            "OnSave": self._handleOnSaveEvent,
            "OnLoad": self._handleOnLoadEvent,
        }.get(eventType, self._handleDefaultEvent)(eventType, argsList[1:])

    def _handleDefaultEvent(self, eventType, argsList):
        if self.EventHandlerMap.has_key(eventType):
            for eventHandler in self.EventHandlerMap[eventType]:
                # the last 6 arguments are for internal use by handleEvent
                eventHandler(argsList[: len(argsList) - 6])

    def _handleConsumableEvent(self, eventType, argsList):
        """Handles events that can be consumed by the handlers, such as
        keyboard or mouse events.

        If a handler returns non-zero, processing is terminated, and no
        subsequent handlers are invoked.

        """
        if self.EventHandlerMap.has_key(eventType):
            for eventHandler in self.EventHandlerMap[eventType]:
                # the last 6 arguments are for internal use by handleEvent
                result = eventHandler(argsList[: len(argsList) - 6])
                if result > 0:
                    return result
        return 0

    # TODO: this probably needs to be more complex
    def _handleOnSaveEvent(self, eventType, argsList):
        """Handles OnSave events by concatenating the results obtained
        from each handler to form an overall consolidated save string.

        """
        result = ""
        if self.EventHandlerMap.has_key(eventType):
            for eventHandler in self.EventHandlerMap[eventType]:
                # the last 6 arguments are for internal use by handleEvent
                result = result + eventHandler(argsList[: len(argsList) - 6])
        return result

    # TODO: this probably needs to be more complex
    def _handleOnLoadEvent(self, eventType, argsList):
        """Handles OnLoad events."""
        return self._handleDefaultEvent(eventType, argsList)

    # popup event handlers
    def beginEvent(self, context, argsList=-1):
        """Begin Event"""
        if self.CustomEvents.has_key(context):
            return self.CustomEvents[context][2](argsList)
        else:
            super(CvRFCEventManager, self).beginEvent(context, argsList)

    def applyEvent(self, argsList):
        """Apply the effects of an event"""
        context, playerID, netUserData, popupReturn = argsList

        if self.CustomEvents.has_key(context):
            entry = self.CustomEvents[context]
            # the apply function
            return entry[1](playerID, netUserData, popupReturn)
        else:
            return super(CvRFCEventManager, self).applyEvent(argsList)

    # popup events
    def rnfEventBegin7614(self):
        pass

    def rnfEventApply7614(self, playerID, netUserData, popupReturn):
        self.rnf.eventApply7614(popupReturn)

    def rnfEventBegin7615(self):
        pass

    def rnfEventApply7615(self, playerID, netUserData, popupReturn):  # 3Miro: flip
        self.rnf.eventApply7615(popupReturn)

    def crusadeBegin7616(self):
        pass

    def crusadeApply7616(self, playerID, netUserData, popupReturn):
        self.crus.eventApply7616(popupReturn)

    def crusadeBegin7617(self):
        pass

    def crusadeApply7617(self, playerID, netUserData, popupReturn):
        pass

    def crusadeBegin7618(self):
        pass

    def crusadeApply7618(self, playerID, netUserData, popupReturn):
        self.crus.eventApply7618(popupReturn)

    def crusadeBegin7619(self):
        pass

    def crusadeApply7619(self, playerID, netUserData, popupReturn):
        self.crus.eventApply7619(popupReturn)

    def crusadeBegin7620(self):
        pass

    def crusadeApply7620(self, playerID, netUserData, popupReturn):
        self.crus.eventApply7620(popupReturn)

    def crusadeBegin7621(self):
        pass

    def crusadeApply7621(self, playerID, netUserData, popupReturn):
        pass

    def rnfEventBegin7622(self):
        pass

    def rnfEventApply7622(self, playerID, netUserData, popupReturn):  # 3Miro: rebel
        self.rnf.eventApply7622(popupReturn)

    ### Begin Reformation ###
    def relEventBegin7624(self):
        pass

    def relEventApply7624(self, playerID, netUserData, popupReturn):
        self.rel.eventApply7624(popupReturn)

    def relEventBegin7626(self):
        pass

    def relEventApply7626(self, playerID, netUserData, popupReturn):
        self.rel.eventApply7626(popupReturn)

    ### End Reformation ###

    def crusadeBegin7625(self):
        pass

    def crusadeApply7625(self, playerID, netUserData, popupReturn):
        self.crus.eventApply7625(popupReturn)

    def barbEventBegin7627(self):
        pass

    def barbEventApply7627(self, playerID, netUserData, popupReturn):
        self.barb.eventApply7627(popupReturn)

    # Absinthe: persecution popup
    def relEventBegin7628(self):
        pass

    def relEventApply7628(self, playerID, netUserData, popupReturn):
        self.rel.eventApply7628(popupReturn)

    # Absinthe: end

    # Absinthe: free religion change
    def relEventBegin7629(self):
        pass

    def relEventApply7629(self, playerID, netUserData, popupReturn):
        self.rel.eventApply7629(playerID, popupReturn)

    # Absinthe: end
