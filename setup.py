from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\Adarsh Basantwani\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Adarsh Basantwani\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'
buildOptions = dict(excludes = ["tkinter"], includes =["idna.idnadata","numpy.core._methods","numpy.lib.format"], optimize=1)
additional_mods = ['numpy.core._methods', 'numpy.lib.format']
setup(name = "technomate", version = "2.1", description = "An AI based Assistant", executables = [Executable('technomate_v2.py')], options =dict(build_exe = buildOptions))
