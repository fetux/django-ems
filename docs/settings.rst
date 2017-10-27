Settings
========

All django-ems settings are optional. Default values are given in
``ems.defaults`` and can be overriden in your project's settings.

.. _EMS_DEFAULT_LOCATION_SLUG:

EMS_DEFAULT_LOCATION_SLUG
-------------------------------

:Default: ``None``

This setting allows you to set an initial Location to associate with an entry
in the Clock In form. The user can override the default choice by selecting
another Location when clocking in.

If ``EMS_DEFAULT_LOCATION_SLUG`` is not given, then then no initial
value is used.

.. _EMS_PAID_LEAVE_PROJECTS:

EMS_PAID_LEAVE_PROJECTS
-----------------------------

:Default: ``{}``

This setting allows you to specify projects which people can clock in to that
are not business-related. These projects will not be included in the total
number of 'worked' hours.  For example::

    EMS_PAID_LEAVE_PROJECTS = {
        'sick': 1,
        'vacation': 2,
    }

where each key is an arbitrary slug for the project and each value is the
primary key of the associated project.

EMS_ACCCOUNTING_EMAILS
----------------------------

:Default: ``[]``

When pending contract hours are created or changed, an email can be sent
to notify someone. This setting is a list of the email addresses where those
emails should be sent.

EMS_EMAILS_USE_HTTPS
--------------------------

:Default: ``True``

Whether links in emails that ems sends should use https://.  The
default is True, but if set to False, links will use http://.
