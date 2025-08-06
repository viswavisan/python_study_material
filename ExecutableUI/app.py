'''
PyQt is a set of Python bindings for Qt, which is a popular C++ framework used to build cross-platform GUI 
(Graphical User Interface) applications. In simpler terms, 
PyQt lets you write desktop applications in Python, using the powerful Qt UI toolkit.
'''

'''
PyInstaller is a popular Python tool that converts Python scripts into standalone executable files
 for Windows, macOS, and Linux.

pyinstaller --onefile --noconsole --icon=app.ico your_script.py
'''

import PyInstaller.__main__

# PyInstaller.__main__.run([
#     'your_script.py',
#     '--onefile',
#     '--noconsole',           # Optional: hide terminal for GUI apps
#     '--icon=app.ico',        # Optional: add icon
#     '--name=MyAppName'       # Optional: name of the .exe
# ])

'''
QWidget is the base class for all user interface objects in PyQt (and Qt). When you create an instance of QWidget(), 
you're creating a basic, empty window or UI component that can:
Act as a window itself, or
Be used as a container/parent for other widgets (buttons, labels, etc.)
'''

'''
In PyQt, a layout is a system that automatically arranges widgets (buttons, labels, etc.) inside a container like a QWidget.
Instead of setting positions and sizes manually (using move() or resize()), layouts let you manage the UI structure more cleanly 
and responsively, especially when the window is resized.
'''
import os,sys
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dir)


from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel,QDockWidget,QWidget,QVBoxLayout,QTabWidget
from PyQt6.QtGui import QAction,QIcon
from PyQt6.QtCore import Qt

#window
app = QApplication(sys.argv) 
window = QMainWindow()
window.setWindowTitle("PyQt6 App")
window.setGeometry(100, 100, 600, 400)

#menubar
def setup_menu():
    menu = window.menuBar()
    file_menu = menu.addMenu("File")
    exit_action = QAction("Exit", window)
    # exit_action.triggered.connect(self.close)
    file_menu.addAction(exit_action)
setup_menu()

#toolbar:
def toolbar():
    fileToolBar = window.addToolBar("view")
    fileToolBar.addAction(QAction(QIcon("png/prop.png"),"prop",window))
    fileToolBar.addAction(QAction(QIcon("png/open.png"),"open",window))
    fileToolBar.addAction(QAction(QIcon("png/mesh.png"),"edge",window))
    fileToolBar.addAction(QAction(QIcon("png/color.png"),"color",window))
toolbar()

#dock window/ movable window
dock = QDockWidget("Dock window", window)
dock.setWidget(QLabel("Dock Content"))
window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |QDockWidget.DockWidgetFeature.DockWidgetClosable)
dock.setStyleSheet("""
    QWidget {
        border: 2px solid black;
        border-radius: 4px;
        background-color: #fdfdfd;
    }
""")
#statusbar
sb=window.statusBar()
sb.setStyleSheet('background-color : lightgray')

#main frame
centralwidget = QWidget(window)
window.setCentralWidget(centralwidget)

#tab widget
layout = QVBoxLayout(centralwidget)
tabs= QTabWidget();layout.addWidget(tabs)

tab1 = QWidget()
tab1_layout = QVBoxLayout(tab1)
tab1_layout.addWidget(QLabel("Content of Tab 1"))


#3D Window
import vtkmodules.all as vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

def add_vtk():
    tab2 = QWidget()
    tab2_layout = QVBoxLayout(tab2)
    vtk_widget = QVTKRenderWindowInteractor(tab2)
    tab2_layout.addWidget(vtk_widget)
    renderer = vtk.vtkRenderer()
    vtk_widget.GetRenderWindow().AddRenderer(renderer)
    interactor = vtk_widget.GetRenderWindow().GetInteractor()
    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetRadius(1.0)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphere_source.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    renderer.AddActor(actor)
    renderer.ResetCamera()
    vtk_widget.Initialize()
    vtk_widget.Start()
    return tab2
tabs.addTab(tab1, "Tab 1")
tabs.addTab(add_vtk(), "Tab 2")

window.show()
sys.exit(app.exec())
