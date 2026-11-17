/*
 * Copyright 2026 Monster Gaming
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import { parse as parseYaml } from "yaml";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = join(__dirname, "..");
const ISSUE_TEMPLATE_DIR = join(REPO_ROOT, ".github", "ISSUE_TEMPLATE");

const SUPPORTED_BODY_TYPES = new Set([
  "markdown",
  "textarea",
  "input",
  "dropdown",
  "checkboxes",
]);

test("issue form YAML files parse and match GitHub form structure", async (t) => {
  const entries = await readdir(ISSUE_TEMPLATE_DIR, { withFileTypes: true });
  const ymlFiles = entries.filter((e) => e.isFile() && e.name.endsWith(".yml"));

  assert.ok(
    ymlFiles.length > 0,
    `expected at least one .yml issue template under ${ISSUE_TEMPLATE_DIR}`,
  );

  for (const entry of ymlFiles) {
    await t.test(entry.name, async () => {
      const filePath = join(ISSUE_TEMPLATE_DIR, entry.name);
      const raw = await readFile(filePath, "utf8");
      let doc;

      assert.doesNotThrow(() => {
        doc = parseYaml(raw);
      }, `invalid YAML in ${entry.name}`);

      assert.equal(typeof doc.name, "string", "name must be a string");
      assert.ok(doc.name.trim().length > 0, "name must not be empty");

      assert.equal(typeof doc.description, "string", "description must be a string");
      assert.ok(doc.description.trim().length > 0, "description must not be empty");

      assert.ok(Array.isArray(doc.body), "body must be an array");

      const ids = new Set();
      for (let i = 0; i < doc.body.length; i++) {
        const block = doc.body[i];
        assert.ok(block && typeof block === "object", `body[${i}] must be an object`);

        assert.equal(
          typeof block.type,
          "string",
          `body[${i}].type must be a string`,
        );
        assert.ok(
          SUPPORTED_BODY_TYPES.has(block.type),
          `body[${i}].type "${block.type}" is not a supported GitHub form block type`,
        );

        if (block.id !== undefined) {
          assert.equal(typeof block.id, "string", `body[${i}].id must be a string`);
          assert.ok(block.id.trim().length > 0, `body[${i}].id must not be empty`);
          assert.ok(
            !ids.has(block.id),
            `duplicate body id "${block.id}" — ids must be unique`,
          );
          ids.add(block.id);
        }

        if (block.attributes !== undefined) {
          assert.ok(
            block.attributes && typeof block.attributes === "object",
            `body[${i}].attributes must be an object when present`,
          );
        }

        if (block.validations?.required === true && block.id) {
          assert.ok(
            block.attributes && typeof block.attributes.label === "string",
            `body[${i}] is required but missing attributes.label`,
          );
        }
      }
    });
  }
});
