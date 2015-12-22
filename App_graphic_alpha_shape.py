__author__ ='Irfaan Domun'
import sys#, os, random
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
from PyQt4.QtGui import QMainWindow,QFileDialog,QMessageBox,QSlider,QWidget,QLineEdit,QCheckBox,QPushButton,QHBoxLayout,QVBoxLayout,QAction,QApplication,QLabel,QIcon
from PyQt4.QtCore import SIGNAL,Qt
import numpy as np

from scipy.spatial import Voronoi#, voronoi_plot_2d
# vor = Voronoi(self.points,furthest_site =True)
# vor1 = Voronoi(self.points,furthest_site =False)
# import matplotlib.pyplot as plt
import math 

# from collections import namedtuple
from math import sqrt
import itertools

# import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure


class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        
        np.random.seed(1234)
        self.nombre_de_point =15
        self.points = np.array( [[np.random.rand(),np.random.rand()]for i in range(self.nombre_de_point)])
        self.alpha=10
        
        
        
        self.setWindowTitle('self.alpha shape: PyQt with matplotlib')
        self.create_menu()
        self.create_main_frame()
        
        self.create_status_bar()
        self.textbox_alpha.setText(str(self.alpha))

#         self.textbox.setText('30 40 20')
#         str = unicode(self.textbox.text())
#         self.data = map(int, str.split())
        self.draw_alpha()

    def save_plot(self):
        file_choices = "PNG (*.png)|*.png"
        
        path = unicode(QFileDialog.getSaveFileName(self, 
                        'Save file', '', 
                        file_choices))
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)
    
    def on_about(self):
        msg = """ Alpha shape implementation:
        
         * Use the matplotlib navigation bar
         * Change the value of alpha and press Enter (or click "Draw")
         * Show or hide the grid
         * Drag the slider to modify the value of alpha
         * Save the plot to a file using the File menu
         * Click on the window to add a point
         * Press random to get a random set of point
         * Click on clear to get a an empty graph that can be filled with the mouse (can't draw the alpha extrems with less than 4 point)
         
        """
        QMessageBox.about(self, "About the demo", msg.strip())
    
    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        # 
#         box_self.points = event.artist.get_bbox().get_self.points()
        
#         msg = "You've clicked on a bar with coords:\n %s" % box_self.points
#         msg = "x :" + str(event.xdata) +"\ny : "+ str(event.ydata) +"\n"
#        #print self.data
#         self.data.append(event.xdata)
        #print self.points[:3],
        if self.points != []:
            self.points = np.append( self.points,[[event.xdata,event.ydata]],axis=0)
        else:
            self.points = [[event.xdata,event.ydata]]
        
        # clear the axes and redraw the plot anew
        #
#         self.axes.clear()        
#         self.axes.grid(self.grid_cb.isChecked())
#         for i in range(len(self.data)):
        self.draw_alpha()
#         self.axes.plot(event.xdata,event.ydata,marker='o')
#         self.axes.bar(
#             left=x, 
#             height=self.data, 
#             width=self.slider.value() / 100.0, 
#             align='center', 
#             self.alpha=0.44,
#             picker=5)
        
#         self.canvas.draw()
#         QMessageBox.information(self, "Click!", msg)
    def circles_from_p1p2r(self,p1, p2, r):
        if r == 0.0:
            raise ValueError('radius of zero')
    #     (x1, y1), (x2, y2) = p1, p2
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]
        if x1 == x2 and y1 == y2:
            raise ValueError('coincident points gives infinite number of Circles')
        # delta x, delta y between points
        dx, dy = x2 - x1, y2 - y1
        # dist between points
    #     q = sqrt(dx**2 + dy**2)
        q = self.dist(p1,p2)
        if q > 2.0*r:
#            print q,2.0*r,r
            raise ValueError('separation of points > diameter')
        # halfway point
        x3, y3 = (x1+x2)/2, (y1+y2)/2
        # distance along the mirror line
        d = sqrt(r**2-(q/2)**2)
        # One answer
        cx1 = x3 - d*dy/q,
        cy1 = y3 + d*dx/q,
#         # The other answer
        cx2 = x3 + d*dy/q,
        cy2 = y3 - d*dx/q,
        return [cx1,cy1],[cx2,cy2]
    
    def dist(self,p,p1):
        return math.sqrt( (p[0]-p1[0])*(p[0]-p1[0]) + (p[1]-p1[1])*(p[1]-p1[1]))

    def draw_alpha(self):
        a = []
        list_extrem = []
        
        if len(self.points) > 3:
            
            self.axes.clear()        
            self.axes.grid(self.grid_cb.isChecked())
            if self.alpha < 0 :
#                print self.points
                vor1 = Voronoi(self.points,furthest_site =False)
            
                for nb_point in range(len(self.points)):
                    numero_region_point = vor1.point_region[nb_point]
                    list_max = []
                    if -1 not in vor1.regions[numero_region_point]:
                
                        for numero_vertices_region in vor1.regions[numero_region_point]:
                                distance_vertice_min_temp = self.dist(vor1.points[nb_point], vor1.vertices[numero_vertices_region])
                                list_max.append(distance_vertice_min_temp)

                        if  self.alpha <= - 1.0/max(list_max):
                            list_extrem.append(list(self.points[nb_point]))
                    else :
                        if self.alpha <= 0:
                            list_extrem.append(list(self.points[nb_point]))
                        else:
                            print " not possible, but algo says stuff"
                            
            
            else : 
                vor1 = Voronoi(self.points,furthest_site =True)
            
                for nb_point in range(len(self.points)):
                    numero_region_point = vor1.point_region[nb_point]
                    list_dist_min = []
                    if vor1.regions[numero_region_point] != []:
                        if vor1.regions[numero_region_point][0]==-1 and len(vor1.regions[numero_region_point]) ==1:
                            if self.alpha ==0 :
                                list_extrem.append(list(self.points[nb_point])) 
                                #print "not supposed to happenned but never too careful..."
                        else :    
                            for numero_vertices_region in vor1.regions[numero_region_point]:                    
                                if numero_vertices_region !=-1:
                                    distance_vertice_min_temp = self.dist(vor1.points[nb_point], vor1.vertices[numero_vertices_region])
                                    list_dist_min.append(distance_vertice_min_temp)
                            if self.alpha <= 1.0/min(list_dist_min):
                                list_extrem.append(list(self.points[nb_point]))
                                    
            
            for a, b in itertools.combinations(list_extrem, 2):
                try :
                    c1,c2 = self.circles_from_p1p2r(a, b,1.0/abs(self.alpha))    
                    list_extrem_temp = list_extrem[:]
                    list_extrem_temp.remove(a)
                    list_extrem_temp.remove(b)
                    list_distance_centre1 = []
                    list_distance_centre2 = []
#                     for extrem in list_extrem_temp:
#                         list_distance_centre1.append(self.dist(c1, extrem))
#                         list_distance_centre2.append(self.dist(c2, extrem))
#                     if self.alpha < 0:
#                         if min(list_distance_centre1) >= -1.0/self.alpha or min(list_distance_centre2) >=- 1.0/self.alpha:
#                             self.axes.plot([a[0],b[0]],[a[1],b[1]],marker='o')
#                     else : 
#                         if max(list_distance_centre1) <= 1.0/self.alpha or max(list_distance_centre2) <= 1.0/self.alpha:
#                             self.axes.plot([a[0],b[0]],[a[1],b[1]],marker='o')     
                    alpha_extrem = True 
                    for extrem in list_extrem_temp:
                        list_distance_centre1.append(self.dist(c1, extrem))
                        list_distance_centre2.append(self.dist(c2, extrem))
                        if self.alpha < 0:
                            if self.dist(c1,extrem) >= -1.0/self.alpha :
                                pass
                            else :
                                alpha_extrem = False
                                break                                                            
                        else : 
                            if self.dist(c1,extrem) <= 1.0/self.alpha :
                                pass
                            else :
                                alpha_extrem = False
                                break                                   
                    if alpha_extrem :
                        self.axes.plot([a[0],b[0]],[a[1],b[1]],marker='o') 
                    else : 
                        alpha_extrem = True
                        for extrem in list_extrem_temp:
                            if self.alpha < 0:
                                if self.dist(c2,extrem) >= -1.0/self.alpha :
                                    pass
                                else :
                                    alpha_extrem = False
                                    break                                                            
                            else : 
                                if self.dist(c2,extrem) <= 1.0/self.alpha :
                                    pass
                                else :
                                    alpha_extrem = False
                                    break                                   
                        if alpha_extrem :
                            self.axes.plot([a[0],b[0]],[a[1],b[1]],marker='o') 
                    
                        
                        
                except :
                    pass
    
            list_extrem.sort()
            a = list(list_extrem for list_extrem,_ in itertools.groupby(list_extrem))
        else : 
            self.axes.clear()
    
            
        for i in self.points:
            self.axes.plot(i[0],i[1],color='blue',marker='o')
        for i in a: 
        #    #print "list_extrem",i 
            self.axes.plot(i[0],i[1],color='red',marker = 'o')
                    

        self.canvas.draw()
        
    def on_draw(self):
        """ Redraws the figure
        """
#         str = unicode(self.textbox.text())
#         self.data = map(int, str.split())
        
#         x = range(len(self.data))

        # clear the axes and redraw the plot anew
        #
        self.axes.clear()        
        self.axes.grid(self.grid_cb.isChecked())
#         self.axes.plot(self.data)
        for i in range(len(self.data)):
            self.axes.plot(self.data[i],i,marker='o')
#         self.axes.bar(
#             left=x, 
#             height=self.data, 
#             width=self.slider.value() / 100.0, 
#             align='center', 
#             self.alpha=0.44,
#             picker=5)
        
        self.canvas.draw()
    def set_alpha(self):
        self.alpha = float(unicode( self.textbox_alpha.text()))
        self.slider.setRange(-abs( self.alpha),abs(self.alpha))
        self.slider.setValue(self.alpha)
        self.slider.setTickPosition(QSlider.TicksBothSides)

        self.draw_alpha()
        
    def set_Slider(self):
        self.alpha = self.slider.value()
        self.textbox_alpha.setText(str(self.alpha))
        self.draw_alpha()
        
    def random_point(self):
#         self.data = np.random.randint(low=0,high=5,size = (4,2))
        np.random.seed()
        self.points = np.array( [[np.random.rand(),np.random.rand()]for i in range(self.nombre_de_point)])
        self.draw_alpha()
    def set_nombre_point(self):
        self.nombre_de_point = int(unicode(self.textbox_nombre_point.text()))
        self.points = np.array( [[np.random.rand(),np.random.rand()]for i in range(self.nombre_de_point)])

        self.draw_alpha()
    def draw_clear(self):
        self.axes.clear()
        self.canvas.draw()
        self.axes.plot()
        self.points = []
        
    def create_main_frame(self):
        self.main_frame = QWidget()
        
        # Create the mpl Figure and FigCanvas objects. 
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        
        # Since we have only one plot, we can use add_axes 
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)
        
        # Bind the 'pick' event for clicking on one of the bars
        
#         self.canvas.mpl_connect('pick_event', self.on_pick)#         
        self.canvas.mpl_connect('button_press_event', self.on_pick)
        
        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        
        # Other GUI controls
        # 
        
#         self.textbox = QLineEdit()
#         self.textbox.setMinimumWidth(200)
#         self.connect(self.textbox, SIGNAL('editingFinished ()'), self.on_draw)
        
        self.textbox_alpha = QLineEdit()
        self.textbox_alpha.setMinimumWidth(5)
#         self.alpha = unicode(self.textbox_alpha.text())
        self.connect(self.textbox_alpha, SIGNAL("editingFinished ()"),self.set_alpha)
        
        self.draw_button = QPushButton("&Draw")
        self.connect(self.draw_button, SIGNAL('clicked()'), self.set_alpha)

        self.clear_button = QPushButton("&Clear")
        self.connect(self.clear_button, SIGNAL('clicked()'), self.draw_clear)
                
        self.random_button = QPushButton("&Random")
        self.connect(self.random_button, SIGNAL('clicked()'), self.random_point)
        
        self.grid_cb = QCheckBox("Show &Grid")
        self.grid_cb.setChecked(False)
        self.connect(self.grid_cb, SIGNAL('stateChanged(int)'), self.draw_alpha)
        
        self.textbox_nombre_point = QLineEdit('nombre de point :')
        self.textbox_nombre_point.setMinimumWidth(5)
        self.textbox_nombre_point.setText(str(self.nombre_de_point))
#         self.alpha = unicode(self.textbox_alpha.text())
        self.connect(self.textbox_nombre_point, SIGNAL("editingFinished ()"),self.set_nombre_point)
        
#         slider_label = QLabel('Bar width (%):')
#         self.slider = QSlider(Qt.Horizontal)
#         self.slider.setRange(1, 100)
#         self.slider.setValue(20)
#         self.slider.setTracking(True)
#         self.slider.setTickPosition(QSlider.TicksBothSides)
#         self.connect(self.slider, SIGNAL('valueChanged(int)'), self.draw_alpha)
        slider_label = QLabel('Range -alpha alpha (%):')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(-abs( self.alpha),abs(self.alpha))
        self.slider.setValue(self.alpha)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.connect(self.slider, SIGNAL('valueChanged(int)'), self.set_Slider)
        
        #
        # Layout with box sizers
        # 
        hbox = QHBoxLayout()
        
        for w in [  self.textbox_alpha, self.draw_button,self.clear_button, self.grid_cb,
                    slider_label, self.slider, self.random_button,self.textbox_nombre_point]:
            hbox.addWidget(w)
            hbox.setAlignment(w, Qt.AlignVCenter)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        vbox.addLayout(hbox)
        
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
    
    
    def create_status_bar(self):
        self.status_text = QLabel("Alpha Shape by Irfaan Domun")
        self.statusBar().addWidget(self.status_text, 1)
        
    def create_menu(self):        
        self.file_menu = self.menuBar().addMenu("&File")
        
        load_file_action = self.create_action("&Save plot",
            shortcut="Ctrl+S", slot=self.save_plot, 
            tip="Save the plot")
        quit_action = self.create_action("&Quit", slot=self.close, 
            shortcut="Ctrl+Q", tip="Close the application")
        
        self.add_actions(self.file_menu, 
            (load_file_action, None, quit_action))
        
        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About", 
            shortcut='F1', slot=self.on_about, 
            tip='About the demo')
        
        self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
