import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const repositoryRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const html = readFileSync(resolve(repositoryRoot, "index.html"), "utf8");

const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]);
assert.equal(new Set(ids).size, ids.length, "index.html contains duplicate IDs");

const internalAnchors = [...html.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1]
);
for (const anchor of internalAnchors) {
    assert(ids.includes(anchor), `Missing internal anchor target: #${anchor}`);
}

const localReferences = [...html.matchAll(/(?:href|src)="([^"]+)"/g)]
    .map((match) => match[1])
    .filter((reference) => !/^(?:#|https?:|mailto:)/.test(reference))
    .map((reference) => reference.split(/[?#]/, 1)[0]);

for (const reference of localReferences) {
    assert(
        existsSync(resolve(repositoryRoot, reference)),
        `Missing local file referenced by index.html: ${reference}`
    );
}

for (const imageTag of html.match(/<img\b[^>]*>/g) ?? []) {
    assert(/\salt="[^"]+"/.test(imageTag), `Image needs useful alt text: ${imageTag}`);
}

for (const frameTag of html.match(/<iframe\b[^>]*>/g) ?? []) {
    assert(/\stitle="[^"]+"/.test(frameTag), `Iframe needs a title: ${frameTag}`);
}

for (const newWindowLink of html.match(/<a\b[^>]*target="_blank"[^>]*>/g) ?? []) {
    assert(
        /\srel="[^"]*noopener[^"]*"/.test(newWindowLink),
        `New-window link needs rel="noopener": ${newWindowLink}`
    );
}

const analyticsId = "G-73MPK6YJRW";
assert.equal(
    (html.match(new RegExp(analyticsId, "g")) ?? []).length,
    2,
    "The approved analytics ID must appear once in the loader and once in gtag config"
);
assert(
    !/(?:G-2PX9V91ZV0|GTM-ND5ZM8D|google-analytics\.com\/analytics\.js)/i.test(html),
    "A retired or legacy analytics tracker is still present"
);

const inlineScripts = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)];
assert.equal(inlineScripts.length, 1, "Only the approved inline analytics initializer is allowed");
assert(
    inlineScripts[0][1].includes(`gtag('config', '${analyticsId}')`),
    "The inline analytics initializer has an unexpected destination"
);

const analyticsScriptHash = createHash("sha256")
    .update(inlineScripts[0][1].replace(/\r\n/g, "\n"), "utf8")
    .digest("base64");
assert(
    html.includes(`'sha256-${analyticsScriptHash}'`),
    "The Content Security Policy must contain the exact inline analytics script hash"
);
assert(!existsSync(resolve(repositoryRoot, "index.html.bak")), "Backup HTML must not be published");

for (const portfolioEntryId of ["blake-twigden-website", "reconcile-gtfs-comparator"]) {
    assert(
        html.includes(`class="portfolio-item" aria-labelledby="${portfolioEntryId}"`) &&
            html.includes(`id="${portfolioEntryId}"`),
        `Missing dedicated portfolio entry: ${portfolioEntryId}`
    );
}

assert(
    html.includes('href="https://reconcile-gtfs.tomjwhite.chatgpt.site/"'),
    "Missing the live Reconcile link"
);
assert.equal(
    (html.match(/class="portfolio-screenshot"/g) ?? []).length,
    4,
    "The Reconcile portfolio entry must include four screenshots"
);

console.log(
    `Site checks passed: ${ids.length} IDs, ${internalAnchors.length} anchors, ${localReferences.length} local files.`
);
