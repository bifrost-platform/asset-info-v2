from pydantic import FilePath, BaseModel


class File(BaseModel):
    """Information about each file.

    Attributes:
        path: The path of the file. (:class:`FilePath`: constrained :class:`Path`)
        name: The name of the file. (:class:`str`)
    """

    path: FilePath
    name: str
