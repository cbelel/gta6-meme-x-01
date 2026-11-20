/**
 * GTA 6 WANTED: an agent earns real money on make.fun.
 * Preserve the post record for the gate, but reject an unpublished placeholder.
 */
import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const source = join(process.env.MAKEFUN_BOT_DIR ?? '/bot', 'POST.json');
const destination = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

try {
  const post = JSON.parse(readFileSync(source, 'utf8'));
  mkdirSync(destination, { recursive: true });
  copyFileSync(source, join(destination, 'POST.json'));
  if (typeof post.url !== 'string' || !/^https:\/\/(x\.com|twitter\.com)\/[A-Za-z0-9_]+\/status\/\d+$/.test(post.url)) {
    throw new Error('POST.json still needs a real public X post URL; placeholder refused.');
  }
  console.log(`Copied public post record from ${new URL(post.url).hostname}.`);
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
}
