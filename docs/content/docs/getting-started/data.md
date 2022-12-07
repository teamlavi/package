---
id: data
title: Data
permalink: docs/getting-started/data.html
---

Understanding how data is represented throughout the LAVI system is very important to understanding how to use and extend LAVI

## Package IDs

Package names are not guaranteed to be unique across all package repositories. In order to deal with that issue, LAVI developers devised a package naming scheme that follows the convention of
```
base64(repo):base64(package_name):base64(package_version)
```

## CDS

The CDS, or Common Data Structure, is a structure created to aid in the language agnostic principle of this project. The intent of the CDS is to provide a language agnostic dependency tree for any language, that conforms to the same standard. And example tree is below

```json
{
 "cmdType": "npm",
 "repository": "npm",
 "nodes": {
  "bnBt:YXhpb3M=:MC4yMS4w": {
   "id": "bnBt:YXhpb3M=:MC4yMS4w",
   "package": "axios",
   "version": "0.21.0",
   "dependencies": [
    "bnBt:Zm9sbG93LXJlZGlyZWN0cw==:MS4xNS4y"
   ]
  },
  "bnBt:Zm9sbG93LXJlZGlyZWN0cw==:MS4xNS4y": {
   "id": "bnBt:Zm9sbG93LXJlZGlyZWN0cw==:MS4xNS4y",
   "package": "follow-redirects",
   "version": "1.15.2",
   "dependencies": []
  },
  "bnBt:bG9kYXNo:NC4xNy4yMA==": {
   "id": "bnBt:bG9kYXNo:NC4xNy4yMA==",
   "package": "lodash",
   "version": "4.17.20",
   "dependencies": []
  },
  "bnBt:bW9tZW50:Mi4yOS40": {
   "id": "bnBt:bW9tZW50:Mi4yOS40",
   "package": "moment",
   "version": "2.29.4",
   "dependencies": []
  }
 },
 "root": {
  "dependencies": [
   "bnBt:YXhpb3M=:MC4yMS4w",
   "bnBt:bG9kYXNo:NC4xNy4yMA==",
   "bnBt:bW9tZW50:Mi4yOS40"
  ]
 }
}
```

### Fields

* `repository` - The package repository used
* `cmdType` - The command used. This is important for differentiating between trees generated using Poetry or Pip, which both rely on the same repository
* `root` - Defines the root level dependencies of the project
* `nodes` - Enumerates all dependencies, both direct and indirect, in a flat map, where the key is the package ID, and the body contains more details about the dependency.
    * `id` - The package id
    * `package` - The name of the package
    * `version` - The exact version of the package
    * `dependencies` - A string list of package IDs that this node depends on