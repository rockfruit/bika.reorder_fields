from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.interfaces import IAnalysisRequest
from zope.component import adapts
from zope.interface import implements


class AnalysisRequestSchemaExtender(object):
    """I normally use this to reorder fields, but this adapter is only
    useful for Plone's generated views etc.  Not for our own AR add etc.
    So we use the Modifier adapter below for everything.
    """
    adapts(IAnalysisRequest)
    implements(IOrderableSchemaExtender)

    fields = []

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields


class AnalysisRequestSchemaModifier(object):
    """The fields include these:
    schema object:
        Contact
        CCContact
        CCEmails
        Client
        Sample
        Batch
        SubGroup
        Template
        Profile
        SamplingDate
        SampleType
        Specification
        PublicationSpecification
        SamplePoint
        StorageLocation
        ClientOrderNumber
        ClientReference
        ClientSampleID
        SampleCondition
        DefaultContainerType
        AdHoc
        Composite
        ReportDryMatter
        InvoiceExclude
        Analyses
        Invoice
        DateReceived
        DatePublished
        Remarks
        DateSampled
        SampleTypeTitle
        SamplePointTitle
        SampleID
        Priority
    """

    adapts(IAnalysisRequest)
    implements(ISchemaModifier)


    def __init__(self, context):
        self.context = context


    def fiddle(self, schema):
        toremove = ['AdHoc', 'Composite', 'InvoiceExclude', 'Priority']
        for field in toremove:
            schema[field].required = False
            schema[field].widget.visible = False

        schema.moveField('Batch', after='SubGroup')
        schema.moveField('ClientSampleID', before='ClientReference')
        schema.moveField('Template', pos="top")
        schema.moveField('Profile', pos="bottom")

        return schema
