"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.objects.objects import DefaultRoom
from evennia.utils import iter_to_str

from .objects import ObjectParent
from evennia import GLOBAL_SCRIPTS


class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    pass

    def at_object_creation(self):
        """
        Called once, when the object is first created.
        """

        super().at_object_creation()
        self.db.outdoors = True

    def return_appearance(self, looker, **kwargs):
        return \
            GLOBAL_SCRIPTS.weather.get_time() + \
            GLOBAL_SCRIPTS.weather.get_weather() + \
            + super().return_appearance(looker, **kwargs)

    def get_display_exits(self, looker, **kwargs):
        """
                Get the 'exits' component of the object description. Called by `return_appearance`.

                Args:
                    looker (Object): Object doing the looking.
                    **kwargs: Arbitrary data for use when overriding.
                Returns:
                    str: The exits display data.

                """

        def _filter_visible(obj_list):
            return (obj for obj in obj_list if obj != looker and obj.access(looker, "view"))

        exits = _filter_visible(self.contents_get(content_type="exit"))
        exit_names = '\n'.join(exi.get_display_name(looker, **kwargs) for exi in exits)

        return f"|wObvious Exits:|n\n{exit_names}" if exit_names else ""
