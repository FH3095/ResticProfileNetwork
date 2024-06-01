Restic {{ .ProfileCommand }} ran for profile {{ .ProfileName }}.

Error-Message: {{ .Error.Message }}
Error-CmdLine: {{ .Error.CommandLine }}
Error-ExitCode: {{ .Error.ExitCode }}
Error-StdErr:
{{ .Error.Stderr }}

---

StdOut:
{{ .Stdout }}
