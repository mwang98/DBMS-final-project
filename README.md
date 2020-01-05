# DBMS Final Project


### Ref
[Anomaly Detection with InfluxDB Tutorial](https://docs.influxdata.com/kapacitor/v1.5/guides/anomaly_detection/?fbclid=IwAR1DzSGOcmdgxzEyNkh8J47iYWUNN3URjMkYLvP_e0A-4t2iCon-kfrhZ_4)
This tutorial is poorly organized, we provide more thorough instructions here.


### Install Dependencies

* python3
* InfluxDB==1.7.9
* Kapacitor==1.5.3
https://portal.influxdata.com/downloads/


### Start Services

#### Mac
```shell script
brew services start influxdb
brew services start kapacitor
brew services start telegraf
```

#### Ubuntu
```shell script
sudo systemctl start influxdb
sudo systemctl start kapacitor
sudo systemctl start telegraf
```

### Verify Services Status

Execute the command and check for errors.
#### Mac
    TODO
#### Ubuntu
```shell script
sudo journalctl -f -n 128 -u influxdb
```
or 
```shell script
sudo systemctl status <influxdb/kapacitor/telegraf>
```
##

### Instructions

You can run `bash run.sh` directly, detailed descriptions are below.

1. Change Kapacitor configs
    Append the code in `kapacitor-part.conf` to your kapacitor configuration file.
    It's typically located at `/etc/kapacitor/kapacitor.conf`
    Note that you should remove the previously defined `[udf]` function if there is any in your conf file.

2. Restart Kapacitor
    ```shell script
    sudo service kapacitor restart
    ```

    Check logs for errors
    ```shell script
    sudo tail -f -n 128 /var/log/kapacitor/kapacitor.log
    sudo tail -f -n 128 /usr/local/var/log/kapacitor.log
    ```

3. Define Kapacitor Task
    ```shell script
    kapacitor define print_temps -tick print_temps.tick
    ```
    If success, there should be nothing printed to your console. 

4. Start the recording in the background
    ```shell script
    rid=$(kapacitor record stream -task print_temps -duration 24h -no-wait)
    ```

5. Run python script to generate data
    ```shell script
    python printer_data.py
    ```

6. We can verify it worked by listing information about the recording. 
    Our recording came out to 1.6MB, so yours should come out somewhere close to that:
    ```
    $ kapacitor list recordings $rid
    ID                                      Type    Status    Size      Date
    7bd3ced5-5e95-4a67-a0e1-f00860b1af47    stream  finished  1.6 MB    04 May 16 11:44 MDT
    ```

7. Finally, let’s run the play against our task and see how it works:
    ```shell script
    kapacitor replay -task print_temps -recording $rid -rec-time
    ```

8. Check the various log files to see if the algorithm caught the anomalies:
    ```shell script
    cat /tmp/kapacitor_udf/{hotend,bed,air}_failure.log
    ```



### Instruction to connect all staff

1. Start `InfluxDB`, `Kapacitor`, `Chronograf`, `Telegraf`

```shell 
brew services restart influxdb
brew services restart kapacitor
brew services restart telegraf
brew services restart chronograf
```

2. `Chronograf` render on the port `http://localhost:8888`
3. 



