#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans import ConanFile, CMake, tools
import os


class GbenchmarkConan(ConanFile):
    name = "gbenchmark"
    version = "1.4.1"
    description = "Google's C++ benchmark framework"
    url = "http://github.com/bincrafters/conan-gbenchmark"
    license = "BSD 3-Clause"
    exports = ["LICENSE.md"]
    exports_sources = ["*.patch"]    
    generators = "cmake"
    source_subfolder = 'source_subfolder'
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = ("shared=False", "fPIC=True")

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        source_url = "https://github.com/google/benchmark"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = "benchmark-" + self.version
        tools.patch(patch_file='werror.patch')                
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        cmake = CMake(self)
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC

        #cmake.definitions["BENCHMARK_BUILD_32_BITS"] = "ON"
        
        cmake.definitions["BENCHMARK_ENABLE_GTEST_TESTS"] = "OFF"
        cmake.definitions['CMAKE_VERBOSE_MAKEFILE'] = "ON"        
        #cmake.definitions["BUILD_GBENCHMARK"] = True
        #cmake.definitions["BUILD_GMOCK"] = self.options.build_gmock

        # if self.settings.os == "Android":
        #     cmake.definitions["ANDROID"] = True
        #     cmake.definitions["CONAN_LIBCXX"] = ''
            
        cmake.configure(source_dir=self.source_subfolder)
        cmake.build()

    def package(self):
        # Copy the license files
        self.copy("LICENSE", dst="licenses", src=self.source_subfolder)

        # Copying headers
        include_dir = os.path.join(self.source_subfolder, "include", "benchmark")

        self.copy(pattern="*.h", dst="include", src=include_dir, keep_path=True)

        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=".", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", src=".", keep_path=False)

    def package_info(self):
        pass
        # if self.options.build_gmock:
        #     self.cpp_info.libs = ['gmock_main', 'gmock', 'gtest']
        # else:
        #     self.cpp_info.libs = ['gtest_main', 'gtest']

        # if self.settings.os == "Linux":
        #     self.cpp_info.libs.append("pthread")

        # if self.options.shared:
        #     self.cpp_info.defines.append("GTEST_LINKED_AS_SHARED_LIBRARY=1")
        #     if self.settings.compiler == "Visual Studio" and self.settings.compiler.version == "11":
        #         self.cpp_info.defines.append('_VARIADIC_MAX=10')

        # if self.settings.compiler == "Visual Studio" and float(str(self.settings.compiler.version)) >= 15:
        #     self.cpp_info.defines.append("GTEST_LANG_CXX11=1")
        #     self.cpp_info.defines.append("GTEST_HAS_TR1_TUPLE=0")
