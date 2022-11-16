package utils

import (
	"crypto/sha256"
	b64 "encoding/base64"
	"strings"
)

func NewSHA256(data []byte) []byte {
	hash := sha256.Sum256(data)
	return hash[:]
}

// b64(repo):b64(package):b64(version)
func GenerateID(pName, pVersion, pRepo string) string {
	pNameB64 := B64Encode([]byte(strings.ToLower(pName)))
	pVersionB64 := B64Encode([]byte(strings.ToLower(pVersion)))
	pRepoB64 := B64Encode([]byte(pRepo))

	joined := pRepoB64 + ":" + pNameB64 + ":" + pVersionB64
	return joined
}

// returns name, version, repo
func DecodeID(pId string) (string, string, string) {
	splits := strings.Split(pId, ":")

	pRepo := B64Decode(splits[0])
	pName := B64Decode(splits[1])
	pVersion := B64Decode(splits[2])
	return string(pName), string(pVersion), string(pRepo)
}

func B64Encode(bytes []byte) string {
	return b64.StdEncoding.EncodeToString([]byte(bytes))
}

func B64Decode(data string) []byte {
	out, _ := b64.StdEncoding.DecodeString(data)
	return out
}

func Contains(arr []string, s string) bool {
	for _, v := range arr {
		if s == v {
			return true
		}
	}
	return false
}
