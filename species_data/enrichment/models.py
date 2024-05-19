import datetime
import logging
import decimal
import enum

from typing import Tuple, Type, Optional, Set, Any

from django.db.models.fields.related import ManyToManyField
from langchain_core.pydantic_v1 import (
    BaseModel,
    Field,
    create_model,
)
from species_data.models import SpeciesProperties
from species_data.models.base import CategorizedPlantPropertyBase
from species_data.fields import DecimalEstimatedRange, DurationEstimatedRange


logger = logging.getLogger(__name__)


def get_species_data_model():
    """Generates a Pydantic model based on the Django models for plant species data categories."""

    class ConfidenceModel(BaseModel):
        confidence: decimal.Decimal = Field(gt=0, lt=1, decimal_places=1, max_digits=2)

    class DecimalRangeField(ConfidenceModel):
        minimum: Optional[decimal.Decimal] = Field(max_digits=3, decimal_places=1)
        typical: Optional[decimal.Decimal] = Field(max_digits=3, decimal_places=1)
        maximum: Optional[decimal.Decimal] = Field(max_digits=3, decimal_places=1)

    class DurationRangeField(ConfidenceModel):
        minimum: Optional[datetime.timedelta]
        typical: Optional[datetime.timedelta]
        maximum: Optional[datetime.timedelta]

    def generate_django_enum(django_model: Type[CategorizedPlantPropertyBase]) -> Any:
        """Generates a string Enum based on the name field of the Django model instances."""
        # Retrieve all distinct name values from the Django model
        objects = django_model.objects.all()

        obj_dict = {obj.slug: obj.slug for obj in objects}

        # Create and return an enum with a name based on the Django model's name
        obj_enum = enum.Enum(f"{django_model.__name__}Enum", obj_dict)
        return obj_enum

    def generate_django_multiselect_field(
        django_model: Type[CategorizedPlantPropertyBase],
    ) -> Type[BaseModel]:
        """Generates a field allowing the selection of multiple options based on a given Django model."""
        model_enum = generate_django_enum(django_model)

        model = create_model(
            f"{django_model.__name__}Model",
            __base__=ConfidenceModel,
            values=(Set[model_enum], ...),
        )

        return model

    def get_model_field(property_field) -> Optional[Tuple[str, Tuple[Any, Any]]]:
        """Determine the Django model field type based on the property field type."""
        field_type = None
        if isinstance(property_field, DecimalEstimatedRange):
            logger.info(f"Adding DecimalRangeField property '{property_field}'.")
            field_type = DecimalRangeField

        elif isinstance(property_field, DurationEstimatedRange):
            logger.info(f"Adding DecimalRangeField property '{property_field}'.")
            field_type = DurationRangeField

        elif isinstance(property_field, ManyToManyField) and issubclass(
            property_field.related_model, CategorizedPlantPropertyBase
        ):
            logger.info(f"Adding multiselect property '{property_field}'.")
            field_type = generate_django_multiselect_field(property_field.related_model)

        if field_type:
            return property_field.name, (field_type, ...)

        return None

    model_fields = {
        result[0]: result[1]
        for property_field in SpeciesProperties._meta.get_fields()
        for result in [get_model_field(property_field)]
        if result is not None
    }

    model = create_model("SpeciesData", **model_fields)  # type: ignore

    return model
