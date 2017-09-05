{
  "variables": {
      # may be redefined in command line on configuration stage
      # "build_librdkafka%": "<!(echo ${BUILD_LIBRDKAFKA:-1})"
      "build_librdkafka%": "1"
  },
  "targets": [
    {
      "target_name": "node-librdkafka",
      "sources": [ "<!@(ls -1 src/*.cc)", ],
      "include_dirs": [
        "<!(node -e \"require('nan')\")",
        "<(module_root_dir)/"
      ],
      'conditions': [
        [
          'OS=="win"',
          {
            'cflags_cc' : [
              '-std=c++11'
            ],
            'msvs_settings': {
              'VCCLCompilerTool': {
                'AdditionalOptions': [
                  '/GR'
                ],
                'AdditionalUsingDirectories': [
                  '<(module_root_dir)/deps/librdkafka/win32/outdir/v120/x64/Release/'
                ]
              }
            },
            'msvs_version': '2013',
            'msbuild_toolset': 'v120',
            "dependencies": [
              "<(module_root_dir)/deps/librdkafka.gyp:librdkafkacpp"
            ],
            'include_dirs': [
              'deps/librdkafka/src-cpp'
            ]
          },
          {
            'conditions': [
              [ "<(build_librdkafka)==1",
                {
                  "dependencies": [
                      "<(module_root_dir)/deps/librdkafka.gyp:librdkafkacpp"
                  ],
                  "include_dirs": [ "deps/librdkafka/src-cpp" ],
                },
                # Else link against globally installed rdkafka and use
                # globally installed headers.  On Debian, you should
                # install the librdkafka1, librdkafka++1, and librdkafka-dev
                # .deb packages.
                {
                  "libraries": ["-lrdkafka", "-lrdkafka++"],
                  "include_dirs": [
                    "/usr/include/librdkafka",
                    "/usr/local/include/librdkafka"
                  ],
                },
              ],
              [
                'OS=="linux"',
                {
                  'cflags_cc' : [
                    '-std=c++11'
                  ],
                  'cflags_cc!': [
                    '-fno-rtti'
                  ]
                }
              ],
              [
                'OS=="mac"',
                {
                  'xcode_settings': {
                    'MACOSX_DEPLOYMENT_TARGET': '10.11',
                    'GCC_ENABLE_CPP_RTTI': 'YES',
                    'OTHER_CPLUSPLUSFLAGS': [
                      '-std=c++11'
                    ],
                  },
                }
              ]
            ]
          }
        ]
      ]
    }
  ]
}
