"""
Room

Rooms are simple containers that has no location of their own.

"""
from collections import defaultdict

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

    def get_display_desc(self, looker, **kwargs):
        """
                Get the 'desc' component of the object description. Called by `return_appearance`.

                Args:
                    looker (Object): Object doing the looking.
                    **kwargs: Arbitrary data for use when overriding.
                Returns:
                    str: The desc display string..

                """
        if self.db.desc:
            if self.db.outdoors:
                return self.db.desc + "\n" + GLOBAL_SCRIPTS.weather.get_time() + ". " + GLOBAL_SCRIPTS.weather.get_weather() + "|n"
            else:
                return self.db.desc + "\n" + GLOBAL_SCRIPTS.weather.get_time() + "|n"

        else:
            if self.db.outdoors:
                return "You see nothing special.\n" + GLOBAL_SCRIPTS.weather.get_time() + ". " + GLOBAL_SCRIPTS.weather.get_weather() + "|n"
            else:
                return "You see nothing special.\n" + GLOBAL_SCRIPTS.weather.get_time() + "|n"

    def get_display_things(self, looker, **kwargs):
        """
                Get the 'things' component of the object description. Called by `return_appearance`.

                Args:
                    looker (Object): Object doing the looking.
                    **kwargs: Arbitrary data for use when overriding.
                Returns:
                    str: The things display data.

                """

        def _filter_visible(obj_list):
            return (obj for obj in obj_list if obj != looker and obj.access(looker, "view"))

        # sort and handle same-named things
        things = _filter_visible(self.contents_get(content_type="object"))

        grouped_things = defaultdict(list)
        for thing in things:
            grouped_things[thing.get_display_name(looker, **kwargs)].append(thing)

        thing_names = []
        for thingname, thinglist in sorted(grouped_things.items()):
            nthings = len(thinglist)
            thing = thinglist[0]
            singular, plural = thing.get_numbered_name(nthings, looker, key=thingname)
            thing_names.append(singular if nthings == 1 else plural)
        thing_names = "\n\t".join(thing_names)
        return f"\n|wYou see:\n\t|n{thing_names}" if thing_names else ""

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
        exit_names = '\n\t'.join(exi.get_display_name(looker, **kwargs) for exi in exits)

        return f"|wObvious Exits:|n\n\t{exit_names}" if exit_names else ""
