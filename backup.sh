#!/bin/sh
  
pg_dump -h localhost -U neverwork -Ft -f /backup/checkcheck/db/gc_`date +%Y%m%d-%T`.backup notecloud

today=$(date +"%Y-%m-%d")

/home/genonfire/.pyenv/versions/checkcheck/bin/python /home/genonfire/git/notecloud/manage.py dumpdata accounts.User --indent 4 -o /home/genonfire/git/notecloud/patch/user.json
/home/genonfire/.pyenv/versions/checkcheck/bin/python /home/genonfire/git/notecloud/manage.py dumpdata accounts.LoginDevice notes forums --indent 4 -o /home/genonfire/git/notecloud/patch/data.json
tar cvzf /backup/checkcheck/fixtures/$today.tar.gz /home/genonfire/git/notecloud/patch/*.json

rm /home/genonfire/git/notecloud/patch/*.json

