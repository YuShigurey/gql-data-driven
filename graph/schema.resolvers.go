package graph

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"example/graph/generated"
	"example/graph/model"
	"fmt"
	"math/rand"

	"github.com/jmoiron/sqlx"
	_ "github.com/mattn/go-sqlite3"
)

// CreateTodo is the resolver for the createTodo field.
func (r *mutationResolver) CreateTodo(ctx context.Context, input model.NewTodo) (*model.Todo, error) {
	todo := &model.Todo{
		Text: input.Text,
		ID:   fmt.Sprintf("T%d", rand.Int()),
		User: &model.User{ID: input.UserID, Name: "user " + input.UserID},
	}
	r.todos = append(r.todos, todo)
	return todo, nil
}

// Todos is the resolver for the todos field.
func (r *queryResolver) Todos(ctx context.Context) ([]*model.Todo, error) {
	return r.todos, nil
}

// HasAttributes is the resolver for the hasAttributes field.
func (r *queryResolver) HasAttributes(ctx context.Context, name *string) ([]*model.HasAttribute, error) {
	var ret []*model.HasAttribute

	db, err := sqlx.Connect("sqlite3", "./foo.db")
	if err != nil {
		return nil, err
	}

	queryString := `
	SELECT id, name FROM has_attribute 
	`
	var has []DBHasAttribute
	err = db.Select(&has, queryString)
	if err != nil {
		return nil, err
	}

	for _, hs := range has {
		var as []DBAttribute
		var as1 []*model.Attribute

		id := hs.ID
		queryString := `
		SELECT
		[attribute2].[name],
		[attribute2].[type],
		[attribute2].[defaultValue],
		[attribute2].[isCore],
		[attribute2].[description],
		[attribute2].[example]
	  FROM
		[has_attribute_attribute_link]
		INNER JOIN [attribute] [attribute2] ON [has_attribute_attribute_link].[attribute_id] = [attribute2].[id]
	  WHERE
		(
		  [has_attribute_attribute_link].[has_attribute_id] = ?
		)`
		err = db.Select(&as, queryString, id)
		if err != nil {
			return nil, err
		}

		for _, a := range as {
			as1 = append(as1, &model.Attribute{
				Name:         a.Name,
				Type:         a.Type,
				DefaultValue: a.DefaultValue,
				IsCore:       a.IsCore,
				Description:  a.Description,
				Example:      a.Example,
			})
		}

		ret = append(ret, &model.HasAttribute{
			Name:       hs.Name,
			Attributes: as1,
		})
	}
	return ret, nil
}

// Mutation returns generated.MutationResolver implementation.
func (r *Resolver) Mutation() generated.MutationResolver { return &mutationResolver{r} }

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

type mutationResolver struct{ *Resolver }
type queryResolver struct{ *Resolver }
