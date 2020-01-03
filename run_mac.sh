mkdir -m777 /tmp/kapacitor_udf/

sudo brew services start kapacitor 

sleep 5

sudo kapacitor define print_temps -tick print_temps.tick

echo "printing "
python3 printer_data.py &

# sudo tail -f -n 128 /var/log/kapacitor/kapacitor.log
sudo tail -f -n 128 /tmp/kapacitor_udf/{hotend,bed,air}_failure.log
