import os
from termcolor import colored
from tick_template.ttest import ttest
from tick_template.fft import fft

OUTPUT_PATH = './tickFiles/'
LOG_PATH = '/tmp/kapacitor_udf/'


class Task:
    def __init__(self, argv, type):
        self.info = argv
        self.type = type
        self.status = False

        self.tick_name = f"{self.info['taskName']}_{self.info['id']}"
        self.tick_path = f"{OUTPUT_PATH}{self.tick_name}.tick"
        self.log_path = f"{LOG_PATH}{self.tick_name}_failure.log"

    def __del__(self):
        myCmd = f"kapacitor delete tasks {self.tick_name}"
        os.system(myCmd)
        print(f"{self.tick_name} is removed.")

    def __str__(self):
        color = "green" if self.status else "red"
        return "{:<15} {:<15} {:<15} {:<15} {:<15} {:<25} {:<15}".format(
            self.info['taskName'], self.type, self.info['database'], self.info['measurement'],
            self.info['field'], self.info['id'], colored(str(self.status), color)
        )

    def getTick(self):
        urlrt = "autogen"
        dbrt = {
            "db": self.tick_name,
            "rt": urlrt
        }
        content = ""
        if not os.path.exists(OUTPUT_PATH):
            try:
                os.mkdir(OUTPUT_PATH)
            except OSError as e:
                print("Failed to create the directory: {}".format(e))

        if not os.path.exists(self.tick_path):
            tick = open(self.tick_path, 'w')

            if self.type == 'ttest':
                content = ttest(self.tick_name, self.info, self.log_path)
            elif self.type == 'fft':
                content = fft(self.tick_name, self.info, self.log_path)

            tick.write(content)
            tick.close()

        # print( f"{self.tick_path} file has been created ")
        return dbrt

    def defineTask(self):
        myCmd = f"kapacitor define {self.tick_name} -tick {self.tick_path}"
        os.system(myCmd)

    def enableTask(self):
        myCmd = f"kapacitor enable {self.tick_name}"
        os.system(myCmd)
        self.status = True

    def disableTask(self):
        myCmd = f"kapacitor disable {self.tick_name}"
        os.system(myCmd)
        self.status = False

    def deleteTask(self):
        del self
