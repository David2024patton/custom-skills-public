# Knowledge digest: c
Source: https://github.com/aleksandar-todorovic/awesome-c
Generated: 2026-10-23T23:57:16Z
Load ONLY when working in this language/domain.

---

Directory structure:
└── aleksandar-todorovic-awesome-c/
    ├── README.md
    ├── code-of-conduct.md
    ├── CONTRIBUTING.md
    ├── LICENSE
    └── .travis.yml

================================================
FILE: README.md
================================================
# awesome-c [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)[![List Status](https://api.travis-ci.org/aleksandar-todorovic/awesome-c.svg?branch=master)](https://travis-ci.org/aleksandar-todorovic/awesome-c)

A curated list of C good stuff. This list contains *only* [free software](https://en.wikipedia.org/wiki/Free_software) for code, and sellers who aren't evil for physical resources.

**LOOKING FOR MAINTAINERS:** This list is currently pretty much inactive. I'm looking for maintainers that can make it great again. See [#26](https://github.com/aleksandar-todorovic/awesome-c/issues/26) for more info, but the process is simple: add or fix a couple of things in this list and you'll become a contributor to a 850+ stars list.

This list was previously maintained by [@kozross](https://github.com/kozross). He decided to switch the list to a [new platform](https://notabug.org/koz.ross/awesome-c), so I've decided to fork it so we could keep it on GitHub.

Contents
========

## Contents ##

- [Build Systems](#build-systems)
- [Compilers](#compilers)
- [Compiler libraries](#compiler-libraries)
- [Compression](#compression)
- [Crypto](#crypto)
- [Database](#database)
- [Deep Learning](#deep-learning)
- [Documentation Generation](#documentation-generation)
- [Editors](#editors)
- [Embedded Systems](#embedded-systems)
  - [RTOS](#rtos)
- [Environments](#environments)
- [Frameworks](#frameworks)
- [Game Programming](#game-programming)
  - [Engines](#engines)
  - [Resources](#resources)
- [Generic Programming](#generic-programming)
- [Graphics](#graphics)
  - [Graphic APIs](#graphic-apis)
- [Graphical User Interface](#graphical-user-interface)
- [Hashing](#hashing)
- [Image Processing](#image-processing)
- [JSON](#json)
- [Learning, Reference and Tutorials](#learning-reference-and-tutorials)
  - [Online](#online)
      - [Reference](#reference)
        - [Language Standards](#language-standards)
      - [Beginner](#beginner)
      - [Intermediate](#intermediate)
      - [Advanced](#advanced)
      - [Self-study courses](#self-study-courses)
  - [Physical](#physical)
      - [Reference](#reference-1)
      - [Beginner](#beginner-1)
      - [Intermediate](#intermediate-1)
      - [Advanced](#advanced-1)
- [Macros](#macros)
- [Memory Allocators](#memory-allocators)
- [Multimedia](#multimedia)
- [Networking and Internet](#networking-and-internet)
  - [Web Frameworks](#web-frameworks)
- [Numerical](#numerical)
- [Parallel Programming](#parallel-programming)
- [Parsers](#parsers)
- [Regex](#regex)
- [Serialization](#serialization)
- [Source Code Collections](#source-code-collections)
- [Standard Libraries](#standard-libraries)
- [String Manipulation](#string-manipulation)
- [Testing](#testing)
- [Text Editor Extensions](#text-editor-extensions)
  - [Atom](#atom)
  - [Emacs](#emacs)
  - [Vim](#vim)
- [Tools](#tools)
- [Utilities](#utilities)
- [XML](#xml)

## Build Systems ##

These are tools to automate the building and testing of projects in C.

* [aimake](http://nethack4.org/projects/aimake/) - Build tool designed to avoid complex configurations. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [Autoconf](https://www.gnu.org/software/autoconf/autoconf.html) - Extensible package of M4 macros that produce shell scripts to automatically configure software source code packages. Part of the Autotools. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [Automake](https://www.gnu.org/software/automake/automake.html) - Tool for automatically generating `Makefile.in` files compliant with the GNU Coding Standards. Requires the use of Autoconf. Part of the Autotools. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [CMake](https://cmake.org/) - Tools for cross-platform building, testing, and packaging. [`3-clause BSD`](https://gitlab.kitware.com/cmake/cmake/raw/master/Copyright.txt)
* [Jam](https://www.perforce.com/documentation/jam-documentation) - Build system, designed to be easier than make. Understands C build rules implicitly. [`Jam License`](https://en.wikipedia.org/wiki/Perforce_Jam#License)
* [Libtool](https://www.gnu.org/software/libtool/) - Generic library support script. Part of the Autotools. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [Meson](https://mesonbuild.com/) - Extremely fast, user-friendly build system. Based on Ninja. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [Premake](https://github.com/premake/premake-core) - Build script generator for toolsets like Visual Studio, Xcode, or GNU Make. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [SCons](https://www.scons.org/) - An easier, more reliable and faster way to build software. [`MIT`](https://raw.githubusercontent.com/atom/atom/master/LICENSE.md)
* [Ninja](https://github.com/ninja-build/ninja) - Small, simple build system with a focus on speed. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [Bazel](https://bazel.build/) - Build system for various operating systems and targets. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [Buck](https://buck.build/) - Build system created and used by Facebook. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [Qbs](https://doc.qt.io/qbs/) - Modern build tool for software projects. [`LGPL3`](https://code.qt.io/cgit/qbs/qbs.git/tree/LICENSE.LGPLv3)
* [qmake](https://doc.qt.io/qt-5/qmake-manual.html) - Build system included with the Qt Framework. [`GNU GPL3 with Qt Exception`](https://github.com/qt/qtbase/blob/5.11/LICENSE.GPL3-EXCEPT)
* [xmake](https://xmake.io/) - Cross-platform build utility based on lua. [`Apache 2.0`](https://github.com/xmake-io/xmake/blob/master/LICENSE.md )

## Compilers ##

* [Clang](http://clang.llvm.org/) - C compiler for LLVM. Supports C11. [`NCSA`](https://directory.fsf.org/wiki/License:NCSA)
* [CompCert](http://compcert.inria.fr/) - Fully-verified C compiler. Supports almost all of C89. [`GNU GPL2.1 or later`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [GCC](https://gcc.gnu.org/) - Provides a C compiler as part of its compiler set. Supports C11 and OpenMP. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [PCC](http://pcc.ludd.ltu.se/) - Venerable C compiler. Supports C99. [`Various free licenses`](http://pcc.ludd.ltu.se/licenses/)
* [TCC](https://bellard.org/tcc/) - Tiny C Compiler; a small, fast C compiler. Supports C99 (except complex types). [`GNU LGPL2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [Intel SPMD](http://ispc.github.io/) - Compiler for a variant of the C language, for single program, multiple data programming. [`Various licenses`](https://github.com/ispc/ispc/blob/master/LICENSE.txt)
* [ccache](https://ccache.dev/) - Compiler cache designed to speedup recompilation. [`GNU GPL3 or later`](https://ccache.dev/license.html)

## Compiler libraries ##

Libraries for use in compilers, interpreters, and low-level based projects.

* [yasm](http://yasm.tortall.net/) - Yasm Modular Assembler Project. [`2-clause BSD`](https://directory.fsf.org/wiki/License:BSD-2-Clause)

## Compression ##

* [libzip](https://libzip.org/) - A C library for reading, creating, and modifying zip archives. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [lzo](http://www.oberhumer.com/opensource/lzo/) - Very fast data compression library. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [zlib](http://zlib.net/) - Massively-spiffy yet delicately-unobtrusive compression library. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [bzip2](http://www.bzip.org/) - Patent free, high quality data compressor. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [lz4](https://lz4.github.io/lz4/) - Fast Compression algorithm.
* [snappy](https://github.com/google/snappy) - Fast compression library (implementation in C++, native bindings to C).
* [zstd](http://facebook.github.io/zstd/) - Fast real-time compression algorithm [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [brotli](https://github.com/google/brotli) - Generic lossless compression algorithm based on LZ77, Huffman coding and 2nd order context modelling [`MIT`](https://raw.githubusercontent.com/atom/atom/master/LICENSE.md)
* [quicklz](http://www.quicklz.com/index.php) - Fast compression library. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [pixz](https://github.com/vasi/pixz) - Pixz (pronounced pixie) is a parallel, indexing version of `xz`. [`2-clause BSD`](https://directory.fsf.org/wiki/License:BSD-2-Clause)

## Crypto ##

* [GnuTLS](https://www.gnutls.org/) - Secure communication library, implementing SSL, TLS and DTLS. [`GNU LGPL2.1 or later`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [libgcrypt](https://gnupg.org/related_software/libgcrypt/) - General-purpose cryptography library, with a range of available ciphers. [`GNU LGPL2.1or later (code)`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html) and [`GNU GPL2.1 or later (manual and tools)`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [OpenSSL](https://www.openssl.org/) - Implementation of the SSL and TLS protocols, and also includes a cryptography library. [`Dual Licensed under the OpenSSL License and the SSLeay License`](https://www.openssl.org/source/license.html)
* [libsodium](https://download.libsodium.org/doc/) - Modern and easy-to-use crypto library. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [libtomcrypt](https://www.libtom.net/) - Fairly comprehensive, modular and portable cryptographic toolkit. [`Public Domain`](https://creativecommons.org/share-your-work/public-domain/)
* [mbed TLS](https://tls.mbed.org/) - Another crypto implementation for C. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [libressl](https://www.libressl.org/) - Modernized fork of OpenSSL. [`Various Licenses`](https://cvsweb.openbsd.org/cgi-bin/cvsweb/~checkout~/src/lib/libssl/LICENSE?rev=1.12)

## Database ##

This lists databases and data stores with C APIs.

* [BerkeleyDB](https://www.oracle.com/database/berkeley-db/) - Library for a high-performance embedded database for key-value data. [`GNU AGPLv3`](https://www.gnu.org/licenses/agpl-3.0.html)
* [Hiredis](https://github.com/redis/hiredis) - Minimalistic client library for Redis. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [LMDB](https://github.com/LMDB/lmdb) - Ultra-fast, ultra-compact key-value embedded data store. [`OpenLDAP License`](https://directory.fsf.org/wiki/License:OLDAP-2.7)
* [MariaDB](https://mariadb.com/) - Robust, scalable and reliable SQL server, designed to be a drop-in replacement for MySQL. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [mongo-c-driver](http://mongoc.org/) - High-performance client library for [MongoDB](https://www.mongodb.com/). [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [PostgreSQL](https://www.postgresql.org/) - Powerful object-relational database system. [`PostgreSQL licence`](https://opensource.org/licenses/postgresql)
* [recutils](https://www.gnu.org/software/recutils/) - Set of tools and a C library for accessing human-editable, plaintext database files called recfiles. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [Redis](https://redis.io/) - Advanced key-value store. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [sophia](http://sophia.systems/) - Modern, embeddable key-value database. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [SQLite](https://www.sqlite.org/about.html) - Self-contained, serverless, zero-configuration, transactional SQL database engine with a C interface. [`Public Domain`](https://creativecommons.org/share-your-work/public-domain/)
* [UnQLite](https://unqlite.org/) - Self-contained, serverless, zero-configuration, transactional NoSQL engine with a C interface. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)

## Deep Learning ##
* [Darknet](https://pjreddie.com/darknet/) - Open source neural network framework written in C and CUDA. It is fast, easy to install, and supports CPU and GPU computation.

## Documentation Generation ##

* [Cxref](http://www.gedanken.org.uk/software/cxref/) - Generates documentation of C programs in either LaTeX, HTML, RTF or SGML. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [DocOnce](https://hplgit.github.io/doconce/doc/web/index.html) - Modestly-tagged markup language that can be used to generate a range of formats. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [Doxygen](http://www.doxygen.nl/) - The de-facto standard tool for generating C documentation from annotated sources. Can generate a large range of formats. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [GTK-Doc](https://www.gtk.org/gtk-doc/) - Tool for generating C documentation from annotated sources. Has support for the Autotools. [`GNU GPL2.1 (code)`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html) or [`GNU FDL1.1`](https://www.gnu.org/licenses/old-licenses/fdl-1.1.html)

## Editors ##

These are specifically fancier, IDE-type editors. If you want a programmer's text editor, look elsewhere. Besides, whatever choice you make most likely supports C anyway.

* [Anjuta DevStudio](http://anjuta.org/) - The GNOME IDE. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [Atom](https://atom.io/) - Hackable text editor for the 21st century. [`MIT`](https://raw.githubusercontent.com/atom/atom/master/LICENSE.md)
* [Code::Blocks](http://www.codeblocks.org/) - Extensible, configurable IDE supporting C. [`GNU GPL3`](http://www.gnu.org/licenses/gpl-3.0.html)
* [CodeLite](https://codelite.org/) - Cross-platform IDE. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [Eclipse](http://www.eclipse.org/ide/) - IDE written in Java. [`EPL`](https://directory.fsf.org/wiki/License:EPL-1.0)
* [Geany](https://www.geany.org/) - Very small and fast IDE. [`GNU GPL2.1 or later`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [KDevelop](https://www.kdevelop.org/) - The KDE IDE. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [Qt Creator](https://www.qt.io/qt-features-libraries-apis-tools-and-ide/#ide) - Cross-platform IDE written with C++ and Qt, part of the Qt SDK. Supports Clang Code Model. [`GNU GPL3 with Qt exception`](https://github.com/qt-creator/qt-creator/blob/master/LICENSE.GPL3-EXCEPT)
* [Visual Studio Code](https://code.visualstudio.com/) - Code editing, redefined. Visual Studio Code.

## Embedded Systems ##

These are projects that allow one to work with microcontrollers and other resource constrained architectures.

### RTOS ###

A real-time operating system (RTOS) is intended to serve real-time applications that process data with low latency delay.

* [Amazon FreeRTOS](https://aws.amazon.com/freertos/) - RTOS for microcontrollers that makes small, low-power edge devices easy to program. [`MIT`](https://github.com/aws/amazon-freertos/blob/master/LICENSE)
* [ChibiOS](http://www.chibios.org/dokuwiki/doku.php) - RTOS with complete development environment (HAL, drivers, support files, and tools). [`Various Licenses`](http://www.chibios.org/dokuwiki/doku.php?id=chibios:licensing:start)
* [Contiki](http://www.contiki-os.org/) - Connect low-cost, low power microcontrollers to the Internet. [`3-clause BSD`](https://github.com/contiki-os/contiki/blob/master/LICENSE)
* [Zephyr Project](https://www.zephyrproject.org/) - Scalable real-time RTOS supporting multiple hardware architectures, optimized for resource constrained devices. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [RIOT OS](https://www.riot-os.org/) - Real-time multi-threading operating system that supports a range of devices that are typically found in the Internet of Things. [`LGPL-2.1`](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html)

## Environments ##

This is a list of technologies designed to bring Windows into the 21st century with respect to support for C.

* [Cygwin](https://cygwin.com/) - Designed to emulate a POSIX-compatible environment extensively under Windows. [`Various Licenses`](https://cygwin.com/licensing.html)
* [MinGW-w64](http://mingw-w64.yaxm.org/doku.php/start) - Minimalist environment for C development on Windows with 64 bit support. [`Various Licenses`](http://mingw.org/license)

## Frameworks ##

This section has big libraries that provide data structures and other stuff you expect of a 'modern' standard library.

* [APR](http://apr.apache.org/) - Apache Portable Runtime; another library of cross-platform utility functions. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [C Algorithms](https://fragglet.github.io/c-algorithms/) - Collection of common algorithms and data structures for C. [`ISC`](https://directory.fsf.org/wiki/License:ISC)
* [C Macro Collections](https://github.com/LeoVen/C-Macro-Collections) - Header only, macro generated, generic and type-safe Collections in C. [`MIT`](https://spdx.org/licenses/MIT.html)
* [CPL](http://www.eso.org/sci/software/cpl/) - The Common Pipeline Library; a set of libraries designed to be a comprehensive, efficient and robust software toolkit. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [EFL](https://www.enlightenment.org/) - Large collection of useful data structures and functions.
* [GLib](https://wiki.gnome.org/Projects/GLib) - Library of utility functions and structures, designed to be portable, efficient and powerful. [`GNU LGPL2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [GIO](https://developer.gnome.org/gio/) - Modern and easy-to-use VFS API. [`GNU LGPL2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [GObject](https://developer.gnome.org/gobject/stable/) - Object-oriented system and object model for C. [`GNU LGPL2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [libnih](https://github.com/keybuk/libnih) - Lightweight library of C functions and structures. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [libU](http://www.koanlogic.com/libu/) - Small library of basic utilities, including memory allocation, string manipulation and logging. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [PBL](http://www.mission-base.com/peter/source/) - Large library of utilities, featuring data structures, among other things. [`GNU LGPL2.1 or later (library)`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html) or [`GNU GPL2.1 or later (test code)`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [qlibc](http://wolkykim.github.io/qlibc/) - Simple and powerful C library, designed as a replacement for GLib while focusing on being small and light. [`qLib license`](https://github.com/wolkykim/qlibc/blob/master/LICENSE) (similar to [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD))
* [stb](https://github.com/nothings/stb) - Range of single-file libraries for C. [`Public Domain`](https://creativecommons.org/share-your-work/public-domain/)
* [libsrt](https://faragon.github.io/libsrt.html) - Safe Real-Time library for C. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)


## Game Programming ##

### Engines ###

These are provided as examples of C game programming code.

* [Corange](https://github.com/orangeduck/Corange) - Game engine in pure C. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [Darkplaces](https://icculus.org/twilight/darkplaces/) - Modified version of the Quake2 engine. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [ioquake3](https://ioquake3.org/) - The Quake3 engine, freed at last. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [Orx](http://orx-project.org/) - Portable, lightweight, plugin-based, data-driven, 2D-oriented game engine. [`zlib`](https://directory.fsf.org/wiki/License:Zlib)
* [Quake](https://github.com/id-Software/Quake) - The Quake engine. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [Quake2](https://github.com/id-Software/Quake-2) - The Quake2 engine. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [Spearmint](https://clover.moe/spearmint/) - Engine designed for FPS games. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)

### Resources ###

These are libraries of all sorts that are useful for game programming.

* [Allegro](https://liballeg.org/) - Cross-platform, video game development and multimedia library. [`zlib`](https://directory.fsf.org/wiki/License:Zlib)
* [Chipmunk2D](http://chipmunk-physics.net/) - Fast and lightweight 2D game physics library. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [CSFML](https://www.sfml-dev.org/download/csfml/) - Binding for [SFML](https://www.sfml-dev.org/index.php) in C. [`zlib`](https://directory.fsf.org/wiki/License:Zlib)
* [FreeGLUT](http://freeglut.sourceforge.net/) - Alternative to the OpenGL Utility Toolkit. Allows the creation and management of windows with OpenGL contexts. [`X11`](https://directory.fsf.org/wiki/License:X11)
* [GLFW](https://www.glfw.org/) - Multi-platform library for creating windows with OpenGL contexts. [`zlib`](https://directory.fsf.org/wiki/License:Zlib)
* [libao](https://xiph.org/ao/) - Cross-platform audio library with a wide variety of outputs. [`GNU GPL2.1 or later`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [RetroArch](https://www.libretro.com/) - The reference frontend for [libretro](https://www.libretro.com/). [`GNU GPL3`](http://www.gnu.org/licenses/gpl-3.0.html)
* [SDL and SDL2](https://www.libsdl.org/) - Cross-platform development library designed to provide low-level access to audio, keyboard, mouse, joystick and graphics hardware via OpenGL. SDL2 is the most current version. [`zlib`](https://directory.fsf.org/wiki/License:Zlib)
* [raylib](https://www.raylib.com/) - Simple and easy-to-use library to learn videogames programming. [`zlib`](https://directory.fsf.org/wiki/License:Zlib)

## Generic Programming ##

* [klib](http://attractivechaos.github.io/klib/#About) - Small and lightweight implementations of common algorithms and data structures. [`MIT`](https://en.wikipedia.org/wiki/MIT_License)

## Graphics ##

* [Cairo](https://www.cairographics.org/) -2D graphics library. [`GNU LGPL2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html) or [`MPLv1.1`](https://directory.fsf.org/wiki/License:MPL-1.1)
* [Cogl](https://github.com/rib/cogl-web/wiki) - GPU graphics and utilities API. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [Clutter](https://blogs.gnome.org/clutter/get-it/) - UI library based on OpenGL. [`GNU LGPL2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [giflib](https://sourceforge.net/projects/giflib/) - Library for reading and writing gif images. [`MIT`](https://spdx.org/licenses/MIT.html)
* [heman](https://github.com/prideout/heman) - Tiny library of image utilities dealing with height maps, normal maps, distance fields and the like. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [libcaca](https://github.com/cacalabs/libcaca) - ASCII renderer for terminal-based interfaces. [`WTFPLv2`](http://www.wtfpl.net/txt/copying/)
* [libimagequant](https://pngquant.org/lib/) - Small, portable library for high-quality conversion of RGBA images to 8-bit indexed colour images. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [libjpeg-turbo](https://libjpeg-turbo.org/) - Faster library for reading and writing JPEG files. [`Various Licenses`](https://libjpeg-turbo.org/About/License)
* [libpng](http://www.libpng.org) - The official PNG reference library. [`libpng license`](http://www.libpng.org/pub/png/src/libpng-LICENSE.txt)
* [libxmi](https://www.gnu.org/software/libxmi/) - Function library for rasterizing 2D vector graphics. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [mozjpeg](https://github.com/mozilla/mozjpeg) - Improved JPEG encoder. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)

### Graphic APIs ###

* [OpenGL](https://www.opengl.org/) - Industry adopted 2D and 3D graphics API. More resources at [awesome-opengl](https://github.com/eug/awesome-opengl).
* [OpenGL ES](https://www.khronos.org/opengles/) - Industry adopted 2D and 3D graphics API for mobile and embedded devices.
* [OpenGL SC](https://www.khronos.org/openglsc/) - Graphic and compute standard for industry requiring system safety certification.
* [Vulkan](https://www.khronos.org/vulkan/) - Explicit graphic and compute API for modern cross-platform development. More resources at [awesome-vulkan](https://github.com/vinjn/awesome-vulkan).

## Graphical User Interface ##

These are specifically [widget toolkits](https://en.wikipedia.org/wiki/Widget_toolkit).

* [GTK+](https://www.gtk.org/) - Cross-platform widget toolkit. [`GNU LGPL2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [IUP](http://webserver2.tecgraf.puc-rio.br/iup/) - Another cross-platform widget toolkit. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [Tk](http://www.tcl.tk/) - Basic widget toolkit. Part of Tcl/Tk. [`Tcl/Tk License`](http://www.tcl.tk/software/tcltk/license.html)
* [XForms Toolkit](http://xforms-toolkit.org/) - Widget toolkit designed for the XWindow system. [`GNU LGPL2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [nuklear](https://github.com/vurtun/nuklear) - Single-header ANSI C gui library. [`Public Domain`](https://creativecommons.org/share-your-work/public-domain/)
* [libui](https://github.com/andlabs/libui) - Simple and portable (but not inflexible) GUI library. [`MIT`](https://github.com/andlabs/libui/blob/master/LICENSE)
* [LCUI](https://github.com/lc-soft/LCUI/) - Small C library for building user interfaces with C, XML and CSS. [`MIT`](https://github.com/lc-soft/LCUI/blob/develop/LICENSE.TXT)

## Hashing ##

All hashing related libraries, cryptographic or not.

* [jwHash](https://github.com/watmough/jwHash) - Fast hashtable implementation. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [xxHash](http://cyan4973.github.io/xxHash/) - Extremely fast non-cryptographic hash algorithm. [`2-clause BSD`](https://directory.fsf.org/wiki/License:BSD-2-Clause)
* [libcrc](https://github.com/PeterScott/murmur3) - Multi platform CRC library. [`MIT`](https://raw.githubusercontent.com/atom/atom/master/LICENSE.md)
* [murmur](https://github.com/ispc/ispc) - C implementation of MurMur Hashing. [`Public Domain`](https://creativecommons.org/share-your-work/public-domain/)
* [t1ha](https://github.com/leo-yuriev/t1ha) - Fast Positive Hash library. [`zlib`](https://directory.fsf.org/wiki/License:Zlib)

## Image Processing ##

* [libccv](http://libccv.org) - Modern Computer Vision Library. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)

## JSON ##

* [Jansson](http://www.digip.org/jansson/) - C library for encoding, decoding and manipulating JSON. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [jsmn](https://zserge.com/jsmn.html) - Minimalistic JSON parser. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [json-c](https://github.com/json-c/json-c/wiki) - Library for working with JSON. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [parson](https://github.com/kgabis/parson) - Lightweight JSON library written in C. [`MIT`](https://raw.githubusercontent.com/atom/atom/master/LICENSE.md)
* [WJElement](https://github.com/netmail-open/wjelement/wiki) - Advanced JSON manipulation library, with support for JSON Schema. [`LGPL, any version`](https://github.com/netmail-open/wjelement/)
* [YAJL](https://lloyd.github.io/yajl/) - Fast C JSON streaming parser library. [`ISC`](https://directory.fsf.org/wiki/License:ISC)

## Learning, Reference and Tutorials ##

This is a list of resources for learning C programming in general, or something useful relating to C programming.

### Online ###

#### Reference ####

* [SEI CERT C Coding Standard](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard)
* [C FAQ - comp.lang.c Frequently Asked Questions](http://c-faq.com/)
* [Comparison of C/POSIX standard library implementations for GNU/Linux](http://www.etalabs.net/compare_libcs.html)
* [GNU C Reference Manual](https://www.gnu.org/software/gnu-c-manual/)
* [Robert Pike's notes on programming in C](http://www.lysator.liu.se/c/pikestyle.html)
* [Draft ANSI C Rationale](http://port70.net/~nsz/c/c89/rationale/)
* [Draft C99 Rationale](http://port70.net/~nsz/c/c99/C99RationaleV5.10.pdf)

##### Language Standards #####
* [Draft ANSI C (C89) standard](http://port70.net/~nsz/c/c89/c89-draft.txt)
* [Draft C99 standard](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf)
* [Draft C11 standard](http://www.open-std.org/JTC1/SC22/WG14/)

#### Beginner ####

* [Tutorial on pointers](http://www.cs.ucsb.edu/~mikec/cs16/misc/ptrtut12/index.htm)
* [Building C Projects](http://nethack4.org/blog/building-c.html)
* [C Programming Wikibook](https://en.wikibooks.org/wiki/C_Programming)
* [Introduction to 'fun' C](https://gist.github.com/eatonphil/21b3d6569f24ad164365)
* [Learning C with GDB](https://www.recurse.com/blog/5-learning-c-with-gdb)
* [POSIX Threads Programming tutorial](https://computing.llnl.gov/tutorials/pthreads/) (a little dated, but most of it is still valid and useful)
* [The GNU C Programming Tutorial](http://www.crasseux.com/books/ctut.pdf) (online PDF)
* [Templating in C](http://blog.pkh.me/p/20-templating-in-c.html)

#### Intermediate ####

* [8 gdb tricks you should know](https://blogs.oracle.com/linux/8-gdb-tricks-you-should-know-v2)
* [10 C99 tricks](https://blog.noctua-software.com/c-tricks.html)
* [Diving into concurrency: trying out mutexes and atomics](https://jvns.ca/blog/2014/12/14/fun-with-threads/)
* [Introduction to OpenMP](https://www.youtube.com/playlist?list=PLLX-Q6B8xqZ8n8bwjGdzBJ25X2utwnoEG) (video)
* [OpenMP tutorial](https://computing.llnl.gov/tutorials/openMP/) (for the OpenMP3 standard)
* [memcpy vs memmove](https://web.archive.org/web/20170620131430/https://www.tedunangst.com/flak/post/memcpy-vs-memmove)
* [MPI tutorial](https://computing.llnl.gov/tutorials/mpi/)
* [Some unknown features or tricks in C language](https://proprogramming.org/some-unknown-features-or-tricks-in-c-language/)
* [The lost art of C structure packing](http://www.catb.org/esr/structure-packing/)
* [What a C programmer should know about memory](https://marek.vavrusa.com/memory/)
* [What every C programmer should know about undefined behaviour](http://blog.llvm.org/2011/05/what-every-c-programmer-should-know.html)

#### Advanced ####

* [Advanced metaprogramming in C](http://250bpm.com/blog:56)
* [Quick tutorial on implementing and debugging malloc, free, calloc, and realloc](http://danluu.com/malloc-tutorial/)
* [Bit twiddling hacks](https://graphics.stanford.edu/~seander/bithacks.html)
* [I do not know C](https://kukuruku.co/post/i-do-not-know-c/)
* [Implementing smart pointers for the C programming language](https://snai.pe/c/c-smart-pointers/)
* [Inline functions in C](http://www.greenend.org.uk/rjk/tech/inline.html)
* [Metaprogramming custom control structures in C](https://www.chiark.greenend.org.uk/~sgtatham/mp/)
* [Some dark corners of C](https://docs.google.com/presentation/d/1h49gY3TSiayLMXYmRMaAEMl05FaJ-Z6jDOWOz3EsqqQ/edit?pli=1#slide=id.gaf50702c_0153)
* [Writing efficient C and C code optimization](https://www.codeproject.com/articles/6154/writing-efficient-c-and-c-code-optimization)
* [What every programmer should know about memory](https://www.akkadia.org/drepper/cpumemory.pdf)

#### Self-study courses ####

* [C Programming Language Certified Associate preparation course](https://cppinstitute.com/study-resources )

### Physical ###

#### Reference ####

* [C: A Reference Manual 5E](http://careferencemanual.com/) - Full reference book for C99.
* [C Pocket Reference](http://shop.oreilly.com/product/9780596004361.do) - Concise reference book for C99.
* [The C Programming Language 2E](https://en.wikipedia.org/wiki/The_C_Programming_Language) - The original book on C, by its creators.

#### Beginner ####

* [C Primer Plus 6E](https://www.pearson.com/us/higher-education/program/Prata-C-Primer-Plus-6th-Edition/PGM4399.html) - Complete tutorial on programming in C11.
* [C Programming: A Modern Approach](http://knking.com/books/c2/index.html) - Excellent book to learn the basics of C.
* [Head First C](http://shop.oreilly.com/product/0636920015482.do) - 'Head-first' style book for learning C.

#### Intermediate ####

* [21st Century C](http://shop.oreilly.com/product/0636920033677.do) - Very good *second* programming book on C.
* [Understanding and Using C Pointers](http://shop.oreilly.com/product/0636920028000.do) - In-depth resource on pointers in C.
* [ZeroMQ](http://shop.oreilly.com/product/0636920026136.do) - Book for using ZeroMQ with C.

#### Advanced ####

* [Expert C Programming: Deep C Secrets](https://dl.acm.org/citation.cfm?id=179241) - Interesting, in-depth and *entertaining* look at the innards of C.

## Macros ##

* [P99](http://p99.gforge.inria.fr/) - Suite of macros to implement advanced features like default function arguments, scope-bound resources, etc. (Requires C99) [`Q Public License`](https://tldrlegal.com/license/q-public-license-1.0-(qpl-1.0)#summary)

## Memory Allocators ##

Implementations of memory allocators for various systems and platforms.

* [jemalloc](http://jemalloc.net/) - General purpose malloc(3) implementation that emphasizes fragmentation avoidance and scalable concurrency support, commonly used in production systems. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [dlmalloc](http://g.oswego.edu/pub/misc/malloc.c) - Doug Lea's malloc(3) implementation, useful for academic and research purposes. [`Public Domain`](https://creativecommons.org/share-your-work/public-domain/)
* [Hoard](http://hoard.org/) - A Fast, Scalable, and Memory-efficient Malloc for Linux, Windows, Mac, and Solaris. [`GNU GPL2`](http://www.gnu.org/licenses/gpl-3.0.html)
* [nedmalloc](http://www.nedprod.com/programs/portable/nedmalloc/) - An EXTREMELY FAST portable thread caching malloc(3) implementation written in C. [`GNU GPL2`](http://www.gnu.org/licenses/gpl-3.0.html)
* [rpmalloc](https://github.com/rampantpixels/rpmalloc) - Cross platform, lock-free memory allocator. [`Public Domain`](https://creativecommons.org/share-your-work/public-domain/)


## Multimedia ##

* [FFMPEG](https://www.ffmpeg.org/) - Complete, cross-platform solution to record, convert and stream audio and video. [`GNU LGPL2.1 or later`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html) or [`GNU GPL2.1 or later (some parts)`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [GStreamer](https://gstreamer.freedesktop.org/) - Framework for audio and visual media. [`GNU LGPL2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [lodepng](https://lodev.org/lodepng/) - Simple PNG image decoder and encoder, requiring no other dependencies. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [libsoup](https://wiki.gnome.org/action/show/Projects/libsoup?action=show&redirect=LibSoup) - GNOME HTTP client/server library. Uses GObject. [`GNU LGPL2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [libmpv](https://mpv.io/) - Music-playing library. Compile with ``./waf configure --disable-cplayer --enable-libmpv-shared`` to not have the music player. [`GNU GPL2.1 or later`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [libsoundio](http://libsound.io/) - Library for cross-platform, real-time audio input and output. Has a range of back-ends. [`Expat`](https://directory.fsf.org/wiki/License:Expat)


## Networking and Internet ##

* [asnlc](http://lionet.info/asn1c/compiler.html) - Compiler of ASN.1 specifications into C source code. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [czmq](http://czmq.zeromq.org/) - High-level binding for ZeroMQ. [`MPL2.0`](https://www.gnu.org/licenses/license-list.html#MPL-2.0)
* [GNU adns](https://www.gnu.org/software/adns/) - Advanced, easy-to-use, asynch-capable DNS client library and utilities. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [GNU SASL](https://www.gnu.org/software/gsasl/) - Implementation of the Simple Authentication and Security Layer and a few common SASL mechanism. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [GnuTLS](https://www.gnutls.org/) - Secure communication library, implementing SSL, TLS and DTLS. [`GNU LGPL2.1 or later`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [gumbo-parser](https://github.com/google/gumbo-parser) - HTML5 parsing library in C99. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [http-parser](https://github.com/nodejs/http-parser) - HTTP request/response parser. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [ldns](https://www.nlnetlabs.nl/projects/ldns/index.html) - Library to simplify DNS programming. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [libcurl](https://curl.haxx.se/libcurl/) - Client-side URL transfer library, supporting a wide range of formats. [`curl license`](https://curl.haxx.se/docs/copyright.html)
* [LibEtPan](http://www.etpan.org/) - Mail library providing an efficient network for IMAP, SMTP, POP and NNTP. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [libev](http://software.schmorp.de/pkg/libev.html) - Yet another event loop. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [libuv](http://libuv.org/) - Cross-platform asynchronous I/O. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [libevent](http://libevent.org/) - Event loop replacement for network servers. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [libgss](https://www.gnu.org/software/gss/) - Generic Security Service. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [libhttpd](https://hughes.com.au/products/libhttpd/) - Library to add basic web server capabilities to an application or embedded device. [`GNU GPL2`](http://www.gnu.org/licenses/gpl-3.0.html)
* [libidn](https://www.gnu.org/software/libidn/) - Implementation of the Stringprep, Punycode and IDNA specifications. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [libmicrohttpd](https://www.gnu.org/software/libmicrohttpd/) - Small C library that makes it easy to run an HTTP server as part of another application. [`GNU LGPL2.1 or later`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [libsagui](https://risoflora.github.io/libsagui/) - Sagui is a cross-platform C library which helps to develop web servers or frameworks. [`GNU LGPL3`](http://www.gnu.org/licenses/lgpl-3.0.html)
* [libvldmail](https://github.com/dertuxmalwieder/libvldmail) - Your friendly e-mail address validation library. [`WTFPLv2`](http://www.wtfpl.net/txt/copying/)
* [lwan](https://lwan.ws/) - Experimental, scalable, high-performance HTTP server. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [mongoose](https://cesanta.com/) - Embedded web server for C. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [MQTT-C](https://github.com/LiamBindle/MQTT-C) - Portable MQTT C client for embedded systems and PCs alike. [`MIT`](https://raw.githubusercontent.com/LiamBindle/MQTT-C/master/LICENSE)
* [nanomsg](https://github.com/nanomsg/nanomsg) - C-based implementation of ZeroMQ. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [OpenSSL](https://www.openssl.org/) - Implementation of the SSL and TLS protocols, and also includes a cryptography library. [`Dual Licensed under the OpenSSL License and the SSLeay License`](https://www.openssl.org/source/license.html)
* [oSip](https://www.gnu.org/software/osip/) - SIP implementation in C without additional dependencies. [`GNU LGPLv2.1 or later`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [pig](https://github.com/rafael-santiago/pig) - Linux packet crafting tool. [`GPL2`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [s2n](https://github.com/awslabs/s2n) - C99 implementation of the TLS/SSL protocols, designed to be simple, fast and with security as a priority. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [socket99](https://github.com/silentbicycle/socket99) - C99 wrapper for the BSD sockets API. [`ISC`](https://directory.fsf.org/wiki/License:ISC)
* [Tox](https://tox.chat/) - Communication platform, designed to be a Skype-killer. [`GNU GPL3`](http://www.gnu.org/licenses/gpl-3.0.html)
* [twitc](https://github.com/sinemetu1/twitc) - Mini C library for interacting with the Twitter OAuth API. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [librg](https://github.com/librg/librg) - Library for building simple and elegant cross-platform mmo client-server solutions. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [dyad](https://github.com/rxi/dyad) - Asynchronous networking library. [`MIT`](https://raw.githubusercontent.com/atom/atom/master/LICENSE.md)
* [h2o](https://github.com/h2o/h2o/) - Optimized HTTP/1, HTTP/2 high performance server/library. [`MIT`](https://raw.githubusercontent.com/atom/atom/master/LICENSE.md)

### Web Frameworks ###

* [balde](https://balde.rgm.io/) - Microframework for C based on GLib. [`GNU LGPLv2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [onion](https://www.coralbits.com/libonion/) - C library to create simple HTTP servers and Web Applications. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [kore](https://kore.io/) - Easy to use, scalable and secure web application framework for writing web APIs in C.
* [klone](http://www.koanlogic.com/klone/) - KLone is a fully-featured, multiplatform, web application development framework.
* [duda](http://duda.io/) - Duda I/O is an event-driven and high performant web services framework written in C. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)

## Numerical ##

* [apophenia](http://apophenia.info/) - Library for statistical and scientific computing. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [ATLAS](http://math-atlas.sourceforge.net/) - Automatically Tuned Linear Algebra Software. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [BLAS](http://www.netlib.org/blas/) - Basic Linear Algebra Subprograms; a set of routines that provide vector and matrix operations. [`BLAS license`](http://www.netlib.org/blas/#_licensing)
* [CDFLIB](https://people.sc.fsu.edu/~jburkardt/c_src/cdflib/cdflib.html) - Library with routines to evaluate cumulative density functions fo a variety of standard probability distributions.  Also can compute one parameter of the CDF given the others.  (No license given)
* [cmathl](https://scientificc.github.io/cmathl/) - Pure-C Math library with a great variety of mathematical functions and CMake build support. Seeks to be close to C89/C90 compliant for portability. [`MIT`](https://github.com/ScientificC/cmathl/blob/master/LICENSE)
* [Cuba](http://www.feynarts.de/cuba/) - Library for multidimensional numerical integration. [`GNU LGPLv3`](http://www.gnu.org/licenses/lgpl-3.0.html)
* [FFTW](http://www.fftw.org/) - The Fastest Fourier Transform in the West; a highly-optimized fast Fourier transform routine. [`GNU GPL2.1 or later`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [FLINT](http://flintlib.org/) - Fast Library for Number Theory; a library supporting arithmetic with numbers, polynomials, power series and matrices, among others. [`GNU GPL2.1 or later`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [GLPK](https://www.gnu.org/software/glpk/) - GNU Linear Programming Kit; a package designed for solving large-scale linear programming, mixed integer programming and other related problems. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [GMP](https://gmplib.org/) - GNU Multple Precision Arithmetic Library; a library for arbitrary-precision arithmetic. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html) and [`GNU LGPLv3`](http://www.gnu.org/licenses/lgpl-3.0.html)
* [GNU MPC](http://www.multiprecision.org/mpc/) - Library for complex number arithmetic. [`GNU LGPL3 or later`](http://www.gnu.org/licenses/lgpl-3.0.html)
* [GNU MPFR](https://www.mpfr.org/index.html) - Library for arbitrary-precision floating-point arithmetic. [`GNU LGPL3 or later`](http://www.gnu.org/licenses/lgpl-3.0.html) or [`GNU LGPL2.1 or later (until version 2.4.x)`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [GNU MPRIA](https://www.gnu.org/software/mpria/) - Portable mathematics library for multi-precision rational interval arithmetic. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [GSL](http://www.gnu.org/software/gsl/) - The GNU Scientific Library; a sophisticated numerical library. [`GNU GPL3`](http://www.gnu.org/licenses/gpl-3.0.html)
* [igraph](https://igraph.org/) - Library for creating and manipulating large graphs. [`GNU GPL2`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [KISS FFT](https://sourceforge.net/projects/kissfft/) - Very simple fast Fourier transform library. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [LAPACKE](http://www.netlib.org/lapack/lapacke.html) - C interface to [LAPACK](http://www.netlib.org/lapack/). [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [PARI/GP](http://pari.math.u-bordeaux.fr/) - Computer algebra system for number theory; includes a compiler to C. [`GNU GPL2.1 or later`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [PETSc](https://www.mcs.anl.gov/petsc/) - Suite of data structures and routines for scalable parallel solution of scientific applications modelled by partial differential equations. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [PROB](https://people.sc.fsu.edu/~jburkardt/c_src/prob/prob.html) - Library that handles various discrete and continuous probability density functions.  [`GNU LGPL3`](https://people.sc.fsu.edu/~jburkardt/txt/gnu_lgpl.txt)
* [Yeppp!](https://bitbucket.org/MDukhan/yeppp) - Very fast, SIMD-optimized mathematical library. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)

## Parallel Programming ##

* [cchan](http://repo.hu/projects/cchan/) - Small library for channel constructs for inter-thread communication. [`Public Domain`](https://creativecommons.org/share-your-work/public-domain/)
* [ck](http://concurrencykit.org/) - Concurrency primitives, safe memory reclamation mechanisms and non-blocking data structures. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [mill](http://libmill.org/) - Go-style concurrency in C. [`X11`](https://directory.fsf.org/wiki/License:X11)
* [libdill](http://libdill.org/) - Structured concurrency in C. [`X11`](https://directory.fsf.org/wiki/License:X11)
* [MPICH](http://www.mpich.org/) - Another implementation of MPI. [`MPICH licence`](http://git.mpich.org/mpich.git/blob_plain/6aab201f58d71fc97f2c044d250389ba86ac1e3c:/COPYRIGHT)
* [OpenMP](https://www.openmp.org/) - Set of C pragmas designed to allow for easy parallelization of code. [`3-clause BSD`](https://opensource.org/licenses/BSD-3-Clause)
* [OpenMPI](https://github.com/open-mpi/ompi) - Message passing interface implementation. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [pth](https://www.gnu.org/software/pth/) - Portable implementation for non-preemptive priority-based scheduling for multiple threads of execution. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [pthreads](https://en.wikipedia.org/wiki/POSIX_Threads) - The POSIX thread library.
* [SLEPc](https://bitbucket.org/slepc/slepc) - Software library for the solution of large, sparse eigenvalue problems on parallel computers. [`GNU LGPL3`](http://www.gnu.org/licenses/lgpl-3.0.html)
* [TinyCThread](https://tinycthread.github.io/) - Portable, small implementation of the C11 threads API. [`zlib`](https://directory.fsf.org/wiki/License:Zlib)

## Parsers ##

* [hammer](https://github.com/abiggerhammer/hammer) - Parser combinators for binary formats. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [iniparser](https://github.com/ndevilla/iniparser) - Parser for `.ini` files. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [libconfini](https://github.com/madmurphy/libconfini) - Yet another INI parser. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [libYAML](https://pyyaml.org/wiki/LibYAML) - YAML 1.1 parser and emitter. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [mpc](https://github.com/orangeduck/mpc) - Parser combinator library. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [libucl](https://github.com/vstakhov/libucl) - Universal configuration library parser. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)


## Regex ##

> "Some people, when confronted with a problem, think 'I know, I'll use regular expressions'. Now they have two problems." - Jamie Zawinski.

* [PCRE](http://www.pcre.org/) - Implementation of regexes identical to that of Perl 5. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [regexp4](https://github.com/nasciiboy/recursiveregexpraptor-4) - Simple and complete implementation of regular expressions with its own sintax. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [SLRE](https://github.com/cesanta/slre) - Super Light Regular Expression library; a very small implementation of a subset of Perl regex syntax. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [sregex](https://github.com/openresty/sregex) - Non-backtracking NFA/DFA-based Perl-compatible regex engine library. [`3-clause BSD`](https://opensource.org/licenses/BSD-3-Clause)
* [TRE](https://github.com/laurikari/tre/) - POSIX-compliant, feature-full regex library. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)

## Serialization ##

* [binn](https://github.com/liteserver/binn) - Binary serialization format meant to be compact, fast and easy-to-use. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [c-capnproto](https://github.com/jmckaskill/c-capnproto) - Implementation of the Cap'n Proto serialization protocol. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [cmp](https://github.com/camgunz/cmp) - Implementation of the [MessagePack](https://msgpack.org/) serialization protocol. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [libavro](http://avro.apache.org/docs/current/api/c/index.html#_introduction_to_avro_c) - C implementation of the Avro data serialization system. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [mpack](https://github.com/ludocode/mpack) - Another implementation of the [MessagePack](https://msgpack.org/) serialization protocol. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [netstring-c](https://github.com/liteserver/netstring-c) - Netstring encoder and decoder. [`Public Domain`](https://creativecommons.org/share-your-work/public-domain/)
* [protobuf-c](https://github.com/protobuf-c/protobuf-c) - Implementation of Google Protocol Buffer in C. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [xdr](https://en.wikipedia.org/wiki/External_Data_Representation) - External Data Representation; a standard for data serialization.

Check also: [JSON](#json), [XML](#xml)

## Source Code Collections ##

This contains collections of small source code. If you want something big and integrated, check the Frameworks section.

* [CCAN](http://ccodearchive.net/) - Modelled after Perl's CPAN, this is a big collection of C code that does stuff. The full list is [here](http://ccodearchive.net/list.html).
* [clib](https://github.com/clibs/clib) - Something of a package manager for C. Comes with a [bunch of libraries of its own](https://github.com/clibs/clib/wiki/Packages). [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [gnulib](https://www.gnu.org/software/gnulib/) - Collection of common GNU code.
* [libdjb](http://www.fefe.de/djb/) - Collection of libraries doing various things. [`(Apparently) Public Domain`](https://creativecommons.org/share-your-work/public-domain/)

## Standard Libraries ##

This contains standard C libraries.

* [Bionic](https://github.com/aosp-mirror/platform_bionic) - Google's C standard library, developed for Android. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [dietlibc](http://www.fefe.de/dietlibc/) - C standard library designed for the smallest possible binaries. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [glibc](http://www.gnu.org/software/libc/) - The GNU C Library; an implementation of the C standard library. [`GNU LGPL2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [musl](http://www.musl-libc.org/) - Standard C library, compatible with POSIX 2008 and C11. Designed for static linking. [`Expat`](https://directory.fsf.org/wiki/License:Expat)

## String Manipulation ##

* [bstrlib](http://bstring.sourceforge.net/) - The Better String Library. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause) and [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [ICU](http://site.icu-project.org/) - International Components for Unicode; a library for Unicode support. [`ICU license`](http://source.icu-project.org/repos/icu/icu/tags/latest/LICENSE)
* [libunistring](https://www.gnu.org/software/libunistring/) - Library for manipulating Unicode strings in C. [`GNU LGPL3`](http://www.gnu.org/licenses/lgpl-3.0.html)
* [libgiconv](https://www.gnu.org/software/libiconv/) - Text conversion library. [`GNU LGPL2.1 (library)`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html) or [`GNU GPL3 (*iconv* program)`](http://www.gnu.org/licenses/gpl-3.0.html)
* [SDS](https://github.com/antirez/sds) - Simple Dynamic Strings; a library for handling C strings in a simpler way, but one that is compatible with normal C string functions. Available via [clib](https://github.com/clibs/clib). [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [shoco](http://ed-von-schleck.github.io/shoco/) - Compressor for small text strings. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [smaz](https://github.com/antirez/smaz) - Efficient string compression library. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [utf8.h](https://github.com/sheredom/utf8.h) - Single header utf8 string functions. [`Unlicense`](https://unlicense.org/)
* [utf8proc](https://github.com/JuliaStrings/utf8proc) - Small, clean library for processing UTF-8 Unicode data. [`License`](https://github.com/JuliaStrings/utf8proc/blob/master/LICENSE.md)

## Testing ##

* [CHEAT](http://users.jyu.fi/~sapekiis/cheat/) - Very simple unit testing framework. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [Check](https://libcheck.github.io/check/) - Unit testing framework for C. [`GNU LGPL2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [CMock](http://www.throwtheswitch.org/) - Mock/stub generator for C. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [cmocka](https://cmocka.org/) - Unit testing framework with support for mock objects. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [Criterion](https://criterion.readthedocs.io/en/master/) - KISS, non-intrusive C test framework. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [CUnit](http://cunit.sourceforge.net/) - Another unit testing framework for C. [`GNU LGPL2.0`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [Cutest](https://github.com/rafael-santiago/cutest) - Library for unit testing with memory leak detection (Linux, freeBSD and Windows). [`GPL2`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [minunit](https://github.com/siu/minunit) - Minimal unit testing framework for C. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [munit](https://nemequ.github.io/munit/) - Small but full-featured unit testing framework for C with no dependencies. [`MIT`](https://raw.githubusercontent.com/atom/atom/master/LICENSE.md)
* [Unity](http://www.throwtheswitch.org/) - Simple unit testing framework for C. [`Expat`](https://directory.fsf.org/wiki/License:Expat)

## Text Editor Extensions ##

While practically any decent programmer's text editor supports C, there are some extensions that make it more pleasant. This is categorized by editor.

### Atom ###
* [linter-clang](https://github.com/AtomLinter/linter-clang) - Lint C code in Atom, using Clang. [`MIT`](https://raw.githubusercontent.com/atom/atom/master/LICENSE.md)
* [linter-gcc](https://github.com/hebaishi/linter-gcc) - Lint C code in Atom, using GCC. [`MIT`](https://raw.githubusercontent.com/atom/atom/master/LICENSE.md)

### Emacs ###

* [CEDET](http://cedet.sourceforge.net/) - Collection of Emacs Development Environment Tools; designed to provide IDE-like features to Emacs. Built-in. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [Flycheck](https://github.com/flycheck/flycheck) - Modern syntax checking. For C, it can use either GCC or Clang as a back-end. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [Yasnippet](https://github.com/joaotavora/yasnippet) - Template system, with C templates for common code snippets. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)

### Vim ###

* [Syntastic](https://github.com/vim-syntastic/syntastic) - Syntax checking and linting. [`Do What The Fuck You Want To license`](https://github.com/vim-syntastic/syntastic/blob/master/LICENCE)
* [YouCompleteMe](http://valloric.github.io/YouCompleteMe/) - Code completion engine for Vim. [`GNU GPL3`](http://www.gnu.org/licenses/gpl-3.0.html)

## Tools ##

This is a list of useful programs to help you write and debug C code which are *not* editors, libraries or compilers.

* [Artistic Style](http://astyle.sourceforge.net/) - Fast and small automatic source code formatter that supports C. [`GNU LGPL3`](http://www.gnu.org/licenses/lgpl-3.0.html)
* [address-sanitizer](https://github.com/google/sanitizers) - Fast memory error detector. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [biicode](https://biicode.github.io/biicode/) - Modern dependency manager for C. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [c](https://github.com/ryanmjacobs/c) - Compile and execute C "scripts" in one go on the command line. Also has shebang support. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [c99sh](https://github.com/RhysU/c99sh) - Run C files using hash-bang. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [CBMC](http://www.cprover.org/cbmc/) - C Bounded Model Checker; a tool for verification of array bounds, pointer safety and user-specified assertions. [`Original BSD`](https://directory.fsf.org/wiki/License:BSD-4-Clause)
* [cdecl](https://cdecl.org/) - Online service to translate C declarations into English and vice versa. [`Public Domain`](https://creativecommons.org/share-your-work/public-domain/)
* [cinclude2dot](https://www.flourish.org/cinclude2dot/) - Graphs include dependencies in a C project using Graphviz. [`Any GNU GPL version (due to underspecification in the file)`](https://directory.fsf.org/wiki/Cinclude2dot#tab=Details)
* [Complexity](https://www.gnu.org/software/complexity/) - Tool for measuring the complexity of C source code. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [CScout](https://www.spinellis.gr/cscout/) - Source code analyzer and refactoring browser for collections of C programs. [`GNU GPL3`](http://www.gnu.org/licenses/gpl-3.0.html)
* [DDD](https://www.gnu.org/software/ddd/ddd.html) - Graphical front-end for a range of command-line debuggers. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [GDB](http://www.gnu.org/software/gdb/) - The GNU Project debugger; a debugger for C. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [Glade](https://glade.gnome.org/) - RAD tool to enable quick development of GTK+ GUIs. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [GMSL](https://gmsl.sourceforge.io/) - GNU Make Standard Library; a collection of additional functionality for GNU Make. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [GNU Global](https://www.gnu.org/software/global/) - Source code tagging tool which works with C. [`GNU GPL3`](http://www.gnu.org/licenses/gpl-3.0.html)
* [gprof](http://www.gnu.org/software/binutils/) - Performance analysis tool. Part of GNU binutils. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [Highlight](http://www.andre-simon.de/index.php) - Converts source code to formatted text with nice highlighting. [`GNU GPL3`](http://www.gnu.org/licenses/gpl-3.0.html)
* [include-what-you-use](https://github.com/include-what-you-use/include-what-you-use) - Helps find unecessary inclusions and make suggestions for fixing them. Based on LLVM/Clang (and only works with it). [`NCSA`](https://directory.fsf.org/wiki/License:NCSA)
* [indent](https://www.gnu.org/software/indent/) - Formats C source code automatically to make it easier to read. Also converts from one style of source to another. [`GNU GPLv3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [rr](https://rr-project.org/) - Debugger that records non-deterministic executions to allow for deterministic debugging. [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [tup](http://gittup.org/tup/index.html) - Very fast, file-based, cross-platform build system. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [unifdef](http://dotat.at/prog/unifdef/) - Removes #ifdef and #if directives with their delimited text without touching any other part of the file. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause) and [`FreeBSD`](https://directory.fsf.org/wiki?title=License:FreeBSD)
* [Valgrind](http://www.valgrind.org/) - Range of dynamic analysis tools, including a leak checker. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)

## Utilities ##

This is a 'catch-all' category for anything that doesn't fit well anywhere else.

* [ApeTagLibs](https://github.com/jeremyevans/ape_tag_libs/tree/master/c) - C library for working with APEv2 tags. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [bfd](http://sourceware.org/binutils/docs/bfd/) - Library for manipulating binary object files. Part of GNU binutils. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [cf4ocl](https://fakenmc.github.io/cf4ocl/) - The C Framework for OpenCL; a cross-platform object-oriented framework for developing and benchmarking  [OpenCL](https://www.khronos.org/opencl/) projects. [`GNU LGPL3 (library)`](http://www.gnu.org/licenses/lgpl-3.0.html) or [`GNU GPL3 (project code)`](http://www.gnu.org/licenses/gpl-3.0.html)
* [CommonMark](https://github.com/commonmark/commonmark-spec) - C implementation of the CommonMark spec. [`Various Licenses`](https://github.com/commonmark/commonmark-spec/blob/master/LICENSE)
* [CException](https://github.com/ThrowTheSwitch/CException) - C implementation of exceptions. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [docopt.c](https://github.com/docopt/docopt.c) - C implementation of a command-line option parser. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [dyncall](http://www.dyncall.org/) - Another foreign function interface library. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [FANN](http://leenissen.dk/fann/wp/) - Fast Artifical Neural Network library; an implementation of neural networks. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [Firm](https://pp.ipd.kit.edu/firm/) - C library that provides a graph-based intermediate representation, optimizations and assembly code generation suitable for use in compilers. Comes with an example C front-end under the same license. [`GNU LGPLv2.1`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
* [Genann](https://github.com/codeplea/genann) - Simple neural network library in C. [`Zlib`](https://directory.fsf.org/wiki/License:Zlib)
* [gjrand](https://sourceforge.net/projects/gjrand/) - Library of random-number generation routines. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html) or [`GNU GPLv3`](http://www.gnu.org/licenses/gpl-3.0.html)
* [GNU FreeIPMI](https://www.gnu.org/software/freeipmi/index.html) - In-band and out-of-band IPMI implementation. [`GNU GPL3`](http://www.gnu.org/licenses/gpl-3.0.html)
* [GNU gperf](https://www.gnu.org/software/gperf/) - Perfect hash function generator, given a list of strings. Outputs C code. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [GNU Libffcall](https://www.gnu.org/software/libffcall/) - Collection of libraries for building foreign function interfaces. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [gperftools](https://github.com/gperftools/gperftools) - Collection of utilities for measuring and improving performance. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [huffandpuff](https://github.com/adamierymenko/huffandpuff) - Minimal Huffman encoder and decoder. [`Public Domain`](https://creativecommons.org/share-your-work/public-domain/)
* [kdtree](https://github.com/jtsiomb/kdtree) - Simple library for working with KD-trees. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [Kitsune](http://kitsune-dsu.com/) - Efficient, general-purpose framework for dynamic software updating. [`GNU LGPL3 or later`](http://www.gnu.org/licenses/lgpl-3.0.html)
* [libavl](http://adtinfo.org/libavl.html/index.html) - Library containing a range of self-balancing binary trees. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [libbson](https://github.com/mongodb/libbson) - BSON utility library. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [libCello](http://libcello.org/) - Library introducing higher-level programming to C. [`3-clause BSD`](https://directory.fsf.org/wiki/License:BSD-3-Clause)
* [libffi](https://github.com/libffi/libffi) - Portable foreign-function interface library. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [libgit2](https://libgit2.org/) - Pure C implementation of Git. [`GNU GPL2 only, with a linking exception`](https://github.com/libgit2/libgit2/blob/master/COPYING)
* [libimobiledevice](https://github.com/libimobiledevice/libimobiledevice) - Cross-platform protocol library to communicate with iThings. [`GNU LGPLv2.1 or later (library)`](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html) or [`GNU GPL2.1 or later (tools)`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [libnfc](https://github.com/nfc-tools/libnfc) - Platform-independent Near-Field Communication library. [`GNU LGPL3`](http://www.gnu.org/licenses/lgpl-3.0.html)
* [libPhenom](https://github.com/facebookarchive/libphenom) - Deprecated, here for archival purposes. Eventing framework for building high-scalability and high-performance systems. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [ncurses](https://www.gnu.org/software/ncurses/) - Coloured terminal UI library. [`GNU GPL3 or later`](http://www.gnu.org/licenses/gpl-3.0.html)
* [nope.c](https://github.com/riolet/WAFer) - C-language-based, ultra-light software platform for scalable server-side and networking applications (think node.js for C programmers). [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [pbc](https://github.com/cloudwu/pbc) - Protocol buffers library. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [rabbitmq-c](https://github.com/alanxz/rabbitmq-c) - Client library for [RabbitMQ](https://www.rabbitmq.com/). [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [Ragel](http://www.colm.net/open-source/ragel/) - DSL for state machines that compiles to C. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [Tinyexpr](https://github.com/codeplea/tinyexpr) - Tiny recursive-descent parser, compiler and evaluation engine for simple mathematical expressions. [`zlib`](https://directory.fsf.org/wiki/License:Zlib)
* [uthash](http://troydhanson.github.io/uthash/) - Hash table implementation, allowing existing structures to be stored in a hash table easily. [`1-clause BSD`](http://troydhanson.github.io/uthash/license.html)
* [cpu_features](https://github.com/google/cpu_features) - A cross platform C99 library to get cpu features at runtime. [`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [pblog](https://github.com/google/pblog) - Small, low overhead, structured logging library intended for logging formware events.[`Apache 2.0`](https://directory.fsf.org/wiki/License:Apache-2.0)
* [libelf](https://github.com/WolfgangSt/libelf) - ELF object file access library in C. [`GNU GPL2.1`](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
* [mcpp](http://mcpp.sourceforge.net/) - Portable C preprocessor. [`2-clause BSD`](https://opensource.org/licenses/BSD-2-Clause)
* [libusb](https://libusb.info/) - Generic access to USB devices. [`LGPL2.1`](https://github.com/libusb/libusb/blob/master/COPYING)
* [alsa-lib](https://www.alsa-project.org/main/index.php/Main_Page ) - Userspace library to interact with ALSA. [`LGPL2.1`](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html)
* [Capstone](https://github.com/aquynh/capstone) - Dissasembly/disassembler framework. [`BSD 3-clause`](https://github.com/aquynh/capstone/blob/master/LICENSE.TXT)

## XML ##

> "XML is crap. Really. There are no excuses. XML is nasty to parse for humans, and it's a disaster to parse even for computers. There's just no reason for that horrible crap to exist." - Linus Torvalds

* [Expat](http://www.libexpat.org/) - Stream-oriented XML parser. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [libxml2](http://xmlsoft.org/) - Standards-compliant, portable XML parser. [`Expat`](https://directory.fsf.org/wiki/License:Expat)
* [mini-xml](https://github.com/michaelrsweet/mxml) - Small XML reading and writing library. No dependencies aside from C standard library. [`Apache 2.0 with exceptions`](https://github.com/michaelrsweet/mxml/blob/master/LICENSE)



================================================
FILE: code-of-conduct.md
================================================
# Contributor Code of Conduct

As contributors and maintainers of this project, and in the interest of
fostering an open and welcoming community, we pledge to respect all people who
contribute through reporting issues, posting feature requests, updating
documentation, submitting pull requests or patches, and other activities.

We are committed to making participation in this project a harassment-free
experience for everyone, regardless of level of experience, gender, gender
identity and expression, sexual orientation, disability, personal appearance,
body size, race, ethnicity, age, religion, or nationality.

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery
* Personal attacks
* Trolling or insulting/derogatory comments
* Public or private harassment
* Publishing other's private information, such as physical or electronic
  addresses, without explicit permission
* Other unethical or unprofessional conduct

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

By adopting this Code of Conduct, project maintainers commit themselves to
fairly and consistently applying these principles to every aspect of managing
this project. Project maintainers who do not follow or enforce the Code of
Conduct may be permanently removed from the project team.

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community.

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting a project maintainer at aleksandar@r3bl.me. All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. Maintainers are
obligated to maintain confidentiality with regard to the reporter of an
incident.


This Code of Conduct is adapted from the [Contributor Covenant][homepage],
version 1.3.0, available at
[http://contributor-covenant.org/version/1/3/0/][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/3/0/



================================================
FILE: CONTRIBUTING.md
================================================
# Contribution Guidelines

Please ensure your pull request adheres to the following guidelines:

> If you forget any of these I will nicely ask you to change it in the pull request.

# Updating [README.md](https://github.com/aleksandar-todorovic/awesome-c/blob/master/README.md)

- Make an individual pull request for each suggestion.
- You can either add a link or new categories, or improvements... all are welcome.
  - If you have other ideas for discussion please leave an issue.
- Use the following format: [Project Name][Project Link] - Description. [`License Name`](License Link)
  - Example: `[Clang][38] - C compiler for LLVM. Supports C11. ['NCSA'](https://en.wikipedia.org/wiki/Software_license)`
  - Keep descriptions simple.
  - Licenses are optional, but encouraged.
  - License should be link to the project's license file if applicable.
- Titles should be [capitalized](http://grammar.yourdictionary.com/capitalization/rules-for-capitalization-in-titles.html).
- Make pull request titles descriptive i.e. not `Updated README`.
- Additions should be added to the bottom of the relevant category.
- New sub-category are placed in alphabetical order.
- New categories or improvements to the existing categorization are welcome.
- Check your spelling and grammar.
- Make sure your text editor is set to remove trailing whitespace.
- End all descriptions with a period.
- No Amazon affiliate codes in links for books.
- Add authors in book listing with `by **Author**` format.

# How to contribute from GitHub.com

- Make sure you have a free [GitHub.com](https://github.com/join) account and you are logged in.
- Find an appropriate topic category in the [README.md](https://github.com/aleksandar-todorovic/awesome-c/blob/master/README.md) file to add it under, or add your own if you think it is needed.
- Click the :pencil: button [Edit link](https://github.com/aleksandar-todorovic/awesome-c/edit/master/README.md) on the top right-hand corner of the README.md. This will do two things:
  - Fork the repository to your account.
  - Create a new branch so you can send your changes in a pull request.
- Add your changes.
- Scroll down to the `Propose file change` box and write a commit message and optional extended description.
- Click the `Propose file change` button.

> NOTE: this works the same for any of the files



================================================
FILE: LICENSE
================================================

                GNU Free Documentation License
                 Version 1.3, 3 November 2008


 Copyright (C) 2000, 2001, 2002, 2007, 2008 Free Software Foundation, Inc.
     <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

0. PREAMBLE

The purpose of this License is to make a manual, textbook, or other
functional and useful document "free" in the sense of freedom: to
assure everyone the effective freedom to copy and redistribute it,
with or without modifying it, either commercially or noncommercially.
Secondarily, this License preserves for the author and publisher a way
to get credit for their work, while not being considered responsible
for modifications made by others.

This License is a kind of "copyleft", which means that derivative
works of the document must themselves be free in the same sense.  It
complements the GNU General Public License, which is a copyleft
license designed for free software.

We have designed this License in order to use it for manuals for free
software, because free software needs free documentation: a free
program should come with manuals providing the same freedoms that the
software does.  But this License is not limited to software manuals;
it can be used for any textual work, regardless of subject matter or
whether it is published as a printed book.  We recommend this License
principally for works whose purpose is instruction or reference.


1. APPLICABILITY AND DEFINITIONS

This License applies to any manual or other work, in any medium, that
contains a notice placed by the copyright holder saying it can be
distributed under the terms of this License.  Such a notice grants a
world-wide, royalty-free license, unlimited in duration, to use that
work under the conditions stated herein.  The "Document", below,
refers to any such manual or work.  Any member of the public is a
licensee, and is addressed as "you".  You accept the license if you
copy, modify or distribute the work in a way requiring permission
under copyright law.

A "Modified Version" of the Document means any work containing the
Document or a portion of it, either copied verbatim, or with
modifications and/or translated into another language.

A "Secondary Section" is a named appendix or a front-matter section of
the Document that deals exclusively with the relationship of the
publishers or authors of the Document to the Document's overall
subject (or to related matters) and contains nothing that could fall
directly within that overall subject.  (Thus, if the Document is in
part a textbook of mathematics, a Secondary Section may not explain
any mathematics.)  The relationship could be a matter of historical
connection with the subject or with related matters, or of legal,
commercial, philosophical, ethical or political position regarding
them.

The "Invariant Sections" are certain Secondary Sections whose titles
are designated, as being those of Invariant Sections, in the notice
that says that the Document is released under this License.  If a
section does not fit the above definition of Secondary then it is not
allowed to be designated as Invariant.  The Document may contain zero
Invariant Sections.  If the Document does not identify any Invariant
Sections then there are none.

The "Cover Texts" are certain short passages of text that are listed,
as Front-Cover Texts or Back-Cover Texts, in the notice that says that
the Document is released under this License.  A Front-Cover Text may
be at most 5 words, and a Back-Cover Text may be at most 25 words.

A "Transparent" copy of the Document means a machine-readable copy,
represented in a format whose specification is available to the
general public, that is suitable for revising the document
straightforwardly with generic text editors or (for images composed of
pixels) generic paint programs or (for drawings) some widely available
drawing editor, and that is suitable for input to text formatters or
for automatic translation to a variety of formats suitable for input
to text formatters.  A copy made in an otherwise Transparent file
format whose markup, or absence of markup, has been arranged to thwart
or discourage subsequent modification by readers is not Transparent.
An image format is not Transparent if used for any substantial amount
of text.  A copy that is not "Transparent" is called "Opaque".

Examples of suitable formats for Transparent copies include plain
ASCII without markup, Texinfo input format, LaTeX input format, SGML
or XML using a publicly available DTD, and standard-conforming simple
HTML, PostScript or PDF designed for human modification.  Examples of
transparent image formats include PNG, XCF and JPG.  Opaque formats
include proprietary formats that can be read and edited only by
proprietary word processors, SGML or XML for which the DTD and/or
processing tools are not generally available, and the
machine-generated HTML, PostScript or PDF produced by some word
processors for output purposes only.

The "Title Page" means, for a printed book, the title page itself,
plus such following pages as are needed to hold, legibly, the material
this License requires to appear in the title page.  For works in
formats which do not have any title page as such, "Title Page" means
the text near the most prominent appearance of the work's title,
preceding the beginning of the body of the text.

The "publisher" means any person or entity that distributes copies of
the Document to the public.

A section "Entitled XYZ" means a named subunit of the Document whose
title either is precisely XYZ or contains XYZ in parentheses following
text that translates XYZ in another language.  (Here XYZ stands for a
specific section name mentioned below, such as "Acknowledgements",
"Dedications", "Endorsements", or "History".)  To "Preserve the Title"
of such a section when you modify the Document means that it remains a
section "Entitled XYZ" according to this definition.

The Document may include Warranty Disclaimers next to the notice which
states that this License applies to the Document.  These Warranty
Disclaimers are considered to be included by reference in this
License, but only as regards disclaiming warranties: any other
implication that these Warranty Disclaimers may have is void and has
no effect on the meaning of this License.

2. VERBATIM COPYING

You may copy and distribute the Document in any medium, either
commercially or noncommercially, provided that this License, the
copyright notices, and the license notice saying this License applies
to the Document are reproduced in all copies, and that you add no
other conditions whatsoever to those of this License.  You may not use
technical measures to obstruct or control the reading or further
copying of the copies you make or distribute.  However, you may accept
compensation in exchange for copies.  If you distribute a large enough
number of copies you must also follow the conditions in section 3.

You may also lend copies, under the same conditions stated above, and
you may publicly display copies.


3. COPYING IN QUANTITY

If you publish printed copies (or copies in media that commonly have
printed covers) of the Document, numbering more than 100, and the
Document's license notice requires Cover Texts, you must enclose the
copies in covers that carry, clearly and legibly, all these Cover
Texts: Front-Cover Texts on the front cover, and Back-Cover Texts on
the back cover.  Both covers must also clearly and legibly identify
you as the publisher of these copies.  The front cover must present
the full title with all words of the title equally prominent and
visible.  You may add other material on the covers in addition.
Copying with changes limited to the covers, as long as they preserve
the title of the Document and satisfy these conditions, can be treated
as verbatim copying in other respects.

If the required texts for either cover are too voluminous to fit
legibly, you should put the first ones listed (as many as fit
reasonably) on the actual cover, and continue the rest onto adjacent
pages.

If you publish or distribute Opaque copies of the Document numbering
more than 100, you must either include a machine-readable Transparent
copy along with each Opaque copy, or state in or with each Opaque copy
a computer-network location from which the general network-using
public has access to download using public-standard network protocols
a complete Transparent copy of the Document, free of added material.
If you use the latter option, you must take reasonably prudent steps,
when you begin distribution of Opaque copies in quantity, to ensure
that this Transparent copy will remain thus accessible at the stated
location until at least one year after the last time you distribute an
Opaque copy (directly or through your agents or retailers) of that
edition to the public.

It is requested, but not required, that you contact the authors of the
Document well before redistributing any large number of copies, to
give them a chance to provide you with an updated version of the
Document.


4. MODIFICATIONS

You may copy and distribute a Modified Version of the Document under
the conditions of sections 2 and 3 above, provided that you release
the Modified Version under precisely this License, with the Modified
Version filling the role of the Document, thus licensing distribution
and modification of the Modified Version to whoever possesses a copy
of it.  In addition, you must do these things in the Modified Version:

A. Use in the Title Page (and on the covers, if any) a title distinct
   from that of the Document, and from those of previous versions
   (which should, if there were any, be listed in the History section
   of the Document).  You may use the same title as a previous version
   if the original publisher of that version gives permission.
B. List on the Title Page, as authors, one or more persons or entities
   responsible for authorship of the modifications in the Modified
   Version, together with at least five of the principal authors of the
   Document (all of its principal authors, if it has fewer than five),
   unless they release you from this requirement.
C. State on the Title page the name of the publisher of the
   Modified Version, as the publisher.
D. Preserve all the copyright notices of the Document.
E. Add an appropriate copyright notice for your modifications
   adjacent to the other copyright notices.
F. Include, immediately after the copyright notices, a license notice
   giving the public permission to use the Modified Version under the
   terms of this License, in the form shown in the Addendum below.
G. Preserve in that license notice the full lists of Invariant Sections
   and required Cover Texts given in the Document's license notice.
H. Include an unaltered copy of this License.
I. Preserve the section Entitled "History", Preserve its Title, and add
   to it an item stating at least the title, year, new authors, and
   publisher of the Modified Version as given on the Title Page.  If
   there is no section Entitled "History" in the Document, create one
   stating the title, year, authors, and publisher of the Document as
   given on its Title Page, then add an item describing the Modified
   Version as stated in the previous sentence.
J. Preserve the network location, if any, given in the Document for
   public access to a Transparent copy of the Document, and likewise
   the network locations given in the Document for previous versions
   it was based on.  These may be placed in the "History" section.
   You may omit a network location for a work that was published at
   least four years before the Document itself, or if the original
   publisher of the version it refers to gives permission.
K. For any section Entitled "Acknowledgements" or "Dedications",
   Preserve the Title of the section, and preserve in the section all
   the substance and tone of each of the contributor acknowledgements
   and/or dedications given therein.
L. Preserve all the Invariant Sections of the Document,
   unaltered in their text and in their titles.  Section numbers
   or the equivalent are not considered part of the section titles.
M. Delete any section Entitled "Endorsements".  Such a section
   may not be included in the Modified Version.
N. Do not retitle any existing section to be Entitled "Endorsements"
   or to conflict in title with any Invariant Section.
O. Preserve any Warranty Disclaimers.

If the Modified Version includes new front-matter sections or
appendices that qualify as Secondary Sections and contain no material
copied from the Document, you may at your option designate some or all
of these sections as invariant.  To do this, add their titles to the
list of Invariant Sections in the Modified Version's license notice.
These titles must be distinct from any other section titles.

You may add a section Entitled "Endorsements", provided it contains
nothing but endorsements of your Modified Version by various
parties--for example, statements of peer review or that the text has
been approved by an organization as the authoritative definition of a
standard.

You may add a passage of up to five words as a Front-Cover Text, and a
passage of up to 25 words as a Back-Cover Text, to the end of the list
of Cover Texts in the Modified Version.  Only one passage of
Front-Cover Text and one of Back-Cover Text may be added by (or
through arrangements made by) any one entity.  If the Document already
includes a cover text for the same cover, previously added by you or
by arrangement made by the same entity you are acting on behalf of,
you may not add another; but you may replace the old one, on explicit
permission from the previous publisher that added the old one.

The author(s) and publisher(s) of the Document do not by this License
give permission to use their names for publicity for or to assert or
imply endorsement of any Modified Version.


5. COMBINING DOCUMENTS

You may combine the Document with other documents released under this
License, under the terms defined in section 4 above for modified
versions, provided that you include in the combination all of the
Invariant Sections of all of the original documents, unmodified, and
list them all as Invariant Sections of your combined work in its
license notice, and that you preserve all their Warranty Disclaimers.

The combined work need only contain one copy of this License, and
multiple identical Invariant Sections may be replaced with a single
copy.  If there are multiple Invariant Sections with the same name but
different contents, make the title of each such section unique by
adding at the end of it, in parentheses, the name of the original
author or publisher of that section if known, or else a unique number.
Make the same adjustment to the section titles in the list of
Invariant Sections in the license notice of the combined work.

In the combination, you must combine any sections Entitled "History"
in the various original documents, forming one section Entitled
"History"; likewise combine any sections Entitled "Acknowledgements",
and any sections Entitled "Dedications".  You must delete all sections
Entitled "Endorsements".


6. COLLECTIONS OF DOCUMENTS

You may make a collection consisting of the Document and other
documents released under this License, and replace the individual
copies of this License in the various documents with a single copy
that is included in the collection, provided that you follow the rules
of this License for verbatim copying of each of the documents in all
other respects.

You may extract a single document from such a collection, and
distribute it individually under this License, provided you insert a
copy of this License into the extracted document, and follow this
License in all other respects regarding verbatim copying of that
document.


7. AGGREGATION WITH INDEPENDENT WORKS

A compilation of the Document or its derivatives with other separate
and independent documents or works, in or on a volume of a storage or
distribution medium, is called an "aggregate" if the copyright
resulting from the compilation is not used to limit the legal rights
of the compilation's users beyond what the individual works permit.
When the Document is included in an aggregate, this License does not
apply to the other works in the aggregate which are not themselves
derivative works of the Document.

If the Cover Text requirement of section 3 is applicable to these
copies of the Document, then if the Document is less than one half of
the entire aggregate, the Document's Cover Texts may be placed on
covers that bracket the Document within the aggregate, or the
electronic equivalent of covers if the Document is in electronic form.
Otherwise they must appear on printed covers that bracket the whole
aggregate.


8. TRANSLATION

Translation is considered a kind of modification, so you may
distribute translations of the Document under the terms of section 4.
Replacing Invariant Sections with translations requires special
permission from their copyright holders, but you may include
translations of some or all Invariant Sections in addition to the
original versions of these Invariant Sections.  You may include a
translation of this License, and all the license notices in the
Document, and any Warranty Disclaimers, provided that you also include
the original English version of this License and the original versions
of those notices and disclaimers.  In case of a disagreement between
the translation and the original version of this License or a notice
or disclaimer, the original version will prevail.

If a section in the Document is Entitled "Acknowledgements",
"Dedications", or "History", the requirement (section 4) to Preserve
its Title (section 1) will typically require changing the actual
title.


9. TERMINATION

You may not copy, modify, sublicense, or distribute the Document
except as expressly provided under this License.  Any attempt
otherwise to copy, modify, sublicense, or distribute it is void, and
will automatically terminate your rights under this License.

However, if you cease all violation of this License, then your license
from a particular copyright holder is reinstated (a) provisionally,
unless and until the copyright holder explicitly and finally
terminates your license, and (b) permanently, if the copyright holder
fails to notify you of the violation by some reasonable means prior to
60 days after the cessation.

Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, receipt of a copy of some or all of the same material does
not give you any rights to use it.


10. FUTURE REVISIONS OF THIS LICENSE

The Free Software Foundation may publish new, revised versions of the
GNU Free Documentation License from time to time.  Such new versions
will be similar in spirit to the present version, but may differ in
detail to address new problems or concerns.  See
http://www.gnu.org/copyleft/.

Each version of the License is given a distinguishing version number.
If the Document specifies that a particular numbered version of this
License "or any later version" applies to it, you have the option of
following the terms and conditions either of that specified version or
of any later version that has been published (not as a draft) by the
Free Software Foundation.  If the Document does not specify a version
number of this License, you may choose any version ever published (not
as a draft) by the Free Software Foundation.  If the Document
specifies that a proxy can decide which future versions of this
License can be used, that proxy's public statement of acceptance of a
version permanently authorizes you to choose that version for the
Document.

11. RELICENSING

"Massive Multiauthor Collaboration Site" (or "MMC Site") means any
World Wide Web server that publishes copyrightable works and also
provides prominent facilities for anybody to edit those works.  A
public wiki that anybody can edit is an example of such a server.  A
"Massive Multiauthor Collaboration" (or "MMC") contained in the site
means any set of copyrightable works thus published on the MMC site.

"CC-BY-SA" means the Creative Commons Attribution-Share Alike 3.0
license published by Creative Commons Corporation, a not-for-profit
corporation with a principal place of business in San Francisco,
California, as well as future copyleft versions of that license
published by that same organization.

"Incorporate" means to publish or republish a Document, in whole or in
part, as part of another Document.

An MMC is "eligible for relicensing" if it is licensed under this
License, and if all works that were first published under this License
somewhere other than this MMC, and subsequently incorporated in whole or
in part into the MMC, (1) had no cover texts or invariant sections, and
(2) were thus incorporated prior to November 1, 2008.

The operator of an MMC Site may republish an MMC contained in the site
under CC-BY-SA on the same site at any time before August 1, 2009,
provided the MMC is eligible for relicensing.


ADDENDUM: How to use this License for your documents

To use this License in a document you have written, include a copy of
the License in the document and put the following copyright and
license notices just after the title page:

    Copyright (c)  YEAR  YOUR NAME.
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
    A copy of the license is included in the section entitled "GNU
    Free Documentation License".

If you have Invariant Sections, Front-Cover Texts and Back-Cover Texts,
replace the "with...Texts." line with this:

    with the Invariant Sections being LIST THEIR TITLES, with the
    Front-Cover Texts being LIST, and with the Back-Cover Texts being LIST.

If you have Invariant Sections without Cover Texts, or some other
combination of the three, merge those two alternatives to suit the
situation.

If your document contains nontrivial examples of program code, we
recommend releasing these examples in parallel under your choice of
free software license, such as the GNU General Public License,
to permit their use in free software.



================================================
FILE: .travis.yml
================================================
language: ruby
rvm:
  - 2.2
before_script:
  - gem install awesome_bot
script:
  - awesome_bot README.md --allow-dupe --white-list proprogramming.org,web.archive.org,travis-ci.org

