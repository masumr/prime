from django.db import models

from models.models import Beat


class BeatPlay(models.Model):
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super(BeatPlay, self).save(*args, **kwargs)
        BeatPopularityIncrease.objects.create(beat=self.beat, increase_amount=BeatPopularityIncrease.AMOUNT_FOR_PLAY)


class BeatDemoDownload(models.Model):
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super(BeatDemoDownload, self).save(*args, **kwargs)
        BeatPopularityIncrease.objects.create(beat=self.beat,
                                              increase_amount=BeatPopularityIncrease.AMOUNT_FOR_DEMO_DOWNLOAD)


class BeatShare(models.Model):
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class BeatPopularityIncrease(models.Model):
    AMOUNT_FOR_PLAY = 1
    AMOUNT_FOR_DEMO_DOWNLOAD = 2
    AMOUNT_FOR_SALE = 5
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    increase_amount = models.PositiveSmallIntegerField()
