mkdir /tmp/kapacitor_udf/

sudo service kapacitor restart

sleep 5

kapacitor define print_temps -tick print_temps.tick

rid=$(kapacitor record stream -task print_temps -duration 24h -no-wait)
echo $rid

pipenv run python printer_data.py

kapacitor list recordings $rid

kapacitor replay -task print_temps -recording $rid -rec-time

cat /tmp/kapacitor_udf/{hotend,bed,air}_failure.log
