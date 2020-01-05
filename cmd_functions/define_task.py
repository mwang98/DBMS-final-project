import os
from termcolor import colored
from tick_template.ttest import ttest
from tick_template.fft   import fft
  

OUTPUT_PATH = './tick_files/'
LOG_PATH = '/tmp/kapacitor_udf/'

class Task():
    def __init__( self, argv, type ):
        self.info        = argv
        self.type        = type
        self.status      = False

        self.tick_name   = f"{ self.info['taskName'] }_{ self.info['id'] }"
        self.tick_path   = f"{ OUTPUT_PATH }{ self.tick_name }.tick"
        self.log_path    = f"{ LOG_PATH    }{ self.tick_name }_failure.log"
    
    def __del__( self ):
        os.system( f"kapacitor delete tasks {self.tick_name}" )
        os.system( f"rm -f {self.tick_path} {self.log_path}" )
        print(f"{self.tick_name} is removed.")

    def __str__( self ):
        color = "green" if self.status else "red"
        return "{:<15} {:<15} {:<15} {:<15} {:<15} {:<25} {:<15}". \
                format(self.info['taskName'], self.type, self.info['database'], self.info['measurement'], self.info['field'], self.info['id'], colored(str(self.status), color))

    def getTick( self ):
        urlrt = "autogen"
        dbrt    = {
            "db": self.tick_name,
            "rp": urlrt
        }
        content = ""
        if not os.path.exists( OUTPUT_PATH ):
            try:
                os.mkdir( OUTPUT_PATH )
            except OSError as e:
                print("Failed to create the directory: {e}".format(e))

        tick = open( self.tick_path, 'w' )

        if self.type == 'ttest':
            content = ttest( self.tick_name, self.info, self.log_path )    
        elif self.type == 'fft':
            content = fft  ( self.tick_name, self.info, self.log_path )

        tick.write( content )
        tick.close()

        return dbrt

    def define( self ):
        try:
            os.system( f"kapacitor define {self.tick_name} -tick {self.tick_path}" )
        except OSError as e:
            print("Unable to define task in kapacitor: " ,e)
            del self
    
    def enable( self ):
        try:
            os.system( f"kapacitor enable {self.tick_name}" )
            self.status = True
        except OSError as e:
            print("Unable to execute task in kapacitor: " ,e)
            del self
    
    def disable( self ):
        os.system( f"kapacitor disable {self.tick_name}" )
        self.status = False

    def modify( self, argv ):
        os.system( f"kapacitor delete tasks {self.tick_name}" )
        os.system( f"rm -f {self.tick_path} {self.log_path}" )

        for key, value in argv.items():
            self.info[ key ] = value

        self.tick_name = f"{ self.info['taskName'] }_{ self.info['id'] }"
        self.tick_path = f"{ OUTPUT_PATH }{ self.tick_name }.tick"
        self.log_path  = f"{ LOG_PATH    }{ self.tick_name }_failure.log"

