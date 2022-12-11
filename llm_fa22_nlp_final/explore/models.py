import jsonfield
from django.db import models


class Corpus(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(name='source', max_length=200)
    safe = models.BooleanField(name='safe',default=False)
    new = models.BooleanField(name='new',default=True)
    import_date = models.DateTimeField(name='import_date')
    imported_by = models.CharField(name='imported_by',max_length=200,default="System")
    corpus = models.TextField(name='corpus',null=False,default="N/A")
    corpus_norm = models.TextField(name='corpus_norm',null=False,default="N/A")
    medspecialty = models.CharField(name='medspecialty',max_length=200, null=True)
    title = models.CharField(name="title", max_length=200,null=True,default="N/A")
    metadata = models.TextField(name="metadata", null=True) #keywords etc

    def __str__(self):
        return self.title

    def get_corpus(self):
        return self.corpus

    def fields(self):
        return self._meta.get_fields()


class Medication(models.Model):
    id = models.AutoField(primary_key=True)
    brand_name = models.TextField(name='brand_name', null=False,default="N/A")
    compound_name = models.TextField(name='compound_name', null=False,default="N/A")
    generic_name = models.TextField(name='generic_name', null=False,default="N/A")
    type = models.TextField(name='type', null=True)
    source = models.TextField(name='source',null=True)
    #is_combo = models.BooleanField(name='combination')
    isotc = models.BooleanField(name="otc",default=False)
    description = models.TextField(name="description",null=False,default="N/A")
    labeler = models.TextField(name='labeler',null=False,default="N/A")
    ndc_id = models.TextField(name='ndc_id',null=True)
    pharm_class = models.TextField(name='pharm_class',null=False,default='Unknown')
    compound_norm=models.TextField(name='compound_norm',null=False,default="N/A")
    brand_norm=models.TextField(name='brand_norm', null=True)
    labeler_norm=models.TextField(name='labeler_norm', null=True)
    generic_norm=models.TextField(name='generic_norm', null=True)
    #dose_form = models.CharField(name="dosageform", max_length=200)
    #route = models.CharField(name="route", max_length=200)

    def __str__(self):
        return self.compound_norm

    def fields(self):
        return self._meta.get_fields()

class Symptom(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(name='name',null=True)
    name_norm = models.TextField(name='name_norm',null=True)
    description = models.TextField(name='description',null=True)
    url = models.URLField(name='url', null=True)
    wordlist = models.JSONField(name="wordlist", null=True)

    def __str__(self):
        return self.name


    def fields(self):
        return self._meta.get_fields()