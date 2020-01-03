Path of kapacitor
    /usr/local/opt/kapacitor
Configuration of kapacitor, telegraf, influxdb
    /usr/local/etc

!!!!!Change kapacitor.conf!!!!!
    python program : prog = "/usr/local/bin/python3"
    args = ["-u", <pathOfUDF.py>]
    pathOfKapacitor : PYTHONPATH = "/usr/local/opt/kapacitor/kapacitor/udf/agent/py"
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Command to define the Kapacitor task (cd to the directory of .tick file)
    kapacitor define print_temps -tick print_temps.tick
Start the recording in the background
    kapacitor record stream -task print_temps -duration 24h -no-wait
Store returned ID as rid
    rid=<returnedID>
Start to generate data
    python printer_data.py
Access output by ID
    kapacitor list recordings $rid
    kapacitor replay -task print_temps -recording $rid -rec-time
