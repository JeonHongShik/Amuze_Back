<<<<<<< HEAD
'use strict';
{
    const $ = django.jQuery;
    const fields = $('#django-admin-prepopulated-fields-constants').data('prepopulatedFields');
    $.each(fields, function(index, field) {
        $(
            '.empty-form .form-row .field-' + field.name +
            ', .empty-form.form-row .field-' + field.name +
            ', .empty-form .form-row.field-' + field.name
        ).addClass('prepopulated_field');
        $(field.id).data('dependency_list', field.dependency_list).prepopulate(
            field.dependency_ids, field.maxLength, field.allowUnicode
        );
    });
}
=======
'use strict';
{
    const $ = django.jQuery;
    const fields = $('#django-admin-prepopulated-fields-constants').data('prepopulatedFields');
    $.each(fields, function(index, field) {
        $(
            '.empty-form .form-row .field-' + field.name +
            ', .empty-form.form-row .field-' + field.name +
            ', .empty-form .form-row.field-' + field.name
        ).addClass('prepopulated_field');
        $(field.id).data('dependency_list', field.dependency_list).prepopulate(
            field.dependency_ids, field.maxLength, field.allowUnicode
        );
    });
}
>>>>>>> 449f363306bc1ffaec77f6392861278cbb95f3fa
