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
    exports_sources = ["*.patch", "FindGBenchmark.cmake"]
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

        cmake.definitions["BENCHMARK_ENABLE_GTEST_TESTS"] = "OFF"
        cmake.definitions["BENCHMARK_ENABLE_TESTING"] = "OFF"
        cmake.definitions['CMAKE_VERBOSE_MAKEFILE'] = "ON"

        cmake.configure(source_dir=self.source_subfolder)
        cmake.build()

    def package(self):
        self.copy("FindGBenchmark.cmake", ".", ".")

        # Copy the license files
        self.copy("LICENSE", dst="licenses", src=self.source_subfolder)

        # Copying headers
        include_dir = os.path.join(self.source_subfolder, "include", "benchmark")

        self.copy(pattern="*.h", dst="include/benchmark", src=include_dir, keep_path=True)

        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=".", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['benchmark_main', 'benchmark']

        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
