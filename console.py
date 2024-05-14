from models.base_model import BaseModel
import cmd
import json
import re
import models

class HBNBCommand(cmd.Cmd):
    prmt = "(hbnb) "

    def s_quit(self, arg):
        return True
    
    def s_EOF(self, arg):
        print()
        return True
    




if __name__ == '__main__':
    HBNBCommand().cmdloop()