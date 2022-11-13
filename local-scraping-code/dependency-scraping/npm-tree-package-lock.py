"""
Create a package.json file with:
    {
        "dependencies": {
            "<pacakge>": ">0.0.0"
        }
    }

run `npm install --package-lock-only` in folder with package.json

package-lock.json includes dependencies and picks versions that will work

LAVI-CLI uses this method

"""
