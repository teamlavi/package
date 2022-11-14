{{- define "repo-worker.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "repo-worker.fullname" -}}
{{- if contains .Chart.Name .Release.Name }}
{{- .Release.Name | trunc (int (sub 63 10)) | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "repo-worker.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "repo-worker.selectorLabels" -}}
app.kubernetes.io/name: {{ include "repo-worker.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: api
{{- end }}

{{- define "repo-worker.labels" -}}
helm.sh/chart: {{ include "repo-worker.chart" . }}
{{ include "repo-worker.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

# this will break if the release name is much more than 60 chars, add a trunc if needed
{{- define "repo-worker.redisFullname" -}}
{{ printf "%s-redis" (include "repo-worker.fullname" .) }}
{{- end }}

{{- define "repo-worker.redisSelectorLabels" -}}
app.kubernetes.io/name: {{ include "repo-worker.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: redis
{{- end }}

{{- define "repo-worker.redisLabels" -}}
helm.sh/chart: {{ include "repo-worker.chart" . }}
{{ include "repo-worker.redisSelectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
