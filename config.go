package main

import (
  "encoding/json"
  "os"
)

type Hook struct {
  Repository  string `json:"repository"`
  Branch      string `json:"branch"`
  Execute    *string `json:"execute"`
  File       *string `json:"file"`
}

type ConfigObject struct {
  ListenAddress string `json:"listen"`
  Hooks         []Hook `json:"hooks"`
}

func parseConfig(path string) (*ConfigObject, error) {
  fp, err := os.Open(path)
  if err != nil {
    return nil, err
  }

  defer fp.Close()

  var c ConfigObject

  err = json.NewDecoder(fp).Decode(&c)

  return &c, err
}
