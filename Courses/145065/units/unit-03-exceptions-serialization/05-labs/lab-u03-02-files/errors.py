# errors.py
# Every error the Line 3 model raises on purpose.
# Lab U03-02 version: the Monday family plus the file errors. GIVEN.
#
# Derived from the plant-model anchor, stage 3 (errors.py), plus one lab-only
# class, UnknownEquipmentError, for a tag that is not on the line.
#
#     PlantError                              catch this to catch all of them
#     |-- ConfigurationError (also ValueError)   a value the model refuses
#     |-- EquipmentError                         carries asset_tag
#     |   |-- LockoutError                       locked out, or the wrong badge
#     |   |-- EquipmentStateError                wrong state: guard open, not running
#     |   `-- UnknownEquipmentError             no such tag on this line
#     `-- PlantFileError                         saving or loading failed; carries source
#         |-- PlantFileMissingError (also FileNotFoundError)
#         `-- PlantFileFormatError               not a valid plant file; carries where
#             `-- UnsupportedVersionError        written by a newer program


class PlantError(Exception):
    """Root of the Line 3 error family. except PlantError catches every one."""


class ConfigurationError(PlantError, ValueError):
    """A value the model will not accept.

    It also inherits ValueError, on purpose. Code written last week says
    `except ValueError`, and it keeps working after the model switched to this
    class. That is how you change an error type without breaking callers.
    """


class EquipmentError(PlantError):
    """A piece of equipment refused an operation. Carries the asset tag."""

    def __init__(self, asset_tag, message):
        # Store the tag as data, so a handler can act on it without parsing text.
        self.asset_tag = asset_tag
        super().__init__(f"{asset_tag}: {message}")


class LockoutError(EquipmentError):
    """The equipment is locked out, or the badge does not hold the lock."""


class EquipmentStateError(EquipmentError):
    """The equipment is in the wrong state for this operation."""


class UnknownEquipmentError(EquipmentError):
    """The tag is well formed, and nothing on this line carries it."""


class PlantFileError(PlantError):
    """Saving or loading a plant file failed. Carries the file it was about."""

    def __init__(self, source, message):
        self.source = str(source)
        super().__init__(f"{source}: {message}")


class PlantFileMissingError(PlantFileError, FileNotFoundError):
    """The plant file is not there. Old `except FileNotFoundError` code still catches it."""


class PlantFileFormatError(PlantFileError):
    """The file exists and is not a valid plant file.

    where is a path into the document, such as line.cells[0].items[1].rated_kw,
    so the person fixing the file knows exactly where to look.
    """

    def __init__(self, source, where, problem):
        self.where = where
        self.problem = problem
        super().__init__(source, f"{where}: {problem}")


class UnsupportedVersionError(PlantFileFormatError):
    """The file was written by a newer version of the program."""

    def __init__(self, source, version, newest):
        self.version = version
        super().__init__(source, "version",
                         f"format version {version} is newer than {newest}, the newest this program reads")
