mkdir -m777 /tmp/kapacitor_udf/

# sudo brew services restart kapacitor 

sleep 5

kapacitor define print_temps -tick print_temps.tick

# rid=$(kapacitor record stream -task print_temps -duration 24h -no-wait)
# echo $rid

# python3 printer_data.py

# kapacitor list recordings $rid

# kapacitor replay -task print_temps -recording $rid -rec-time

echo "printing "
python3 printer_data.py

# sudo tail -f -n 128 /var/log/kapacitor/kapacitor.log
# tail -f -n 128 /tmp/kapacitor_udf/{hotend,bed,air}_failure.log
