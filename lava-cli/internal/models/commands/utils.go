package commands

import (
	"dep-tree-gen/utils"
	"fmt"
	"strings"
)

func AnyArrayToString[T any](arr []T) string {
	outStrArray := []string{}
	for _, v := range arr {
		outStrArray = append(outStrArray, fmt.Sprintf("%v", v))
	}
	return "[" + strings.Join(outStrArray, ", ") + "]"
}

// converts an id array to string array
func IdArrayToStringArray(arr []string) []string {
	out := []string{}
	for _, id := range arr {
		pname, pversion, _ := utils.DecodeID(id)
		out = append(out, fmt.Sprintf("%s==%s", pname, pversion))
	}
	return out
}

func IdToString(id string) string {
	pname, pversion, _ := utils.DecodeID(id)
	return pname + "==" + pversion
}
