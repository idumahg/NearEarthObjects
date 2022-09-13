"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether
    it's marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments.
        """
        # did not realize I was suppose to unpack the info argument
        # then I saw it done in someone's work in Knowledge.
        self.designation = info["pdes"]

        if info["name"] == "":
            self.name = None
        else:
            self.name = info["name"]

        if info["diameter"] == "":
            self.diameter = float('nan')
        else:
            self.diameter = float(info["diameter"])

        self.hazardous = info["pha"]

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name is None:
            return f'{self.designation}'
        else:
            return f'{self.designation} {(self.name)}'

    @property
    def serialize(self):
        """Return dict of relevant attributes for CSV or JSON serialization."""
        result_dict = {'designation': self.designation,
                       'name': self.name, 'diameter_km': self.diameter,
                       'potentially_hazardous': self.hazardous}

        return result_dict

    def __str__(self):
        """Return `str(self)`."""
        if self.hazardous:
            return f"A NearEarthObject {self.fullname} has a diameter of " \
                   f"{self.diameter:.3f} km and is potentially hazardous."
        else:
            return f"A NearEarthObject {self.fullname} has a diameter of " \
                   f"{self.diameter:.3f} km and is not potentially hazardous."

    def __repr__(self):
        """Return a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, "
                f"name={self.name!r}, " f"diameter={self.diameter:.3f}, "
                f"hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    to Earth, such as the date and time (in UTC) of closest approach,
    the nominal approach distance in astronomical units, and the relative
    approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments.
        """
        # did not realize I was suppose to unpack the info argument
        # then I saw it done in someone's work in Knowledge.
        self._designation = info["des"]

        self.time = cd_to_datetime(info["cd"])
        self.distance = float(info["dist"])
        self.velocity = float(info["v_rel"])

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of the Class's approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't
        exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return f'{datetime_to_str(self.time)}'

    @property
    def serialize(self):
        """Return dict of relevant attributes for CSV or JSON serialization."""
        result_dict = {'datetime_utc': self.time_str,
                       'distance_au': self.distance,
                       'velocity_km_s': self.velocity}

        return result_dict

    def __str__(self):
        """Return `str(self)`."""
        return f"On {self.time_str} approaches Earth at a distance of " \
               f"{self.distance:.2f} au and a velocity of " \
               f"{self.velocity} km/s)"

    def __repr__(self):
        """Return a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, "
                f"distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
