from stage.prior_stage import PriorStage


p = PriorStage('hi')


from imager.pymmcore_singleton import PymmcoreSingleton


inst = PymmcoreSingleton()
del inst

inst2 = PymmcoreSingleton()

inst3 = PymmcoreSingleton()

inst4 = PymmcoreSingleton()

inst5 = PymmcoreSingleton()

