package models

import "errors"

type Requires = func(lr *LavaRequest) (bool, error)

var REQUIRES_PKG_LIST Requires = func(lr *LavaRequest) (bool, error) {
	if len(lr.Packages) == 0 {
		return false, errors.New("this command requires providing a list of packages")
	}
	return true, nil
}
