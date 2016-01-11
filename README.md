# ArcGISServerGenerateToken #
Generate a token for an ArcGIS Server federated with Portal for ArcGIS using NTLM Security.

## Dependancies ##
The following dependancies are required for this script to run. Given the environment that this script is working is within a secured NTLM environment, I have created a [gist](https://gist.github.com/SamDrummond/c796710fd812e9a25505) which provides instructions on how to install pip and pip packages.

- Requests v2.9.1 - http://docs.python-requests.org/en/latest/
- Requests-ntlm - https://github.com/requests/requests-ntlm

## Example ##

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

status_url = "https://" + session_parameters.web_adaptor + "/" + session_parameters.arcgis_path + "/admin/services/" + \
             service_name + ".MapServer/status"

response = session.handle.post(status_url, data=data)

print response.text
```
