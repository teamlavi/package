
// parse json response from api
// returns output in the form of
/* [ (for each root node)
    {
        "package": NAME,
        "version": VER,
        "id": ID,
        "vulnerabilities": []
    }
] */
export function parseApiResponse(response) {
    const { root, nodes } = response

    const vulnData = {}

    for (const dep of root.dependencies) {
        const currentNode = nodes[dep]
        const output = parseApiResponseRecursive(currentNode, nodes, [])
        vulnData[dep] = makeVulnListUnique(output)
    }
    return vulnData
}


// this will create duplicates because multiple packages can depends on the same packages in side a tree
/* 
    A     E
  /   \  /
 B     C
  \   /
    D
*/
function parseApiResponseRecursive(currentNode, nodes, visited) {
    if (!currentNode) {
        return []
    }

    const { id, dependencies, vulnerabilities } = currentNode
    const tempVulnArray = vulnerabilities ? vulnerabilities : []

    if (dependencies.length === 0) {
        if (tempVulnArray.length !== 0) {
            return [{
                vulnerabilities: tempVulnArray,
                associatedWith: id,
            }]
        } else {
            return []
        }
    }
    for (const dep of dependencies) {
        const n = nodes[dep]
        if (visited[dep]) {
            continue
        } else {
            visited[dep] = true
        }
        const out = parseApiResponseRecursive(n, nodes, visited)
        if (out) {
            tempVulnArray.push(...out)
        }
    }
    return tempVulnArray
}

function makeVulnListUnique(list) {
    const foundIds = []
    const out = []

    for (const l of list) {
        if (!foundIds.includes(l.associatedWith)) {
            foundIds.push(l.associatedWith)
            out.push(l)
        }
    }
    return out
}

export function getVulnDataStats(nodes, pkgs) {
    const out = []
    const totals = {
        high: 0,
        medium: 0,
        low: 0
    }
    for (const id of Object.keys(pkgs)) {
        const node = nodes[id]
        const counts = makeCounts(pkgs[id])
        out.push({
            name: node.package,
            version: node.version,
            vulnerabilities: pkgs[id],
            severities: counts
        })
        totals.high += counts.high
        totals.medium += counts.medium
        totals.low += counts.low
    }
    return [out, totals]
}

function makeCounts(vulnArray) {
    const out = {
        high: 0,
        medium: 0,
        low: 0
    }
    for (const p of vulnArray) {
        for (const vuln of p.vulnerabilities) {
            if (vuln.severity === 0) {
                out.low += 1
            } else if (vuln.severity === 1) {
                out.medium += 1
            } else {
                out.high += 1
            }
        }
    }
    return out
}