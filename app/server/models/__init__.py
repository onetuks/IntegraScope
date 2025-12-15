from app.server.models.mpl import ProblemAnalysisResponse, MplLog, MplResultSet, \
  MplResponse, parse_sap_datetime

__all__ = [
  "ProblemAnalysisResponse",
  "MplLog",
  "MplResultSet",
  "MplResponse",
  "parse_sap_datetime",
]


"""
{
    "d": {
        "__count": "7",
        "results": [
            {
                "__metadata": {
                    "id": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xKgivsDaGSUpuvz-eEFzhKZO')",
                    "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xKgivsDaGSUpuvz-eEFzhKZO')",
                    "type": "com.sap.hci.api.MessageProcessingLog"
                },
                "MessageGuid": "AGk_xKgivsDaGSUpuvz-eEFzhKZO",
                "CorrelationId": "AGk_xKgw-s94x2mK6ZYjCul6BgQj",
                "ApplicationMessageId": null,
                "PredecessorMessageGuid": null,
                "ApplicationMessageType": null,
                "LogStart": "/Date(1765786792442)/",
                "LogEnd": "/Date(1765786794800)/",
                "Sender": null,
                "Receiver": null,
                "IntegrationFlowName": "INTEGRA_SCOPE_TEST",
                "Status": "FAILED",
                "AlternateWebLink": "https://inspien.integrationsuite.cfapps.ap10.hana.ondemand.com:443/shell/monitoring/Messages/%7B%22identifier%22%3A%22AGk_xKgivsDaGSUpuvz-eEFzhKZO%22%7D",
                "IntegrationArtifact": {
                    "__metadata": {
                        "type": "com.sap.hci.api.IntegrationArtifact"
                    },
                    "Id": "INTEGRA_SCOPE_TEST",
                    "Name": "INTEGRA_SCOPE_TEST",
                    "Type": "INTEGRATION_FLOW",
                    "PackageId": "TEST10192",
                    "PackageName": "TEST_10192"
                },
                "LogLevel": "INFO",
                "CustomStatus": "FAILED",
                "ArchivingStatus": "NOT_RELEVANT",
                "ArchivingSenderChannelMessages": false,
                "ArchivingReceiverChannelMessages": false,
                "ArchivingLogAttachments": false,
                "ArchivingPersistedMessages": false,
                "TransactionId": "f116bfb5124f4f0cbda44f0e9fd33a11",
                "PreviousComponentName": "CPI_inspien",
                "LocalComponentName": "CPI_inspien",
                "OriginComponentName": "CPI_inspien",
                "CustomHeaderProperties": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xKgivsDaGSUpuvz-eEFzhKZO')/CustomHeaderProperties"
                    }
                },
                "MessageStoreEntries": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xKgivsDaGSUpuvz-eEFzhKZO')/MessageStoreEntries"
                    }
                },
                "ErrorInformation": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xKgivsDaGSUpuvz-eEFzhKZO')/ErrorInformation"
                    }
                },
                "AdapterAttributes": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xKgivsDaGSUpuvz-eEFzhKZO')/AdapterAttributes"
                    }
                },
                "Attachments": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xKgivsDaGSUpuvz-eEFzhKZO')/Attachments"
                    }
                },
                "Runs": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xKgivsDaGSUpuvz-eEFzhKZO')/Runs"
                    }
                }
            },
            {
                "__metadata": {
                    "id": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xSqDsVNVUpeNZhdlIkhtDaRj')",
                    "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xSqDsVNVUpeNZhdlIkhtDaRj')",
                    "type": "com.sap.hci.api.MessageProcessingLog"
                },
                "MessageGuid": "AGk_xSqDsVNVUpeNZhdlIkhtDaRj",
                "CorrelationId": "AGk_xSqvWPzbbVLY3TVFylVwHmmy",
                "ApplicationMessageId": null,
                "PredecessorMessageGuid": null,
                "ApplicationMessageType": null,
                "LogStart": "/Date(1765786922074)/",
                "LogEnd": "/Date(1765786924320)/",
                "Sender": null,
                "Receiver": null,
                "IntegrationFlowName": "INTEGRA_SCOPE_TEST",
                "Status": "FAILED",
                "AlternateWebLink": "https://inspien.integrationsuite.cfapps.ap10.hana.ondemand.com:443/shell/monitoring/Messages/%7B%22identifier%22%3A%22AGk_xSqDsVNVUpeNZhdlIkhtDaRj%22%7D",
                "IntegrationArtifact": {
                    "__metadata": {
                        "type": "com.sap.hci.api.IntegrationArtifact"
                    },
                    "Id": "INTEGRA_SCOPE_TEST",
                    "Name": "INTEGRA_SCOPE_TEST",
                    "Type": "INTEGRATION_FLOW",
                    "PackageId": "TEST10192",
                    "PackageName": "TEST_10192"
                },
                "LogLevel": "TRACE",
                "CustomStatus": "FAILED",
                "ArchivingStatus": "NOT_RELEVANT",
                "ArchivingSenderChannelMessages": false,
                "ArchivingReceiverChannelMessages": false,
                "ArchivingLogAttachments": false,
                "ArchivingPersistedMessages": false,
                "TransactionId": "eb54566148404243a58f006a87caa26e",
                "PreviousComponentName": "CPI_inspien",
                "LocalComponentName": "CPI_inspien",
                "OriginComponentName": "CPI_inspien",
                "CustomHeaderProperties": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xSqDsVNVUpeNZhdlIkhtDaRj')/CustomHeaderProperties"
                    }
                },
                "MessageStoreEntries": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xSqDsVNVUpeNZhdlIkhtDaRj')/MessageStoreEntries"
                    }
                },
                "ErrorInformation": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xSqDsVNVUpeNZhdlIkhtDaRj')/ErrorInformation"
                    }
                },
                "AdapterAttributes": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xSqDsVNVUpeNZhdlIkhtDaRj')/AdapterAttributes"
                    }
                },
                "Attachments": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xSqDsVNVUpeNZhdlIkhtDaRj')/Attachments"
                    }
                },
                "Runs": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_xSqDsVNVUpeNZhdlIkhtDaRj')/Runs"
                    }
                }
            },
            {
                "__metadata": {
                    "id": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yVRs9uZeiJ8qf7XIm3CQdrTI')",
                    "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yVRs9uZeiJ8qf7XIm3CQdrTI')",
                    "type": "com.sap.hci.api.MessageProcessingLog"
                },
                "MessageGuid": "AGk_yVRs9uZeiJ8qf7XIm3CQdrTI",
                "CorrelationId": "AGk_yVS0KmTl7tWWSN9HBBxQcBAv",
                "ApplicationMessageId": null,
                "PredecessorMessageGuid": null,
                "ApplicationMessageType": null,
                "LogStart": "/Date(1765787988335)/",
                "LogEnd": "/Date(1765788000870)/",
                "Sender": null,
                "Receiver": null,
                "IntegrationFlowName": "OData_10195",
                "Status": "FAILED",
                "AlternateWebLink": "https://inspien.integrationsuite.cfapps.ap10.hana.ondemand.com:443/shell/monitoring/Messages/%7B%22identifier%22%3A%22AGk_yVRs9uZeiJ8qf7XIm3CQdrTI%22%7D",
                "IntegrationArtifact": {
                    "__metadata": {
                        "type": "com.sap.hci.api.IntegrationArtifact"
                    },
                    "Id": "OData_10195",
                    "Name": "OData_10195",
                    "Type": "INTEGRATION_FLOW",
                    "PackageId": "TEST10195",
                    "PackageName": "TEST_10195"
                },
                "LogLevel": "TRACE",
                "CustomStatus": "FAILED",
                "ArchivingStatus": "NOT_RELEVANT",
                "ArchivingSenderChannelMessages": false,
                "ArchivingReceiverChannelMessages": false,
                "ArchivingLogAttachments": false,
                "ArchivingPersistedMessages": false,
                "TransactionId": "a68cafa18ea241a7929257048f9a8d2d",
                "PreviousComponentName": "CPI_inspien",
                "LocalComponentName": "CPI_inspien",
                "OriginComponentName": "CPI_inspien",
                "CustomHeaderProperties": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yVRs9uZeiJ8qf7XIm3CQdrTI')/CustomHeaderProperties"
                    }
                },
                "MessageStoreEntries": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yVRs9uZeiJ8qf7XIm3CQdrTI')/MessageStoreEntries"
                    }
                },
                "ErrorInformation": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yVRs9uZeiJ8qf7XIm3CQdrTI')/ErrorInformation"
                    }
                },
                "AdapterAttributes": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yVRs9uZeiJ8qf7XIm3CQdrTI')/AdapterAttributes"
                    }
                },
                "Attachments": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yVRs9uZeiJ8qf7XIm3CQdrTI')/Attachments"
                    }
                },
                "Runs": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yVRs9uZeiJ8qf7XIm3CQdrTI')/Runs"
                    }
                }
            },
            {
                "__metadata": {
                    "id": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yenHAn1URffFxWC50PKk02kG')",
                    "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yenHAn1URffFxWC50PKk02kG')",
                    "type": "com.sap.hci.api.MessageProcessingLog"
                },
                "MessageGuid": "AGk_yenHAn1URffFxWC50PKk02kG",
                "CorrelationId": "AGk_yemVKHmZGwXN-3xwsVLmlnd0",
                "ApplicationMessageId": null,
                "PredecessorMessageGuid": null,
                "ApplicationMessageType": null,
                "LogStart": "/Date(1765788137772)/",
                "LogEnd": "/Date(1765788149553)/",
                "Sender": null,
                "Receiver": null,
                "IntegrationFlowName": "OData_10195",
                "Status": "FAILED",
                "AlternateWebLink": "https://inspien.integrationsuite.cfapps.ap10.hana.ondemand.com:443/shell/monitoring/Messages/%7B%22identifier%22%3A%22AGk_yenHAn1URffFxWC50PKk02kG%22%7D",
                "IntegrationArtifact": {
                    "__metadata": {
                        "type": "com.sap.hci.api.IntegrationArtifact"
                    },
                    "Id": "OData_10195",
                    "Name": "OData_10195",
                    "Type": "INTEGRATION_FLOW",
                    "PackageId": "TEST10195",
                    "PackageName": "TEST_10195"
                },
                "LogLevel": "TRACE",
                "CustomStatus": "FAILED",
                "ArchivingStatus": "NOT_RELEVANT",
                "ArchivingSenderChannelMessages": false,
                "ArchivingReceiverChannelMessages": false,
                "ArchivingLogAttachments": false,
                "ArchivingPersistedMessages": false,
                "TransactionId": "03050340af844052a01350b0a367e22a",
                "PreviousComponentName": "CPI_inspien",
                "LocalComponentName": "CPI_inspien",
                "OriginComponentName": "CPI_inspien",
                "CustomHeaderProperties": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yenHAn1URffFxWC50PKk02kG')/CustomHeaderProperties"
                    }
                },
                "MessageStoreEntries": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yenHAn1URffFxWC50PKk02kG')/MessageStoreEntries"
                    }
                },
                "ErrorInformation": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yenHAn1URffFxWC50PKk02kG')/ErrorInformation"
                    }
                },
                "AdapterAttributes": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yenHAn1URffFxWC50PKk02kG')/AdapterAttributes"
                    }
                },
                "Attachments": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yenHAn1URffFxWC50PKk02kG')/Attachments"
                    }
                },
                "Runs": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yenHAn1URffFxWC50PKk02kG')/Runs"
                    }
                }
            },
            {
                "__metadata": {
                    "id": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yl0SCO6graUbvlfdQxFjqKdp')",
                    "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yl0SCO6graUbvlfdQxFjqKdp')",
                    "type": "com.sap.hci.api.MessageProcessingLog"
                },
                "MessageGuid": "AGk_yl0SCO6graUbvlfdQxFjqKdp",
                "CorrelationId": "AGk_yl3ity0rdd9sO_nZlH5X3UeJ",
                "ApplicationMessageId": null,
                "PredecessorMessageGuid": null,
                "ApplicationMessageType": null,
                "LogStart": "/Date(1765788253783)/",
                "LogEnd": "/Date(1765788274062)/",
                "Sender": null,
                "Receiver": null,
                "IntegrationFlowName": "OData_10195",
                "Status": "FAILED",
                "AlternateWebLink": "https://inspien.integrationsuite.cfapps.ap10.hana.ondemand.com:443/shell/monitoring/Messages/%7B%22identifier%22%3A%22AGk_yl0SCO6graUbvlfdQxFjqKdp%22%7D",
                "IntegrationArtifact": {
                    "__metadata": {
                        "type": "com.sap.hci.api.IntegrationArtifact"
                    },
                    "Id": "OData_10195",
                    "Name": "OData_10195",
                    "Type": "INTEGRATION_FLOW",
                    "PackageId": "TEST10195",
                    "PackageName": "TEST_10195"
                },
                "LogLevel": "TRACE",
                "CustomStatus": "FAILED",
                "ArchivingStatus": "NOT_RELEVANT",
                "ArchivingSenderChannelMessages": false,
                "ArchivingReceiverChannelMessages": false,
                "ArchivingLogAttachments": false,
                "ArchivingPersistedMessages": false,
                "TransactionId": "d9a18eafbfc84f27b0e166a645fc4389",
                "PreviousComponentName": "CPI_inspien",
                "LocalComponentName": "CPI_inspien",
                "OriginComponentName": "CPI_inspien",
                "CustomHeaderProperties": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yl0SCO6graUbvlfdQxFjqKdp')/CustomHeaderProperties"
                    }
                },
                "MessageStoreEntries": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yl0SCO6graUbvlfdQxFjqKdp')/MessageStoreEntries"
                    }
                },
                "ErrorInformation": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yl0SCO6graUbvlfdQxFjqKdp')/ErrorInformation"
                    }
                },
                "AdapterAttributes": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yl0SCO6graUbvlfdQxFjqKdp')/AdapterAttributes"
                    }
                },
                "Attachments": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yl0SCO6graUbvlfdQxFjqKdp')/Attachments"
                    }
                },
                "Runs": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_yl0SCO6graUbvlfdQxFjqKdp')/Runs"
                    }
                }
            },
            {
                "__metadata": {
                    "id": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zESn71TjoVrFUcuwN50bSMkN')",
                    "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zESn71TjoVrFUcuwN50bSMkN')",
                    "type": "com.sap.hci.api.MessageProcessingLog"
                },
                "MessageGuid": "AGk_zESn71TjoVrFUcuwN50bSMkN",
                "CorrelationId": "AGk_zERt-1dqjmHfbfXxRYCgoHq4",
                "ApplicationMessageId": null,
                "PredecessorMessageGuid": null,
                "ApplicationMessageType": null,
                "LogStart": "/Date(1765788740199)/",
                "LogEnd": "/Date(1765788743361)/",
                "Sender": null,
                "Receiver": null,
                "IntegrationFlowName": "OData_10195",
                "Status": "FAILED",
                "AlternateWebLink": "https://inspien.integrationsuite.cfapps.ap10.hana.ondemand.com:443/shell/monitoring/Messages/%7B%22identifier%22%3A%22AGk_zESn71TjoVrFUcuwN50bSMkN%22%7D",
                "IntegrationArtifact": {
                    "__metadata": {
                        "type": "com.sap.hci.api.IntegrationArtifact"
                    },
                    "Id": "OData_10195",
                    "Name": "OData_10195",
                    "Type": "INTEGRATION_FLOW",
                    "PackageId": "TEST10195",
                    "PackageName": "TEST_10195"
                },
                "LogLevel": "TRACE",
                "CustomStatus": "FAILED",
                "ArchivingStatus": "NOT_RELEVANT",
                "ArchivingSenderChannelMessages": false,
                "ArchivingReceiverChannelMessages": false,
                "ArchivingLogAttachments": false,
                "ArchivingPersistedMessages": false,
                "TransactionId": "ae92b79c5f474cdab23f68d4161dbfc3",
                "PreviousComponentName": "CPI_inspien",
                "LocalComponentName": "CPI_inspien",
                "OriginComponentName": "CPI_inspien",
                "CustomHeaderProperties": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zESn71TjoVrFUcuwN50bSMkN')/CustomHeaderProperties"
                    }
                },
                "MessageStoreEntries": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zESn71TjoVrFUcuwN50bSMkN')/MessageStoreEntries"
                    }
                },
                "ErrorInformation": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zESn71TjoVrFUcuwN50bSMkN')/ErrorInformation"
                    }
                },
                "AdapterAttributes": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zESn71TjoVrFUcuwN50bSMkN')/AdapterAttributes"
                    }
                },
                "Attachments": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zESn71TjoVrFUcuwN50bSMkN')/Attachments"
                    }
                },
                "Runs": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zESn71TjoVrFUcuwN50bSMkN')/Runs"
                    }
                }
            },
            {
                "__metadata": {
                    "id": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zNxrWbi6u9QgwMnv227rAF5G')",
                    "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zNxrWbi6u9QgwMnv227rAF5G')",
                    "type": "com.sap.hci.api.MessageProcessingLog"
                },
                "MessageGuid": "AGk_zNxrWbi6u9QgwMnv227rAF5G",
                "CorrelationId": "AGk_zNz7h3mpYtwyKrneQrPmESdF",
                "ApplicationMessageId": null,
                "PredecessorMessageGuid": null,
                "ApplicationMessageType": null,
                "LogStart": "/Date(1765788892182)/",
                "LogEnd": "/Date(1765788908288)/",
                "Sender": null,
                "Receiver": null,
                "IntegrationFlowName": "OData_10195",
                "Status": "FAILED",
                "AlternateWebLink": "https://inspien.integrationsuite.cfapps.ap10.hana.ondemand.com:443/shell/monitoring/Messages/%7B%22identifier%22%3A%22AGk_zNxrWbi6u9QgwMnv227rAF5G%22%7D",
                "IntegrationArtifact": {
                    "__metadata": {
                        "type": "com.sap.hci.api.IntegrationArtifact"
                    },
                    "Id": "OData_10195",
                    "Name": "OData_10195",
                    "Type": "INTEGRATION_FLOW",
                    "PackageId": "TEST10195",
                    "PackageName": "TEST_10195"
                },
                "LogLevel": "TRACE",
                "CustomStatus": "FAILED",
                "ArchivingStatus": "NOT_RELEVANT",
                "ArchivingSenderChannelMessages": false,
                "ArchivingReceiverChannelMessages": false,
                "ArchivingLogAttachments": false,
                "ArchivingPersistedMessages": false,
                "TransactionId": "a54de26e7aa24a0d98db299d0ad52b55",
                "PreviousComponentName": "CPI_inspien",
                "LocalComponentName": "CPI_inspien",
                "OriginComponentName": "CPI_inspien",
                "CustomHeaderProperties": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zNxrWbi6u9QgwMnv227rAF5G')/CustomHeaderProperties"
                    }
                },
                "MessageStoreEntries": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zNxrWbi6u9QgwMnv227rAF5G')/MessageStoreEntries"
                    }
                },
                "ErrorInformation": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zNxrWbi6u9QgwMnv227rAF5G')/ErrorInformation"
                    }
                },
                "AdapterAttributes": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zNxrWbi6u9QgwMnv227rAF5G')/AdapterAttributes"
                    }
                },
                "Attachments": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zNxrWbi6u9QgwMnv227rAF5G')/Attachments"
                    }
                },
                "Runs": {
                    "__deferred": {
                        "uri": "https://inspien.it-cpi002.cfapps.ap10.hana.ondemand.com:443/api/v1/MessageProcessingLogs('AGk_zNxrWbi6u9QgwMnv227rAF5G')/Runs"
                    }
                }
            }
        ]
    }
}
"""