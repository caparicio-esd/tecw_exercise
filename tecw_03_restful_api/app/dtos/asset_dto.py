"""
dtos/asset_dto.py — Data Transfer Objects for Asset.

Classes:
  AssetDTO       — outbound: model → JSON (camelCase)
  CreateAssetDTO — inbound:  JSON → new model
"""

from dataclasses import dataclass

from .utils import camelize


@dataclass
class AssetDTO:
    """Outbound representation of an Asset (model → JSON)."""

    id:  int
    url: str

    @staticmethod
    def from_model(asset) -> dict:
        """Serialize an Asset ORM instance to a camelCase dict ready for jsonify."""
        return camelize({
            'id':  asset.id,
            'url': asset.url,
        })


@dataclass
class CreateAssetDTO:
    """Inbound payload for registering a new asset (JSON → model)."""

    url: str

    @staticmethod
    def from_request(data: dict) -> 'CreateAssetDTO':
        """Parse a request body dict into a CreateAssetDTO. Raises KeyError if a required field is missing."""
        return CreateAssetDTO(url=data['url'])
