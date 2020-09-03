from _io import open
import os
import shutil
from genericpath import isdir
from os.path import isfile


class FileHandler(object):
    '''
    Omogucuje rad sa fajlovima
    '''

    def __init__(self, ):
        """
        Konstruktor
        """
        super(FileHandler, self).__init__()

    def createFile(self, path, name):
        """

        Metoda kreira fajl sa zadatim imenom u zadatom direktorijumu

        Args:
            path: putanje do direktorijuma u kom se kreira fajl
            name: ime fajla koji ce biti kreiran
        """
        open(os.path.join(path, name), mode='w').close()

    def createDirectory(self, path, name):
        """

        Metoda kreira direktorijum sa zadatim imenom u zadatom direktorijumu

        Args:
            path: putanje do direktorijuma u kom se kreira direktorijum
            name: ime direktorijuma koji ce biti kreiran
        """
        os.mkdir(os.path.join(path, name))

    def removeFile(self, path, name):
        """

        Metoda brise fajl sa zadatim imenom u zadatom direktorijumu

        Args:
            path: putanje do direktorijuma u kom se brise fajl
            name: ime fajla koji ce biti obrisan
        """
        os.remove(os.path.join(path, name))

    def removeDirectory(self, path, name):
        """

        Metoda brise direktorjium sa zadatim imenom u zadatom direktorijumu

        Args:
            path: putanje do direktorijuma u kom se brise direktorijum
            name: ime direktorijuma koji ce biti obrisan
        """
        shutil.rmtree(os.path.join(path, name))

    def rename(self, path, oldName, newName):
        """

        Metoda menja ime fajla sa zadatim imenom u zadatom direktorijumu

        Args:
            path: putanje do direktorijuma u kom se menja ime zadatog fajla
            oldName: ime fajla cije ce ime biti promenjeno
            newName: novo ime fajla
        """
        os.rename(os.path.join(path, oldName), os.path.join(path, newName))

    def getChildList(self, path):
        """
        Metoda vraca listu svih fajla koji se nalaze u direktorijumu

        Args:
            path: putanja do direktorijuma
        """
        return os.listdir(path)

    def getType(self, path):
        """
        Metoda vraca tip fajla koji se nalazi na zadatoj putanji

        Args:
              path putanja do fajla
        """
        if isdir(path):
            return "FOLDER "
        if isfile(path):
            return "FILE "
        else:
            return "INVALID"
