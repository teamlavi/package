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

func GenerateID(pName, pVersion, pRepo string) string {
	pNameSha := NewSHA256([]byte(strings.ToLower(pName)))
	pVersionSha := NewSHA256([]byte(strings.ToLower(pVersion)))
	pRepoSha := NewSHA256([]byte(pRepo))

	joinedSha := NewSHA256(append(pNameSha, append(pVersionSha, pRepoSha...)...))
	return B64Encode(joinedSha)
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
