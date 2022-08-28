package graph

type DBHasAttribute struct {
	ID   int    `db:"id"`
	Name string `db:"name"`
}

type DBAttribute struct {
	Name         string  `db:"name"`
	Type         string  `db:"type"`
	DefaultValue string  `db:"defaultValue"`
	IsCore       string  `db:"isCore"`
	Description  *string `db:"description"`
	Example      *string `db:"example"`
}
