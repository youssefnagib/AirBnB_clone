#!/usr/bin/python3
"""console.py that contains the entry point of the command interpreter"""
from models.base_model import BaseModel
import cmd
import shlex
import models
import re
from shlex import split
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import sys
"""console.py  that contains the entry point of the command interprete"""


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """The command line """
    prompt = "(hbnb) "
    __class_names = {
        "Amenity": Amenity, "BaseModel": BaseModel, "City": City,
        "Place": Place, "Review": Review, "State": State, "User": User
    }
    # __class_names = {"Amenity": Amenity, "BaseModel": BaseModel,
    # "City": City, "Place": Place, "Review": Review,
    # "State": State, "User": User}

    def precmd(self, line):
        """ Edit given command to allow second type of input"""
        if not sys.stdin.isatty():
            print()
        if '.' in line:
            line = line.replace('.', ' ').replace('(', ' ').replace(')', ' ')
            cmd_argv = line.split()
            cmd_argv[0], cmd_argv[1] = cmd_argv[1], cmd_argv[0]
            line = " ".join(cmd_argv)
        return cmd.Cmd.precmd(self, line)
    
    def do_quit(self, arg):
        """ Quit command is to exit the program """
        return True

    def do_EOF(self, arg):
        """ EOF command to exit the program """
        print()
        exit()

    def emptyline(self):
        """if empty line + ENTER should not execute anything"""
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        """
        arg = shlex.split(arg)
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in self.__class_names:
            print("** class doesn't exist **")
        else:
            creates__new_instance = self.__class_names[arg[0]]()
            models.storage.save()
            print(creates__new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and id
        """
        arg = shlex.split(arg)
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in self.__class_names:
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        else:
            show_class = models.storage.all()
            key = arg[0] + '.' + arg[1]
            if key in show_class:
                print(show_class[key])
            else:
                print("** no instance found **")
    
    def do_destroy(self, arg):
        """
        Deletes an instance based on
        the class name and id
        """
        arg = shlex.split(arg)
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in self.__class_names:
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        else:
            store_all = models.storage.all()
            for key, value in store_all.items():
                name = value.__class__.__name__
                id = value.id
                if name == arg[0] and id == arg[1].strip('"'):
                    del value
                    del models.storage._FileStorage__objects[key]
                    models.storage.save()
                    return
            print("** no instance found **")

    def do_all(self, arg):
        """
           Prints all string representation
           of all instances based or not on the class name
        """
        arg = shlex.split(arg)
        all = models.storage.all()
        new_list = []
        if len(arg) == 0:
            for value in all.values():
                new_list.append(str(value))
            print(new_list)
        elif arg[0] not in self.__class_names:
            print("** class doesn't exist **")
        else:
            for value in all.values():
                if value.__class__.__name__ == arg[0]:
                    new_list.append(str(value))
            print(new_list)

    def do_update(self, arg):
        """
        Updates an instance based on the class name
        and id by adding or updating attribute
        """
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__class_names:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_count(self, args):
        """Count current number of class instances"""
        if not args:
            print("** class name is missing **")
        elif args.split()[0] not in HBNBCommand.__class_names:
            print("** class doesn't exist **")
        else:
            count = 0
            for k in models.storage.all():
                if args == k.split('.')[0]:
                    count += 1
            print(count)

if __name__ == '__main__':
    HBNBCommand().cmdloop()
