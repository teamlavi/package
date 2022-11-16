
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
export function parseApiResponse(response, vulns) {
    const { root, nodes } = response

    const vulnData = {}

    for (const dep of root.dependencies) {
        const currentNode = nodes[dep]
        const output = parseApiResponseRecursive(currentNode, nodes, vulns, {})
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
function parseApiResponseRecursive(currentNode, nodes, vulns, visited) {
    if (!currentNode) {
        return []
    }

    const { id, dependencies } = currentNode
    const tempVulnArray = vulns[id] ? vulns[id] : []

    if (tempVulnArray.length !== 0) {
        return [{
            vulnerabilities: tempVulnArray,
            associatedWith: id,
        }]
    }

    for (const dep of dependencies) {
        const n = nodes[dep]
        if (visited[dep]) {
            continue
        } else {
            visited[dep] = true
        }
        const out = parseApiResponseRecursive(n, nodes, vulns, visited)
        
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
        critical: 0,
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
        totals.critical += counts.critical
        totals.high += counts.high
        totals.medium += counts.medium
        totals.low += counts.low
    }
    return [out, totals]
}

function makeCounts(vulnArray) {
    const out = {
        critical: 0,
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
            } else if (vuln.severity === 2) {
                out.high += 1
            } else {
                out.critical += 1
            }
        }
    }
    return out
}

export function getPackagePath(cds, id) {
    if (cds.root.dependencies.includes(id)) {
        return [cds.nodes[id].package]
    }

    const out = []
    for (const node of Object.values(cds.nodes)) {
        if (node.dependencies.includes(id)) {
            const path = getPackagePath(cds, node.id)
            path.push(cds.nodes[id].package)
            return path
        }
    }
    return out
}