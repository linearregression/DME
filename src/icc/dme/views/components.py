
from gi.repository import Gtk
from icc.xray.views.drawing import *
from icc.rake.views.base import ConfirmationDialog, InputDialog
import icc.rake.views.components
import icc.rake.interfaces

from interfaces import *
import zope.component

from matplotlib.figure import Figure
import matplotlib
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

import pyxser

def gsm():
    return zope.component.getGlobalSiteManager()

class DMENavigatorToolbar(NavigationToolbar):
    pass


class View(icc.rake.views.components.View):
    """
    """
    resource=__name__

    def __init__(self, model=None, parent=None):
        icc.rake.views.components.View.__init__(
            self, model=model, parent=parent)

class DMEPlotView(View):
    """
    """

    def __init__(self, model=None, parent=None):
        """
        """
        View.__init__(self, model=model, parent=parent)
        self.parent_ui=pui=gsm().getUtility(
            icc.rake.views.interfaces.IApplication
        )

        self.ui.main_frame=frame=Gtk.Frame()
        vbox=Gtk.VBox()
        frame.add(vbox)

        fig = Figure(figsize=(5,4), dpi=120,
            subplotpars=matplotlib.figure.SubplotParams(
                left=0.03,
                right=0.96,
                bottom=0.03,
                top=0.96)
        )

        canvas=FigureCanvas(fig)
        canvas.set_size_request(600,400)
        vbox.pack_start(canvas, True, True, 0)
        toolbar=DMENavigatorToolbar(canvas, self)

        parent.connect("project-open", self.on_project_open)
        parent.connect("project-save", self.on_project_save)
        self.invalidate_model(model)

    def on_project_open(self, widget, filename):
        if 1:
        #try:
            i=open(filename, "r")
        #except IO:
        s=i.read()
        model=pyxser.unserialize(s, enc='utf-8', cinit=True)
        self.set_model(model)
        i.close()
        return True

    def on_project_save(self, widget, filename):
        assert (self.model != None), "the model should be not None"
        o=open(filename, "w")
        w=pyxser.serialize(self.model, enc='utf-8', depth=3)
        o.write(w)
        o.close()
        return True
