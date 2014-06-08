package main

import (
  "log"
  "os"
  "os/exec"
)

type Pushycat struct {
  Hooks []Hook
}

func NewPushycat(hooks []Hook) *Pushycat {
  return &Pushycat{hooks}
}

func writeCommit(path string, commit string) error {
  fp, err := os.Create(path)
  if err != nil {
    return err
  }

  defer fp.Close()

  _, err = fp.WriteString(commit + "\n")

  return err
}

func executeHook(command string) error {
  return exec.Command("bash", "-c", command).Run()
}

func Notify(hook Hook, commit string) error {
  if hook.File != nil {
    err := writeCommit(*hook.File, commit)
    if err != nil {
      log.Printf("error writing commit: %v", err)
    }

    return err
  }

  if hook.Execute != nil {
    err := executeHook(*hook.Execute)
    if err != nil {
      log.Printf("error executing command: %v", err)
    }

    return err
  }

  return nil
}

func (ps *Pushycat) Notify(repository string, branch string, commit string) {
  for _, hook := range ps.Hooks {
    if hook.Repository == repository && hook.Branch == branch {
      Notify(hook, commit)
    }
  }
}
