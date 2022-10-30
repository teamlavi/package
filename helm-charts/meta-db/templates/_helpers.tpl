{{- define "meta-db.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "meta-db.fullname" -}}
{{- if contains .Chart.Name .Release.Name }}
{{- .Release.Name | trunc (int (sub 63 10)) | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "meta-db.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "meta-db.selectorLabels" -}}
app.kubernetes.io/name: {{ include "meta-db.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "meta-db.labels" -}}
helm.sh/chart: {{ include "meta-db.chart" . }}
{{ include "meta-db.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
