package commands

type AffectedCountResponse struct {
	PkgsAffected map[string]int `json:"pkgsAffected"` // CVE id -> Number of packages affected
}

func (a AffectedCountResponse) Display() {
	panic("not implemented") // TODO: Implement
}

func (a AffectedCountResponse) Finalize() {
	panic("not implemented") // TODO: Implement
}
