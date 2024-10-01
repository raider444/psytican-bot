# Psytican Bot Helm Chart

## Summary

This chart deploys bot application to Kubernetes cluster.

## Install

```
helm install psytican-bot oci://git.psynet.su/genesis/psytican-bot-experiment/helm/psytican-bot
```

## Values

| Value | Description | Default |
| --- | --- | --- |
| `hostname` | Hostname that will serve the bot | `example.com` |
| `config.logLevel` | Log level | `INFO` |
| `config.webhookMode` | Enables webhook mode. Bot will not pull telegram API. It will liste to webhooks from telegram | `true` |
| `config.converstationTimeout` | Sets timeout for all opened conversation. 0 - disables timeout (use with caution, this can cause bot stuck) | 300 |
| `config.calendarId` | Id of google calendar in format `id@group.calendar.google.com` | `your-google-calendar-id@group.calendar.google.com` |
| `config.vault` | If defined bot can use HashiCorp Vault to store secrets like bot token or Google credetials | `{}` |
| `config.vault.url` | Vault url | - |
| `config.vault.secretPath` | Path to secrets in Vault | - |
| `config.vault.kubernetesRole` | Vault role to use with kubernetes | - |
| `config.acl` | Configure allowed chats and admin users | `{}` |
| `config.acl.allowedChats` | List of allowed chat ids | `[]` |
| `config.acl.adminUsers` | List of users with admin privileges | `[]` |
| `ingress.enabled` | Enables ingress | false |
| `ingress.className` | Name of Ingress Class | `""` |
| `ingress.annotations` | Ingress annotations | `{}` |
| `ingress.tls` | If this scetion exists ingress will apply TLS to ingress | `{}` |
| `ingress.secret` | Name of secret with TLS certificate and private key | `psytican-bot-tls` |
| `resources` | Kubernetes resource definition (cpu/memory) requests and limits | `{}` |
| `nodeSelector` | Kubernetes node selector | `{}` |
| `tolerations` | Kubernetes tolerations | `[]` |
| `affinity` | Kubernetes affinity | `{}` |
