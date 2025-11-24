import path from 'node:path';
import { fileURLToPath } from 'node:url';

import js from '@eslint/js';
import nextPlugin from '@next/eslint-plugin-next';
import prettierConfig from 'eslint-config-prettier';
import importPlugin from 'eslint-plugin-import';
import globals from 'globals';
import tseslint from 'typescript-eslint';

// Alternative to __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default tseslint.config(
  // 0. Global ignore settings
  {
    ignores: [
      'node_modules/',
      '.next/',
      '**/.next/**',
      'dist/',
      '**/dist/**',
      'build/',
      '**/build/**',
    ],
  },

  // 1. Basic settings: ESLint recommended + TypeScript recommended + Node/Browser globals + custom rules
  {
    files: ['**/*.ts', '**/*.tsx'],
    extends: [
      js.configs.recommended,
      ...tseslint.configs.recommended,
      // ...tseslint.configs.recommendedTypeChecked,
    ],
    languageOptions: {
      parserOptions: {
        project: true,
        // tsconfigRootDir: __dirname,
      },
      globals: {
        ...globals.node,
        ...globals.browser,
      },
    },
    plugins: {
      import: importPlugin,
    },
    rules: {
      // --- TypeScript custom rules ---
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': ['error', { ignoreRestSiblings: true, argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-var-requires': 'off',
      '@typescript-eslint/no-empty-interface': 'off',
      '@typescript-eslint/no-empty-function': 'off',
      '@typescript-eslint/no-non-null-assertion': 'off',
      '@typescript-eslint/ban-ts-comment': 'off',
      '@typescript-eslint/no-explicit-any': 'off',

      // --- import/order rules (within TS files) ---
      'import/order': [
        'error', // Severity
        {       // Options
          alphabetize: { order: 'asc' },
          'newlines-between': 'always',
          groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
          pathGroups: [{ pattern: '@flow/**', group: 'internal' }],
          pathGroupsExcludedImportTypes: ['builtin'],
        },
      ],
      'import/no-anonymous-default-export': 'off',

      // --- Other custom rules (within TS files) ---
      'no-empty': 'off',
    },
    settings: {
      // 'import/resolver': { typescript: {} },
    },
  },

  // 2. Basic settings for JavaScript files
  {
    files: ['**/*.{js,mjs,cjs}'],
    languageOptions: {
      globals: {
        ...globals.node,
      },
    },
    plugins: {
      import: importPlugin,
    },
    rules: {
      // --- import/order rules (within JS files) ---
      // ***** Modified here *****
      'import/order': [
        'error', // Severity
        {       // Options (copy same settings as TS files)
          alphabetize: { order: 'asc' },
          'newlines-between': 'always',
          groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
          pathGroups: [{ pattern: '@flow/**', group: 'internal' }],
          pathGroupsExcludedImportTypes: ['builtin'],
        },
      ],
      // ***** End of modifications *****
      'import/no-anonymous-default-export': 'off',
      'no-empty': 'off',
    },
    settings: {
      // 'import/resolver': { node: {} },
    },
  },

  // 3. Settings for Next.js
  {
    files: ['apps/reader/**/*.{js,jsx,ts,tsx}'],
    plugins: {
      '@next/next': nextPlugin,
    },
    rules: {
      ...nextPlugin.configs.recommended.rules,
      // ...nextPlugin.configs['core-web-vitals'].rules,
    },
    settings: {
      next: {
        rootDir: path.join(__dirname, 'apps/reader'),
      },
    },
  },

  // 4. Prettier integration (must be described last)
  prettierConfig,
);
