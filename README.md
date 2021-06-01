# django-redpanda
App to report your health status and possible symptoms.

# clear cache and repopulate for redpanda
20 04 * * * DJANGO_SETTINGS_MODULE=redpanda.settings.shell ; export DJANGO_SETTINGS_MODULE; (cd /data2/python_venv/3.8/redpanda/ && . bin/activate && bin/python /data2/python_venv/3.8/djimix/djimix/bin/clear_cache.py 2>&1 | mail -s "[Red Panda] clear cache" larry@carthage.edu) >> /dev/null 2>&1

# send notifications to folks
#30 06 * * * (cd /data2/python_venv/3.8/redpanda/ && . bin/activate && bin/python redpanda/bin/facstaff_list.py 2>&1 | mail -s "[RedPanda] faculty and staff reminder" larry@carthage.edu) >> /dev/null 2>&1
