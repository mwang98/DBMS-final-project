mkdir -m777 /tmp/kapacitor_udf/

sudo service kapacitor restart

sudo sleep 5

sudo kapacitor define print_temps -tick print_temps.tick

echo "printing"
pipenv run python printer_data.py &

sudo chmod 777 /tmp/kapacitor_udf/*
cat /tmp/kapacitor_udf/{hotend,bed,air}_failure.log
