# ArcGISWebSessionWrapper #
A collection of python classes used to create a 'requests' session for managing request to an on-premise ArcGIS Server
federated with Portal for ArcGIS using NTLM security (active directory).

The session class is used in conjunction with the token class to create a single web session that takes care of authentication and token management.

## Dependancies ##
The following dependancies are required for this script to run. Given the environment that this script is working is within a secured NTLM environment, I have created a [gist](https://gist.github.com/SamDrummond/c796710fd812e9a25505) which provides instructions on how to install pip and pip packages.

- Requests v2.9.1 - http://docs.python-requests.org/en/latest/
- Requests-ntlm - https://github.com/requests/requests-ntlm

## Example Raw Python ##

```Python

import ArcGISWebSession

service_name = "Example_Map_Service_Name"

session_parameters = ArcGISWebSession.SessionParameters
session_parameters.domain = "FakeDomain"
session_parameters.username = "FakeyMcFake"
session_parameters.password = ""F4k3r%"
session_parameters.web_adaptor = "maps.FakePortalURL.com"
session_parameters.arcgis_path = "arcgis" #optional
session_parameters.portal_path = "portal" #optional

session = ArcGISWebSession.Session(session_parameters);
token = ArcGISWebSession.Token(session)

data = {
    "f":"json",
    "token":token.aquire()
}

status_url = "https://" + session_parameters.web_adaptor + "/" + session_parameters.arcgis_path +
             "/admin/services/" + service_name + ".MapServer/status"

response = session.handle.post(status_url, data=data)

print response.text
```

## Example ArcGIS Desktop Python Script ##

This script can be configured in an ArcToolBox with two parameters. The first defines the map service name and can be a data type of "MapServer" the second is the password which should be a 'String Hidden'

```Python

import ArcGISWebSession
import getpass
import arcpy

full_service_name = arcpy.GetParameterAsText(0)

service_name_segments = full_service_name.split('\\')
service_name = service_name_segments[len(service_name_segments) - 1]
arcpy.AddMessage(service_name)

session_parameters = ArcGISWebSession.SessionParameters
session_parameters.domain = "FakeDomain"
session_parameters.username = getpass.getuser()
session_parameters.password = arcpy.GetParameterAsText(1)
session_parameters.web_adaptor = "maps.FakePortalURL.com"
session_parameters.arcgis_path = "arcgis" #optional
session_parameters.portal_path = "portal" #optional

session = ArcGISWebSession.Session(session_parameters);
token = ArcGISWebSession.Token(session)

data = {
    "f":"json",
    "token":token.aquire()
}

status_url = "https://" + session_parameters.web_adaptor + "/" + \
             session_parameters.arcgis_path + "/admin/services/" + \
             service_name + "/status"

response = session.handle.post(status_url, data=data)
arcpy.AddMessage(response.text)
```
