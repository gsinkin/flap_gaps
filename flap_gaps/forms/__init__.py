from __future__ import unicode_literals
import re
from wtforms import PasswordField
from wtforms import validators
from wtforms import Form
from wtforms import FormField
from wtforms import TextField
from wtforms import ValidationError
from flap_gaps.lib.formatting_utils import format_phone
from flap_gaps.lib.formatting_utils import format_percent

NUMBER_RE = re.compile(r"\d+")


def strip(value):
    return value.strip() if value else None


def lower_filter(value):
    return value.lower() if value else None


def password_field(label="Password", required=True):
    v = [validators.length(min=6)]
    if required:
        v.append(validators.required())
    return PasswordField(label, v)


class PercentageField(TextField):

    def _value(self):
        if self.data and not self.errors:
            return format_percent(self.data)
        elif self.raw_data:
            return self.raw_data[0]
        else:
            return u""

    def process_formdata(self, valuelist):
        if not valuelist:
            return
        percent_str = u" ".join(valuelist)
        digits = re.sub("[^\d.]", "", percent_str)
        try:
            self.data = float(digits) / 100.0
        except ValueError:
            self.data = None

    def post_validate(self, form, stop_validation):
        if stop_validation:
            return
        if self.raw_data and self.raw_data[0]:
            if self.data is None:
                raise ValidationError(
                    "Value must be between 0 and 100")
            elif self.data >= 1.0:
                raise ValidationError(
                    "Value must be less than or equal to 100")
            elif self.data < 0:
                raise ValidationError(
                    "Value must be greater than or equal to 0")


class PhoneNumberField(TextField):

    def _value(self):
        if self.data and not self.errors:
            return format_phone(self.data)
        elif self.raw_data:
            return self.raw_data[0]
        else:
            return u""

    def process_formdata(self, valuelist):
        if not valuelist:
            return
        phone_str = u" ".join(valuelist)
        digits = re.sub("[^\d]", "", phone_str)
        if len(digits) >= 10:
            self.data = digits
        else:
            self.data = None

    def post_validate(self, form, stop_validation):
        if stop_validation:
            return
        if self.raw_data and self.raw_data[0]:
            if not self.data or len(self.data) < 10:
                raise ValidationError(
                    "Phone numbers must have at least 10 digits")


class DBMappedForm(Form):
    """
    A base class for forms whose values directly map to database models.
    Example usage:
      (Assuming the SQLAlchemy model is "Account")

    class UserAccountForm(DBMappedForm):
      first_name = TextField("First Name", [validators.required(),
                                            mapped(Account.first_name)])
      last_name = TextField("Last Name", [validators.required(),
                                          mapped(Account.last_name)])
      email_address = TextField("E-Mail", [validators.required(),
                                           mapped(Account.email_address)])

    # Load form values from WSGI input
    form = UserAccountForm(wsgi_request.form)

    # Populate a DB object with the form values:
    account_obj = session.query(Account).get(id)
    form.fill_db_object(account_obj)


    # Populate a form from a DB object
    other_account_obj = session.query(Account).get(other_id)
    form.from_db_object(other_account_obj)

    """

    @property
    def mapped_fields(self):
        """
        Yield all fields that are mapped to a DB column.
        """
        for field in self:
            if field.flags.db_mapped:
                yield field

    def mappings(self, db_object):
        """
        Yield tuples (form_field, mapped_field) for all mapped form fields.
        """
        for field in self.mapped_fields:
            for validator in field.validators:
                if not isinstance(validator, Mapped):
                    continue
                if validator.has_mapping_for(db_object):
                    yield field, validator

    @property
    def subforms(self):
        for field in self:
            if isinstance(field, FormField):
                if (hasattr(field.form_class, "fill_db_object") and
                    hasattr(field.form_class, "from_db_object")):
                    yield field

    def fill_db_object(self, db_object):
        for form_field, db_mapping in self.mappings(db_object):
            db_mapping.set_db_object_value(db_object, form_field.data)

        for subform in self.subforms:
            subform.fill_db_object(db_object)

        self.post_fill(db_object)

    def fill_db_objects(self, *objects):
        for o in objects:
            self.fill_db_object(o)

    def from_db_object(self, db_object):
        for form_field, db_mapping in self.mappings(db_object):
            db_value = db_mapping.db_object_value(db_object)
            try:
                default_value = form_field.default()
            except TypeError:
                default_value = form_field.default
            form_field.data = db_value or default_value

        for subform in self.subforms:
            subform.from_db_object(db_object)

        self.post_from(db_object)

    def from_db_objects(self, *objects):
        for o in objects:
            self.from_db_object(o)

    def post_fill(self, db_object):
        """
        Called after fields have been set by fill_db_object().

        Override this method in your subclass if you want some additional
        behavior after filling a DB object from a form.
        """
        pass

    def post_from(self, db_object):
        """
        Called after the form fields have been filled from a DB
        object in from_db_object().

        Override this method in your subclass if you want some additional
        behavior after filling the from from a DB object.
        """
        pass


class Mapped(object):
    """
    A "validator" to support the database object mapping in DBMappedForm.
    This does not do any real validaton, it's just a placeholder object
    that stores the form field -> database column mapping.


    You should never have to call any of the methods on this object.

    Example usage:
      (Assuming the SQLAlchemy model is "Account")

    class UserAccountForm(DBMappedForm):
      first_name = TextField("First Name", [Mapped(Account.first_name)])


    For style convenience, we also define mapped = Mapped in this module,
    so your field definitions can look a little cleaner:

      first_name = TextField("First Name", [mapped(Account.first_name)])

    """

    field_flags = ("db_mapped",)

    def __init__(self, mapped_field):
        self.mapped_field = mapped_field

    def __call__(self, form, field):
        pass

    @property
    def model_class(self):
        return self.mapped_field.class_

    @property
    def model_attribute_name(self):
        return self.mapped_field.key

    def has_mapping_for(self, db_object):
        return isinstance(db_object, self.model_class)

    def db_object_value(self, db_object):
        if not self.has_mapping_for(db_object):
            raise ValueError("No mapping for model: %s" % self.model_class)
        return getattr(db_object, self.model_attribute_name)

    def set_db_object_value(self, db_object, value):
        if not self.has_mapping_for(db_object):
            raise ValueError("No mapping for model: %s" % self.model_class)
        setattr(db_object, self.model_attribute_name, value)


mapped = Mapped
