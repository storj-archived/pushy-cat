package main

import (
  "flag"
  "net/http"
  "log"
)

func main() {
  configPath := flag.String("conf", "/etc/pushycat/hooks.json", "")
  flag.Parse()

  conf, err := parseConfig(*configPath)
  if err != nil {
    log.Panicf("Invalid configuration file: %v", err)
  }

  http.ListenAndServe(
    conf.ListenAddress,
    &GithubHandler{NewPushycat(conf.Hooks)})
}
