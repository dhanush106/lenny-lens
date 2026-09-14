export function artifactFormat(artifact) {
  return artifact?.format || (artifact?.type === 'artifact' ? artifact?.artifact_type : artifact?.type);
}

export function htmlDocument(content) {
  if (/^\s*<!doctype html>|^\s*<html[\s>]/i.test(content || '')) return content;
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src data:;">
</head>
<body style="margin: 0; padding: 1rem; font-family: system-ui, sans-serif;">
${content}
</body>
</html>`;
}