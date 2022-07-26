from typing import List
from fastapi import (
    APIRouter,
    Depends,
    status,
    exceptions
)
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories.artist import ArtistRepository
from repositories.album import AlbumRepository
from repositories.track import TrackRepository
from schemas.artist import (
    ArtistNameSchema,
    ArtistSchema
)
from schemas.album import (
    AlbumSchema,
    AlbumTitleSchema
)
from schemas.track import (
    TrackSchema,
    TrackInfoSchema
)
from exceptions.not_found import ArtistNotFoundError

router = APIRouter(
    tags=["Singers"],
)


@router.get(
    "/singers/",
    response_model=List[ArtistNameSchema],
    status_code=status.HTTP_200_OK
)
# Depends Shortcut
# see: https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/#shortcut     # noqa: E501
def get_all(
    db: Session = Depends(get_db),
    artist_repository: ArtistRepository = Depends()
) -> List[ArtistSchema]:
    """
    Get All Artists

    :param db: Database Session
    :param artist_repository: Artist Repository

    :return: List of Artists
    """

    return artist_repository.get_all(db)


@router.get(
    "/singers/{artist_id}/",
    response_model=List[AlbumTitleSchema],
    status_code=status.HTTP_200_OK
)
def get_albums_by_artist(
    artist_id: int,
    db: Session = Depends(get_db),
    artist_repository: ArtistRepository = Depends(),
    album_repository: AlbumRepository = Depends()
) -> List[AlbumSchema]:
    """
    Get All Albums by Artist

    :param artist_id: Artist ID

    :param db: Database Session

    :param artist_repository: Artist Repository

    :param album_repository: Album Repository

    :return: List of Albums
    """
    try:
        artist_repository.get_by_id(db, artist_id)
    except ArtistNotFoundError as e:
        raise exceptions.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    return album_repository.get_by_artist_id(db, artist_id)


@router.get(
    "/singer/{artist_id}/",
    response_model=List[TrackInfoSchema],
    status_code=status.HTTP_200_OK
)
def get_tracks_by_artist(
    artist_id: int,
    db: Session = Depends(get_db),
    artist_repository: ArtistRepository = Depends(),
    track_repository: TrackRepository = Depends()
) -> List[TrackSchema]:
    """
    Get All Tracks by Artist

    :param artist_id: Artist ID

    :param db: Database Session

    :param artist_repository: Artist Repository

    :param track_repository: Track Repository

    :return: List of Tracks
    """
    try:
        artist_repository.get_by_id(db, artist_id)
    except ArtistNotFoundError as e:
        raise exceptions.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    return track_repository.get_by_artist_id(db, artist_id)
