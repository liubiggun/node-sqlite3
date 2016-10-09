{
  'includes': [ 'common-sqlite.gypi' ],
  'target_defaults': {
    'default_configuration': 'Release',
    'cflags':[
      '-std=c99'
    ],
    'configurations': {
      'Debug': {
        'defines': [ 'DEBUG', '_DEBUG' ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'RuntimeLibrary': 1, # static debug
          },
        },
      },
      'Release': {
        'defines': [ 'NDEBUG' ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'RuntimeLibrary': 0, # static release
          },
        },
      }
    },
    'msvs_settings': {
      'VCCLCompilerTool': {
      },
      'VCLibrarianTool': {
      },
      'VCLinkerTool': {
        'GenerateDebugInformation': 'true',
      },
    },
    'conditions': [
      ['OS == "win"', {
        'defines': [
          'WIN32'
        ],
        'conditions': [
          ['target_arch == "ia32"', {
            'variables': {
              'openssl_root%': 'OpenSSL-Win32',
            }
          }, {
            'variables': {
              'openssl_root%': 'OpenSSL-Win64',
            }
          }]
        ],
        'link_settings': {
          'libraries': [
            '-llibeay32.lib',
            '-lssleay32.lib',
          ],
          'library_dirs': [
            '<(SHARED_INTERMEDIATE_DIR)/sqlite-autoconf-<@(sqlite_version)/<(openssl_root)'
          ]
        }
      }]
    ],
  },

  'targets': [
    {
      'target_name': 'action_before_build',
      'type': 'none',
      'hard_dependency': 1,
      'actions': [
        {
          'action_name': 'unpack_sqlite_dep',
          'inputs': [
            './sqlite-autoconf-<@(sqlite_version).tar.gz'
          ],
          'outputs': [
            '<(SHARED_INTERMEDIATE_DIR)/sqlite-autoconf-<@(sqlite_version)/sqlite3.c'
          ],
          'action': ['python','./extract.py','./sqlite-autoconf-<@(sqlite_version).tar.gz','<(SHARED_INTERMEDIATE_DIR)']
        }
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(SHARED_INTERMEDIATE_DIR)/sqlite-autoconf-<@(sqlite_version)/',
        ]
      },
    },
    {
      'target_name': 'sqlite3',
      'type': 'static_library',
      'include_dirs': [ '<(SHARED_INTERMEDIATE_DIR)/sqlite-autoconf-<@(sqlite_version)/' ],
      'dependencies': [
        'action_before_build'
      ],
      'cflags': [ '-include ../src/gcc-preinclude.h' ],
      'sources': [
        '<(SHARED_INTERMEDIATE_DIR)/sqlite-autoconf-<@(sqlite_version)/sqlite3.c'
      ],
      'direct_dependent_settings': {
        'include_dirs': [ '<(SHARED_INTERMEDIATE_DIR)/sqlite-autoconf-<@(sqlite_version)/' ],
        'defines': [
          'SQLITE_THREADSAFE=1',
          'SQLITE_ENABLE_FTS3',
          'SQLITE_ENABLE_JSON1',
          'SQLITE_ENABLE_RTREE'
        ],
      },
      'cflags_cc': [
          '-Wno-unused-value',
          '-include ../src/gcc-preinclude.h'
      ],
      'defines': [
        '_REENTRANT=1',
        'SQLITE_THREADSAFE=1',
        'SQLITE_ENABLE_FTS3',
        'SQLITE_ENABLE_JSON1',
        'SQLITE_ENABLE_RTREE',
        'SQLITE_HAS_CODEC=1',
        'CODEC_TYPE=CODEC_TYPE_AES128',
        'SQLITE_CORE',
        'THREADSAFE',
        'SQLITE_SECURE_DELETE',
        'SQLITE_SOUNDEX',
        'SQLITE_ENABLE_COLUMN_METADATA',
      ],
      'export_dependent_settings': [
        'action_before_build',
      ]
    }
  ]
}
