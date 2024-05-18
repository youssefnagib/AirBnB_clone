from models.base_model import BaseModel
import cmd
import shlex
import models
"""console.py  that contains the entry point of the command interprete"""


class HBNBCommand(cmd.Cmd):
    """The command line """
    prmt = "(hbnb) "
    __class_names = [
        "Amenity",
        "BaseModel",
        "City",
        "Place",
        "Review",
        "State",
        "User"
    ]

    def do_quit(self, arg):
        """Quit /EOF command to exit the program"""
        return True

    do_EOF = do_quit

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
            creates__new_instance = self.__classes[arg[0]]()
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
            show_class = models.storage.all
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
        opject = models.storage.all()
        arg = arg.split(" ")

        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in self.__class_names:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif len(arg) == 2:
            print("** attribute name missing **")
        elif len(arg) == 3:
            print("** value missing **")
        else:
            pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
