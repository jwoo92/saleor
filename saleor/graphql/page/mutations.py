import graphene

from ...page import models
from ..core.mutations import ModelDeleteMutation, ModelMutation
from ..core.types import SeoInput
from ..core.utils import clean_seo_fields


class PageInput(graphene.InputObjectType):
    slug = graphene.String()
    title = graphene.String()
    content = graphene.String()
    is_visible = graphene.Boolean(required=True)
    available_on = graphene.String()
    seo = SeoInput(description='Search engine optimization fields.')


class PageCreate(ModelMutation):
    class Arguments:
        input = PageInput(
            required=True, description='Fields required to create a page.')

    class Meta:
        description = 'Creates a new page.'
        model = models.Page

    @classmethod
    def user_is_allowed(cls, user, input):
        return user.has_perm('page.edit_page')

    @classmethod
    def clean_input(cls, info, instance, input, errors):
        cleaned_input = super().clean_input(info, instance, input, errors)
        clean_seo_fields(cleaned_input)
        return cleaned_input


class PageUpdate(PageCreate):
    class Arguments:
        id = graphene.ID(required=True, description='ID of a page to update.')
        input = PageInput(
            required=True, description='Fields required to update a page.')

    class Meta:
        description = 'Updates an existing page.'
        model = models.Page


class PageDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description='ID of a page to delete.')

    class Meta:
        description = 'Deletes a page.'
        model = models.Page

    @classmethod
    def user_is_allowed(cls, user, input):
        return user.has_perm('page.edit_page')
