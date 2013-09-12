from zope.interface import implements
from interfaces import *

from icc.dme.fd import *
from icc.rake.views import get_user_config_option, set_user_config_option

class Project(object):

    implements(IProject)

    def __init__(self):
        self.setup_test_model()

    def setup_test_model(self):
        excel_file=get_user_config_option("source", type='string', keys='data_source')
        start_year=get_user_config_option("start_year", type='int', default=1973, keys='data_source')
        if excel_file == None:
            raise ValueError, "Forest data source is not supplied"
        self.fm = ForestModel(excel_file, start_year,
#		options={"NO_LOGGING":None, "NO_FIRES":None, "NO_INTERCHANGE":None}
#		options={"NO_INTERCHANGE":None}
#		options={"NO_INTERCHANGE":None,"NO_LOGGING":None, "NO_FIRES":None, "NO_GET":None}
		options={"NO_INTERCHANGE":None,"NO_FIRES":None, "NO_GET":None}
        )
        self.do_something()

    def do_something(self):
        F=self.fm
        self.modeller = Modeller = ForestModeller(F,
            endtime=50., starttime=0., interval=5., subdivisions=100)
        control=Modeller.model_head.total
        Modeller.Model()
        print "Modelling done."

        # Quantum (end)

        plot=ModelParameter(
            {
                "Sfree":Modeller.trajectories.S.O,
                "Snel":Modeller.trajectories.S.Nel
            }
        )

        def All(kind):
            return kind.I+kind.II+kind.Sr+kind.Pr+kind.Sp+kind.Per

        plot_max=ModelParameter(
            {
                "Sos":All(Modeller.trajectories.f101.S),
                "El":All(Modeller.trajectories.f102.S),
                "Pikhta":All(Modeller.trajectories.f103.S),
                "Listvennica":All(Modeller.trajectories.f104.S),
                "Kedr":All(Modeller.trajectories.f105.S),
                "Bereza":All(Modeller.trajectories.f124.S),
                "Osina":All(Modeller.trajectories.f125.S),
                "Free":(Modeller.trajectories.S)
            }
        )

        log_y_init="set logscale y"
