from django.db import models
from django.core.validators import FileExtensionValidator
# from .validators import validate_csv


class FileModel(models.Model):
    csv_file_name = models.CharField(max_length=50)
    csv_file = models.BinaryField()


GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
)


class MuseumAPICSV(models.Model):
    objectId = models.IntegerField(primary_key=True)
    isHighlight = models.BooleanField()
    accessionNumber = models.CharField(max_length=50)
    accessionYear = models.IntegerField()
    isPublicDomain = models.BooleanField()
    primaryImage = models.CharField(max_length=50, null=True, blank=True)
    primaryImageSmall = models.CharField(max_length=50, null=True, blank=True)
    additionalImages = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=50)
    objectName = models.CharField(max_length=50)
    title = models.CharField(max_length=50, null=True, blank=True)
    culture = models.CharField(max_length=50, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    dynasty = models.CharField(max_length=50, null=True, blank=True)
    reign = models.CharField(max_length=50, null=True, blank=True)
    portfolio = models.CharField(max_length=50, null=True, blank=True)
    artistRole = models.CharField(max_length=50, null=True, blank=True)
    artistPrefix = models.CharField(max_length=50, null=True, blank=True)
    artistDisplayName = models.CharField(max_length=50, null=True, blank=True)
    artistDisplayBio = models.CharField(max_length=200, null=True, blank=True)
    artistSuffix = models.CharField(max_length=50, null=True, blank=True)
    artistAlphaSort = models.CharField(max_length=50, null=True, blank=True)
    artistNationality = models.CharField(max_length=50, null=True, blank=True)
    artistBeginDate = models.CharField(max_length=50, null=True, blank=True)
    artistEndDate = models.CharField(max_length=50, null=True, blank=True)
    artistGender = models.CharField(max_length=20,
                                    choices=GENDER_CHOICES,
                                    default='male'
                                    )
    artistWikidata_URL = models.CharField(max_length=50, null=True, blank=True)
    artistULAN_URL = models.CharField(max_length=50, null=True, blank=True)
    objectDate = models.CharField(max_length=50, null=True, blank=True)
    objectBeginDate = models.CharField(max_length=50, null=True, blank=True)
    objectEndDate = models.CharField(max_length=50, null=True, blank=True)
    medium = models.CharField(max_length=50, null=True, blank=True)
    dimensions = models.CharField(max_length=50, null=True, blank=True)
    measurements = models.CharField(max_length=50, null=True, blank=True)
    creditLine = models.CharField(max_length=50, null=True, blank=True)
    geographyType = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    subregion = models.CharField(max_length=50, null=True, blank=True)
    locale = models.CharField(max_length=50, null=True, blank=True)
    locus = models.CharField(max_length=50, null=True, blank=True)
    excavation = models.CharField(max_length=50, null=True, blank=True)
    river = models.CharField(max_length=50, null=True, blank=True)
    classification = models.CharField(max_length=50, null=True, blank=True)
    rightsAndReproduction = models.CharField(max_length=50, null=True, blank=True)
    linkResource = models.CharField(max_length=50, null=True, blank=True)
    metadataDate = models.CharField(max_length=50, null=True, blank=True)
    repository = models.CharField(max_length=50, null=True, blank=True)
    objectURL = models.CharField(max_length=50, null=True, blank=True)
    tags = models.CharField(max_length=50, null=True, blank=True)
    objectWikidata_URL = models.CharField(max_length=50, null=True, blank=True)
    isTimelineWork = models.BooleanField()
    galleryNumber = models.IntegerField(null=True, blank=True)
    constituentID = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    constituentULAN_URL = models.CharField(max_length=50, null=True, blank=True)
    constituentWikidata_URL = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length = 20,
                              choices=GENDER_CHOICES,
                              default='male'
                              )

    def __str__(self):
        return str(self.objectId)



