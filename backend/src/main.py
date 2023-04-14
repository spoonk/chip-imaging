import logging
logging.basicConfig(level = logging.DEBUG)


from stage.pmm_stage import PMMStage
s = PMMStage()


s.move_to(100.0, 100.0)
print(s.get_current_position())