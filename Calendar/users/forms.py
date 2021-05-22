from django.contrib.auth.forms import UserCreationForm


# BOYAN: Note
# The default metaclass for ModelForms is django.forms.models.ModelFormMetaclass.
# It looks for an attribute named 'Meta' and attaches to its callback so it would use
# the data specified in it instead of the default.


class UserCreationFormWithEmail(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", )
