#!/usr/bin/python
# -*- coding: utf-8 -*-

from fedora.client import PackageDB
import unittest
import logging
import imp

pkgdb = imp.load_source('pkgdb', 'pkgdb-cli')



class testPkgdDBCli(unittest.TestCase):
    def setUp(self):
        """ set up data used in the tests.
        setUp is called before each test function execution.
        """
        pkgdb.pkgdbclient = PackageDB('https://admin.stg.fedoraproject.org/pkgdb',
                        insecure=True)
        pkgdb.log.setLevel(logging.DEBUG)
        print pkgdb.pkgdbclient.base_url

    def testGetPackageInfo(self):
        out = pkgdb.get_package_info('guake', 'all', False, True)
        out = pkgdb.get_package_info('guake', 'devel', False, True)
        out = pkgdb.get_package_info('guake', 'all', False, False)
        out = pkgdb.get_package_info('guake', 'all', True, True)

    def testGetPackages(self):
        pkgdb.get_packages('R-*', branch='all')
        pkgdb.get_packages('R-*', branch='devel')

    def testGetOrphanedPackages(self):
        pkgdb.get_orphaned_packages('perl-*', eol=False,
                                    name_only=False,
                                    branch='all')
        pkgdb.get_orphaned_packages('perl-*', eol=True,
                                    name_only=True,
                                    branch='all')
        pkgdb.get_orphaned_packages('perl-*', eol=True,
                                    name_only=True,
                                    branch='devel')

    def testGetPackagerInfo(self):
        pkgdb.get_packager_info('pingou', motif=None,
                                    name_only=False,
                                    branch='all')
        pkgdb.get_packager_info('pingou', motif=None,
                                    name_only=True,
                                    branch='all')
        pkgdb.get_packager_info('pingou', motif='R-*',
                                    name_only=False,
                                    branch='all')
        pkgdb.get_packager_info('pingou', motif='R-*',
                                    name_only=False,
                                    branch='devel')

    def testOrphanPackage(self):
        pkgdb.orphan_package('R-ROC', 'devel', False, None, None)

    def testUnOrphanPackage(self):
        pkgdb.unorphan_package('R-ROC', 'devel', None, None)

    def testGetBranches(self):
        branches = pkgdb._get_active_branches()
        self.assertTrue(len(branches) >= 5)
        self.assertTrue(len(branches) <= 6)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testPkgdDBCli))
    return suite


if __name__ == '__main__':

    suiteFew = unittest.TestSuite()
    suiteFew.addTest(testPkgdDBCli("testGetPackageInfo"))
    suiteFew.addTest(testPkgdDBCli("testGetOrphanedPackages"))
    suiteFew.addTest(testPkgdDBCli("testGetPackagerInfo"))
    suiteFew.addTest(testPkgdDBCli("testOrphanPackage"))
    suiteFew.addTest(testPkgdDBCli("testUnOrphanPackage"))
    #suiteFew.addTest(testPkgdDBCli("testGetPackages"))
    suiteFew.addTest(testPkgdDBCli("testGetBranches"))
    unittest.TextTestRunner(verbosity=2).run(suite())
