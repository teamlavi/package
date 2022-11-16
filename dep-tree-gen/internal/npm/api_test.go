package npm

import (
	"dep-tree-gen/models"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"testing"

	"github.com/stretchr/testify/assert"
)

/*
CASES
1: This tree should generate a diamond
	A
  /   \
 B     C
  \   /
	D
Where A is a direct dependency

2:
	A	  Z
  /   \  / \
 B     C	 D (bundled at a different version)
  \   /		  \
	D			E
*/

var cases = []struct {
	pkg      Package
	lock     PackageLock
	expected models.CDS
}{
	{ // 1
		pkg: Package{
			Name: "asdf",
			Dependencies: map[string]interface{}{
				"A": 0,
			},
		},
		lock: PackageLock{
			Dependencies: map[string]Dependency{
				"A": {
					Version: "1.2.3",
					Requires: map[string]string{
						"B": "",
						"C": "",
					},
				},
				"B": {
					Version: "1.2.3",
					Requires: map[string]string{
						"D": "",
					},
				},
				"C": {
					Version: "1.4.2",
					Requires: map[string]string{
						"D": "",
					},
				},
				"D": {
					Version:  "0.6.9",
					Requires: map[string]string{},
				},
			},
		},
		expected: models.CDS{
			CmdType:    "npm",
			Repository: "npm",
			Nodes: map[string]models.CDSNode{
				"bnBt:YQ==:MS4yLjM=": {
					ID:           "bnBt:YQ==:MS4yLjM=",
					Package:      "A",
					Version:      "1.2.3",
					Dependencies: []string{"bnBt:Yg==:MS4yLjM=", "bnBt:Yw==:MS40LjI="},
				},
				"bnBt:Yg==:MS4yLjM=": {
					ID:           "bnBt:Yg==:MS4yLjM=",
					Package:      "B",
					Version:      "1.2.3",
					Dependencies: []string{"bnBt:ZA==:MC42Ljk="},
				},
				"bnBt:Yw==:MS40LjI=": {
					ID:           "bnBt:Yw==:MS40LjI=",
					Package:      "C",
					Version:      "1.4.2",
					Dependencies: []string{"bnBt:ZA==:MC42Ljk="},
				},
				"bnBt:ZA==:MC42Ljk=": {
					ID:           "bnBt:ZA==:MC42Ljk=",
					Package:      "D",
					Version:      "0.6.9",
					Dependencies: []string{},
				},
			},
			Root: models.CDSNode{
				Dependencies: []string{"bnBt:YQ==:MS4yLjM="},
			},
		},
	},
	{ // 2
		pkg: Package{
			Name: "asdf",
			Dependencies: map[string]interface{}{
				"A": 0,
				"Z": 0,
			},
		},
		lock: PackageLock{
			Dependencies: map[string]Dependency{
				"A": {
					Version: "1.2.3",
					Requires: map[string]string{
						"B": "",
						"C": "",
					},
				},
				"B": {
					Version: "1.2.3",
					Requires: map[string]string{
						"D": "",
					},
				},
				"C": {
					Version: "1.4.2",
					Requires: map[string]string{
						"D": "",
					},
				},
				"D": {
					Version:  "0.6.9",
					Requires: map[string]string{},
				},
				"Z": {
					Version: "0.0.0",
					Requires: map[string]string{
						"C": "",
					},
					Dependencies: map[string]Dependency{
						"D": {
							Version: "6.0.9",
							Requires: map[string]string{
								"E": "",
							},
						},
					},
				},
				"E": {
					Version:  "6.8.2",
					Requires: map[string]string{},
				},
			},
		},
		expected: models.CDS{
			CmdType:    "npm",
			Repository: "npm",
			Nodes: map[string]models.CDSNode{
				"bnBt:YQ==:MS4yLjM=": {
					ID:           "bnBt:YQ==:MS4yLjM=",
					Package:      "A",
					Version:      "1.2.3",
					Dependencies: []string{"bnBt:Yg==:MS4yLjM=", "bnBt:Yw==:MS40LjI="},
				},
				"bnBt:Yg==:MS4yLjM=": {
					ID:           "bnBt:Yg==:MS4yLjM=",
					Package:      "B",
					Version:      "1.2.3",
					Dependencies: []string{"bnBt:ZA==:MC42Ljk="},
				},
				"bnBt:Yw==:MS40LjI=": {
					ID:           "bnBt:Yw==:MS40LjI=",
					Package:      "C",
					Version:      "1.4.2",
					Dependencies: []string{"bnBt:ZA==:MC42Ljk="},
				},
				"bnBt:ZA==:MC42Ljk=": {
					ID:           "bnBt:ZA==:MC42Ljk=",
					Package:      "D",
					Version:      "0.6.9",
					Dependencies: []string{},
				},
				"bnBt:ZA==:Ni4wLjk=": {
					ID:           "bnBt:ZA==:Ni4wLjk=",
					Package:      "D",
					Version:      "6.0.9",
					Dependencies: []string{"bnBt:ZQ==:Ni44LjI="},
				},
				"bnBt:ZQ==:Ni44LjI=": {
					ID:           "bnBt:ZQ==:Ni44LjI=",
					Package:      "E",
					Version:      "6.8.2",
					Dependencies: []string{},
				},
				"bnBt:eg==:MC4wLjA=": {
					ID:           "bnBt:eg==:MC4wLjA=",
					Package:      "Z",
					Version:      "0.0.0",
					Dependencies: []string{"bnBt:Yw==:MS40LjI="},
				},
			},
			Root: models.CDSNode{
				Dependencies: []string{"bnBt:YQ==:MS4yLjM=", "bnBt:eg==:MC4wLjA="},
			},
		},
	},
}

type DisabledList []int

func (d DisabledList) contains(v int) bool {
	for _, c := range d {
		if v == c {
			return true
		}
	}
	return false
}

var DISABLED = DisabledList{}

// just a util func for when needed
func saveCds(cds models.CDS) {
	var fileData []byte
	fileData, _ = json.MarshalIndent(cds, "", " ")
	_ = ioutil.WriteFile("cds.json", fileData, 0644)
}

func TestGenerateTree(t *testing.T) {
	for i, c := range cases {
		i += 1
		if DISABLED.contains(i) {
			continue
		}
		t.Run(fmt.Sprintf("case %d", i), func(t *testing.T) {
			t.Parallel()
			got := c.lock.ToCDS(c.pkg)
			saveCds(got)
			assert.Equal(t, got.CmdType, c.expected.CmdType)
			assert.Equal(t, got.Repository, c.expected.Repository)
			assert.Equal(t, len(got.Nodes), len(c.expected.Nodes))
			assert.True(t, got.Root.IsEqual(c.expected.Root))

			for k := range c.expected.Nodes {
				expectedNode := c.expected.Nodes[k]
				gotNode := got.Nodes[k]
				assert.True(t, expectedNode.IsEqual(gotNode), fmt.Sprintf("nodes for id %s are not equal", k))
			}
		})
	}
}
