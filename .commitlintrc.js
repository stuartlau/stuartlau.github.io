module.exports = {
  extends: ['@commitlint/config-conventional'],
  formatter: '@commitlint/format',
  rules: {
    'header-min-length': [2, 'always', 10],
    'header-max-length': [2, 'always', 72],
    'header-case': [2, 'always', ['sentence-case']],
    'type-empty': [2, 'always'],
    'scope-empty': [0, 'always'],
    'subject-empty': [2, 'always'],
    'subject-full-stop': [0, 'always'],
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'chore',
        'security',
        'delete'
      ]
    ]
  }
};
