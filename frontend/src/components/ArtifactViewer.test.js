import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import { artifactFormat, htmlDocument } from './artifactViewerUtils.js';

test('Artifact Viewer recognizes structured Markdown artifacts', () => {
  assert.equal(artifactFormat({ type: 'artifact', format: 'markdown' }), 'markdown');
});

test('Artifact Viewer wraps HTML with a restrictive CSP', () => {
  const document = htmlDocument('<h1>Safe</h1>');
  assert.match(document, /^<!DOCTYPE html>/);
  assert.match(document, /default-src 'none'/);
  assert.doesNotMatch(document, /<script>/i);
});

test('Artifact Viewer keeps generated HTML in an empty sandbox', async () => {
  const source = await readFile(new URL('./ArtifactViewer.jsx', import.meta.url), 'utf8');
  assert.match(source, /sandbox=""/);
});