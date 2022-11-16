package utils

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestGenerateID(t *testing.T) {
	cases := []struct {
		repo     string
		name     string
		version  string
		expected string
	}{
		{"asdf", "fdsa", "4.523.4", "YXNkZg==:ZmRzYQ==:NC41MjMuNA=="},
		{"asdf", "fDSa", "4.523.4", "YXNkZg==:ZmRzYQ==:NC41MjMuNA=="},
	}

	for _, c := range cases {
		t.Run(c.expected, func(t *testing.T) {
			got := GenerateID(c.name, c.version, c.repo)
			assert.Equal(t, got, c.expected)
		})
	}
}

func TestDecodeID(t *testing.T) {
	cases := []struct {
		repo     string
		name     string
		version  string
		expected string
	}{
		{"asdf", "fdsa", "4.523.4", "YXNkZg==:ZmRzYQ==:NC41MjMuNA=="},
		{"asdf", "fDSa", "4.523.4", "YXNkZg==:ZmRzYQ==:NC41MjMuNA=="},
	}

	for _, c := range cases {
		t.Run(c.expected, func(t *testing.T) {
			t.Parallel()
			name, version, repo := DecodeID(c.expected)
			assert.Equal(t, name, strings.ToLower(c.name))       // because we expect things to be lowercase
			assert.Equal(t, repo, strings.ToLower(c.repo))       // because we expect things to be lowercase
			assert.Equal(t, version, strings.ToLower(c.version)) // because we expect things to be lowercase
		})
	}
}
