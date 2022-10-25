{{- define "lavi-worker.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "lavi-worker.fullname" -}}
{{- if contains .Chart.Name .Release.Name }}
{{- .Release.Name | trunc (int (sub 63 10)) | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "lavi-worker.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "lavi-worker.selectorLabels" -}}
app.kubernetes.io/name: {{ include "lavi-worker.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "lavi-worker.labels" -}}
helm.sh/chart: {{ include "lavi-worker.chart" . }}
{{ include "lavi-worker.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}