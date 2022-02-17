from django.db import models

class Realization(models.Model):
    #DEBT add parent either ProjectDetail or Budget
    realization_jan = models.BigIntegerField(default = 0, blank = True)
    realization_feb = models.BigIntegerField(default = 0, blank = True)
    realization_mar = models.BigIntegerField(default = 0, blank = True)
    realization_apr = models.BigIntegerField(default = 0, blank = True)
    realization_may = models.BigIntegerField(default = 0, blank = True)
    realization_jun = models.BigIntegerField(default = 0, blank = True)
    realization_jul = models.BigIntegerField(default = 0, blank = True)
    realization_aug = models.BigIntegerField(default = 0, blank = True)
    realization_sep = models.BigIntegerField(default = 0, blank = True)
    realization_oct = models.BigIntegerField(default = 0, blank = True)
    realization_nov = models.BigIntegerField(default = 0, blank = True)
    realization_dec = models.BigIntegerField(default = 0, blank = True)
    switching_in = models.BigIntegerField(default = 0, blank = True)
    switching_out = models.BigIntegerField(default = 0, blank = True)
    top_up = models.BigIntegerField(default = 0, blank = True)
    returns = models.BigIntegerField(default = 0, blank = True)
    allocate = models.BigIntegerField(default = 0, blank = True)