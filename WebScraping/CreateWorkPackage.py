import requests
import json
from bs4 import BeautifulSoup
userid='apikey'
passwd='8b61472ad3ccf78f384d489a3aeec1872d1078b0cd9a55170938f476bc9b0b23'
url='http://192.168.99.100:30080/api/v3/work_packages/'
data=json.dumps(
    {
    "description": {
        "format": "markdown",
        "raw": "これは19番です",
        "html": "<p>これは19番です</p>"
    },
    "_embedded": {
        "attachments": {
        "_type": "Collection",
        "total": 0,
        "count": 0,
        "_embedded": {
            "elements": []
        },
        "_links": {
            "self": {
            "href": "/api/v3/work_packages/19/attachments"
            }
        }
        },
        "watchers": {
        "_type": "Collection",
        "total": 0,
        "count": 0,
        "_embedded": {
            "elements": []
        },
        "_links": {
            "self": {
            "href": "/api/v3/work_packages/19/watchers"
            }
        }
        },
        "relations": {
        "_type": "Collection",
        "total": 2,
        "count": 2,
        "_embedded": {
            "elements": [
            {
                "_type": "Relation",
                "id": 26,
                "name": "translation missing: ja.label_",
                "delay": "null",
                "description": "null",
                "_links": {
                "self": {
                    "href": "/api/v3/relations/26"
                },
                "updateImmediately": {
                    "href": "/api/v3/relations/26",
                    "method": "patch"
                },
                "delete": {
                    "href": "/api/v3/relations/26",
                    "method": "delete",
                    "title": "Remove relation"
                },
                "from": {
                    "href": "/api/v3/work_packages/19",
                    "title": "Release v1.0"
                },
                "to": {
                    "href": "/api/v3/work_packages/19",
                    "title": "Release v1.0"
                }
                }
            },
            {
                "_type": "Relation",
                "id": 31,
                "name": "次の項目に後続",
                "type": "follows",
                "reverseType": "precedes",
                "delay": "null",
                "description": "null",
                "_links": {
                "self": {
                    "href": "/api/v3/relations/31"
                },
                "updateImmediately": {
                    "href": "/api/v3/relations/31",
                    "method": "patch"
                },
                "delete": {
                    "href": "/api/v3/relations/31",
                    "method": "delete",
                    "title": "Remove relation"
                },
                "from": {
                    "href": "/api/v3/work_packages/19",
                    "title": "Release v1.0"
                },
                "to": {
                    "href": "/api/v3/work_packages/18",
                    "title": "Develop v1.0"
                }
                }
            }
            ]
        },
        "_links": {
            "self": {
            "href": "/api/v3/work_packages/19/relations"
            }
        }
        },
        "type": {
        "_type": "Type",
        "id": 2,
        "name": "Milestone",
        "color": "#35C53F",
        "position": 2,
        "isDefault": "true",
        "isMilestone": "true",
        "createdAt": "2019-08-24T06:37:39Z",
        "updatedAt": "2019-08-24T06:37:39Z",
        "_links": {
            "self": {
            "href": "/api/v3/types/2",
            "title": "Milestone"
            }
        }
        },
        "priority": {
        "_type": "Priority",
        "id": 10,
        "name": "Immediate",
        "position": 4,
        "color": "#FFA8A8",
        "isDefault": "false",
        "isActive": "true",
        "_links": {
            "self": {
            "href": "/api/v3/priorities/10",
            "title": "Immediate"
            }
        }
        },
        "project": {
        "_type": "Project",
        "id": 1,
        "identifier": "your-scrum-project",
        "name": "Scrum project",
        "description": "*This is a Scrum demo project.*\nYou can edit the project description in the [Project settings -> Description](/projects/your-scrum-project/settings).\n",
        "createdAt": "2019-08-24T06:37:50Z",
        "updatedAt": "2019-08-24T06:37:50Z",
        "_links": {
            "self": {
            "href": "/api/v3/projects/1",
            "title": "Scrum project"
            },
            "createWorkPackage": {
            "href": "/api/v3/projects/1/work_packages/form",
            "method": "post"
            },
            "createWorkPackageImmediate": {
            "href": "/api/v3/projects/1/work_packages",
            "method": "post"
            },
            "categories": {
            "href": "/api/v3/projects/1/categories"
            },
            "versions": {
            "href": "/api/v3/projects/1/versions"
            },
            "types": {
            "href": "/api/v3/projects/1/types"
            }
        }
        },
        "status": {
        "_type": "Status",
        "id": 1,
        "name": "New",
        "isClosed": "false",
        "color": "#C3FAE8",
        "isDefault": "true",
        "isReadonly": "false",
        "defaultDoneRatio": "null",
        "position": 1,
        "_links": {
            "self": {
            "href": "/api/v3/statuses/1",
            "title": "New"
            }
        }
        },
        "author": {
        "_type": "User",
        "id": 1,
        "name": "Admin OpenProject",
        "createdAt": "2019-08-24T06:37:50Z",
        "updatedAt": "2019-08-24T07:12:56Z",
        "login": "admin",
        "admin": "true",
        "firstName": "OpenProject",
        "lastName": "Admin",
        "email": "null",
        "avatar": "http://gravatar.com/avatar/cb4f282fed12016bd18a879c1f27ff97?default=404&secure=false",
        "status": "active",
        "identityUrl": "null",
        "_links": {
            "self": {
            "href": "/api/v3/users/1",
            "title": "Admin OpenProject"
            },
            "showUser": {
            "href": "/users/1",
            "type": "text/html"
            },
            "updateImmediately": {
            "href": "/api/v3/users/1",
            "title": "Update admin",
            "method": "patch"
            },
            "lock": {
            "href": "/api/v3/users/1/lock",
            "title": "Set lock on admin",
            "method": "post"
            }
        }
        },
        "assignee": {
        "_type": "User",
        "id": 1,
        "name": "Admin OpenProject",
        "createdAt": "2019-08-24T06:37:50Z",
        "updatedAt": "2019-08-24T07:12:56Z",
        "login": "admin",
        "admin": "true",
        "firstName": "OpenProject",
        "lastName": "Admin",
        "email": "null",
        "avatar": "http://gravatar.com/avatar/cb4f282fed12016bd18a879c1f27ff97?default=404&secure=false",
        "status": "active",
        "identityUrl": "null",
        "_links": {
            "self": {
            "href": "/api/v3/users/1",
            "title": "Admin OpenProject"
            },
            "showUser": {
            "href": "/users/1",
            "type": "text/html"
            },
            "updateImmediately": {
            "href": "/api/v3/users/1",
            "title": "Update admin",
            "method": "patch"
            },
            "lock": {
            "href": "/api/v3/users/1/lock",
            "title": "Set lock on admin",
            "method": "post"
            }
        }
        },
        "customActions": []
    },
    "_type": "WorkPackage",
    "id": 19,
    "lockVersion": 2,
    "subject": "Release v1.0",
    "date": "2019-09-06",
    "estimatedTime": "null",
    "percentageDone": 0,
    "createdAt": "2019-08-24T06:37:51Z",
    "updatedAt": "2019-08-24T09:41:50Z",
    "remainingTime": "null",
    "_links": {
        "attachments": {
        "href": "/api/v3/work_packages/19/attachments"
        },
        "addAttachment": {
        "href": "/api/v3/work_packages/19/attachments",
        "method": "post"
        },
        "self": {
        "href": "/api/v3/work_packages/19",
        "title": "Release v1.0"
        },
        "update": {
        "href": "/api/v3/work_packages/19/form",
        "method": "post"
        },
        "schema": {
        "href": "/api/v3/work_packages/schemas/1-2"
        },
        "updateImmediately": {
        "href": "/api/v3/work_packages/19",
        "method": "patch"
        },
        "delete": {
        "href": "/api/v3/work_packages/19",
        "method": "delete"
        },
        "move": {
        "href": "/work_packages/19/move/new",
        "type": "text/html",
        "title": "Move Release v1.0"
        },
        "copy": {
        "href": "/work_packages/19/copy",
        "title": "Copy Release v1.0"
        },
        "pdf": {
        "href": "/work_packages/19.pdf",
        "type": "application/pdf",
        "title": "Export as PDF"
        },
        "atom": {
        "href": "/work_packages/19.atom",
        "type": "application/rss+xml",
        "title": "Atom feed"
        },
        "availableRelationCandidates": {
        "href": "/api/v3/work_packages/19/available_relation_candidates",
        "title": "Potential work packages to relate to"
        },
        "customFields": {
        "href": "/projects/your-scrum-project/settings/custom_fields",
        "type": "text/html",
        "title": "Custom fields"
        },
        "configureForm": {
        "href": "/types/2/edit?tab=form_configuration",
        "type": "text/html",
        "title": "Configure form"
        },
        "activities": {
        "href": "/api/v3/work_packages/19/activities"
        },
        "availableWatchers": {
        "href": "/api/v3/work_packages/19/available_watchers"
        },
        "relations": {
        "href": "/api/v3/work_packages/19/relations"
        },
        "revisions": {
        "href": "/api/v3/work_packages/19/revisions"
        },
        "watchers": {
        "href": "/api/v3/work_packages/19/watchers"
        },
        "addWatcher": {
        "href": "/api/v3/work_packages/19/watchers",
        "method": "post",
        "payload": {
            "user": {
            "href": "/api/v3/users/{user_id}"
            }
        },
        "templated": "true"
        },
        "removeWatcher": {
        "href": "/api/v3/work_packages/19/watchers/{user_id}",
        "method": "delete",
        "templated": "true"
        },
        "addRelation": {
        "href": "/api/v3/work_packages/19/relations",
        "method": "post",
        "title": "Add relation"
        },
        "changeParent": {
        "href": "/api/v3/work_packages/19",
        "method": "patch",
        "title": "Change parent of Release v1.0"
        },
        "addComment": {
        "href": "/api/v3/work_packages/19/activities",
        "method": "post",
        "title": "Add comment"
        },
        "previewMarkup": {
        "href": "/api/v3/render/markdown?context=/api/v3/work_packages/19",
        "method": "post"
        },
        "category": {
        "href": "null"
        },
        "type": {
        "href": "/api/v3/types/2",
        "title": "Milestone"
        },
        "priority": {
        "href": "/api/v3/priorities/10",
        "title": "Immediate"
        },
        "project": {
        "href": "/api/v3/projects/1",
        "title": "Scrum project"
        },
        "status": {
        "href": "/api/v3/statuses/1",
        "title": "New"
        },
        "author": {
        "href": "/api/v3/users/1",
        "title": "Admin OpenProject"
        },
        "responsible": {
        "href": "null"
        },
        "assignee": {
        "href": "/api/v3/users/1",
        "title": "Admin OpenProject"
        },
        "version": {
        "href": "null"
        },
        "watch": {
        "href": "/api/v3/work_packages/19/watchers",
        "method": "post",
        "payload": {
            "user": {
            "href": "/api/v3/users/3"
            }
        }
        },
        "ancestors": [],
        "parent": {
        "href": "null",
        "title": "null"
        },
        "customActions": []
    }})
html_doc = requests.post(url, data, headers={'Content-Type': 'application/hal+json'}, auth=(userid, passwd)).text
soup = BeautifulSoup(html_doc, 'html.parser') # BeautifulSoup
print(soup.prettify())