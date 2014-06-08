package main

import (
  "strings"
  "encoding/json"
  "net/http"
  "log"
)

func last(pieces []string) string {
  return pieces[len(pieces)-1]
}

type PushEvent struct {
  Ref   string `json:"ref"`
  After string `json:"after"`
}

func (pe PushEvent) Branch() string {
  return last(strings.Split(pe.Ref, "/"))
}

type GithubHandler struct {
  pushycat *Pushycat
}

func (gh *GithubHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
  repository := last(strings.Split(r.URL.Path, "/"))
  eventType  := r.Header.Get("X-Github-Event")

  switch eventType {
  case "ping":
    w.Write([]byte(`{"zen_level": "super"}`))

  case "push":
    var event PushEvent
    err := json.NewDecoder(r.Body).Decode(&event)
    if err != nil {
      http.NotFound(w, r)
      return
    }

    log.Printf("Received push event: %v/%v/%v", repository, event.Branch(), event.After)
    go gh.pushycat.Notify(repository, event.Branch(), event.After)
  }
}
