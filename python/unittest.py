# File: u (Python 2.4)

__author__ = 'Steve Purcell'
__email__ = 'stephen_purcell at yahoo dot com'
__version__ = '#Revision: 1.63 $'[11:-2]
import time
import sys
import traceback
import os
import types
__all__ = [
    'TestResult',
    'TestCase',
    'TestSuite',
    'TextTestRunner',
    'TestLoader',
    'FunctionTestCase',
    'main',
    'defaultTestLoader']
__all__.extend([
    'getTestCaseNames',
    'makeSuite',
    'findTestCases'])
if sys.version_info[:2] < (2, 2):
    (False, True) = (0, 1)
    
    def isinstance(obj, clsinfo):
        import __builtin__ as __builtin__
        if type(clsinfo) in (types.TupleType, types.ListType):
            for cls in clsinfo:
                if cls is type:
                    cls = types.ClassType
                
                if __builtin__.isinstance(obj, cls):
                    return 1
                    continue
            
            return 0
        else:
            return __builtin__.isinstance(obj, clsinfo)


__metaclass__ = type

def _strclass(cls):
    return '%s.%s' % (cls.__module__, cls.__name__)

__unittest = 1

class TestResult:
    
    def __init__(self):
        self.failures = []
        self.errors = []
        self.testsRun = 0
        self.shouldStop = 0

    
    def startTest(self, test):
        self.testsRun = self.testsRun + 1

    
    def stopTest(self, test):
        pass

    
    def addError(self, test, err):
        self.errors.append((test, self._exc_info_to_string(err, test)))

    
    def addFailure(self, test, err):
        self.failures.append((test, self._exc_info_to_string(err, test)))

    
    def addSuccess(self, test):
        pass

    
    def wasSuccessful(self):
        if len(self.failures) == len(self.errors):
            pass
        len(self.errors) == 0
        return 1

    
    def stop(self):
        self.shouldStop = True

    
    def _exc_info_to_string(self, err, test):
        (exctype, value, tb) = err
        while tb and self._is_relevant_tb_level(tb):
            tb = tb.tb_next
        if exctype is test.failureException:
            length = self._count_relevant_tb_levels(tb)
            return ''.join(traceback.format_exception(exctype, value, tb, length))
        
        return ''.join(traceback.format_exception(exctype, value, tb))

    
    def _is_relevant_tb_level(self, tb):
        return tb.tb_frame.f_globals.has_key('__unittest')

    
    def _count_relevant_tb_levels(self, tb):
        length = 0
        while tb and not self._is_relevant_tb_level(tb):
            length += 1
            tb = tb.tb_next
        return length

    
    def __repr__(self):
        return '<%s run=%i errors=%i failures=%i>' % (_strclass(self.__class__), self.testsRun, len(self.errors), len(self.failures))



class TestCase:
    failureException = AssertionError
    
    def __init__(self, methodName = 'runTest'):
        
        try:
            self._TestCase__testMethodName = methodName
            testMethod = getattr(self, methodName)
            self._TestCase__testMethodDoc = testMethod.__doc__
        except AttributeError:
            raise ValueError, 'no such test method in %s: %s' % (self.__class__, methodName)


    
    def setUp(self):
        pass

    
    def tearDown(self):
        pass

    
    def countTestCases(self):
        return 1

    
    def defaultTestResult(self):
        return TestResult()

    
    def shortDescription(self):
        doc = self._TestCase__testMethodDoc
        if not doc or doc.split('\n')[0].strip():
            pass

    
    def id(self):
        return '%s.%s' % (_strclass(self.__class__), self._TestCase__testMethodName)

    
    def __str__(self):
        return '%s (%s)' % (self._TestCase__testMethodName, _strclass(self.__class__))

    
    def __repr__(self):
        return '<%s testMethod=%s>' % (_strclass(self.__class__), self._TestCase__testMethodName)

    
    def run(self, result = None):
        if result is None:
            result = self.defaultTestResult()
        
        result.startTest(self)
        testMethod = getattr(self, self._TestCase__testMethodName)
        
        try:
            self.setUp()
        except KeyboardInterrupt:
            raise 
        except:
            result.addError(self, self._TestCase__exc_info())
            return None
        

        ok = False
        
        try:
            testMethod()
            ok = True
        except self.failureException:
            result.addFailure(self, self._TestCase__exc_info())
        except KeyboardInterrupt:
            raise 
        except:
            result.addError(self, self._TestCase__exc_info())

        
        try:
            self.tearDown()
        except KeyboardInterrupt:
            raise 
        except:
            result.addError(self, self._TestCase__exc_info())
            ok = False

        if ok:
            result.addSuccess(self)
        result.stopTest(self)

    
    def __call__(self, *args, **kwds):
        return self.run(*args, **args)

    
    def debug(self):
        self.setUp()
        getattr(self, self._TestCase__testMethodName)()
        self.tearDown()

    
    def _TestCase__exc_info(self):
        (exctype, excvalue, tb) = sys.exc_info()
        if sys.platform[:4] == 'java':
            return (exctype, excvalue, tb)
        
        return (exctype, excvalue, tb)

    
    def fail(self, msg = None):
        raise self.failureException, msg

    
    def failIf(self, expr, msg = None):
        if expr:
            raise self.failureException, msg
        

    
    def failUnless(self, expr, msg = None):
        if not expr:
            raise self.failureException, msg
        

    
    def failUnlessRaises(self, excClass, callableObj, *args, **kwargs):
        
        try:
            callableObj(*args, **args)
        except excClass:
            return None

        if hasattr(excClass, '__name__'):
            excName = excClass.__name__
        else:
            excName = str(excClass)
        raise self.failureException, '%s not raised' % excName

    
    def failUnlessEqual(self, first, second, msg = None):
        if not first == second:
            if not msg:
                pass
            raise self.failureException, '%r != %r' % (first, second)
        

    
    def failIfEqual(self, first, second, msg = None):
        if first == second:
            if not msg:
                pass
            raise self.failureException, '%r == %r' % (first, second)
        

    
    def failUnlessAlmostEqual(self, first, second, places = 7, msg = None):
        if round(second - first, places) != 0:
            if not msg:
                pass
            raise self.failureException, '%r != %r within %r places' % (first, second, places)
        

    
    def failIfAlmostEqual(self, first, second, places = 7, msg = None):
        if round(second - first, places) == 0:
            if not msg:
                pass
            raise self.failureException, '%r == %r within %r places' % (first, second, places)
        

    assertEqual = failUnlessEqual
    assertEquals = failUnlessEqual
    assertNotEqual = failIfEqual
    assertNotEquals = failIfEqual
    assertAlmostEqual = failUnlessAlmostEqual
    assertAlmostEquals = failUnlessAlmostEqual
    assertNotAlmostEqual = failIfAlmostEqual
    assertNotAlmostEquals = failIfAlmostEqual
    assertRaises = failUnlessRaises
    assert_ = failUnless
    assertTrue = failUnless
    assertFalse = failIf


class TestSuite:
    
    def __init__(self, tests = ()):
        self._tests = []
        self.addTests(tests)

    
    def __repr__(self):
        return '<%s tests=%s>' % (_strclass(self.__class__), self._tests)

    __str__ = __repr__
    
    def __iter__(self):
        return iter(self._tests)

    
    def countTestCases(self):
        cases = 0
        for test in self._tests:
            cases += test.countTestCases()
        
        return cases

    
    def addTest(self, test):
        self._tests.append(test)

    
    def addTests(self, tests):
        for test in tests:
            self.addTest(test)
        

    
    def run(self, result):
        for test in self._tests:
            if result.shouldStop:
                break
            
            test(result)
        
        return result

    
    def __call__(self, *args, **kwds):
        return self.run(*args, **args)

    
    def debug(self):
        for test in self._tests:
            test.debug()
        



class FunctionTestCase(TestCase):
    
    def __init__(self, testFunc, setUp = None, tearDown = None, description = None):
        TestCase.__init__(self)
        self._FunctionTestCase__setUpFunc = setUp
        self._FunctionTestCase__tearDownFunc = tearDown
        self._FunctionTestCase__testFunc = testFunc
        self._FunctionTestCase__description = description

    
    def setUp(self):
        if self._FunctionTestCase__setUpFunc is not None:
            self._FunctionTestCase__setUpFunc()
        

    
    def tearDown(self):
        if self._FunctionTestCase__tearDownFunc is not None:
            self._FunctionTestCase__tearDownFunc()
        

    
    def runTest(self):
        self._FunctionTestCase__testFunc()

    
    def id(self):
        return self._FunctionTestCase__testFunc.__name__

    
    def __str__(self):
        return '%s (%s)' % (_strclass(self.__class__), self._FunctionTestCase__testFunc.__name__)

    
    def __repr__(self):
        return '<%s testFunc=%s>' % (_strclass(self.__class__), self._FunctionTestCase__testFunc)

    
    def shortDescription(self):
        if self._FunctionTestCase__description is not None:
            return self._FunctionTestCase__description
        
        doc = self._FunctionTestCase__testFunc.__doc__
        if not doc or doc.split('\n')[0].strip():
            pass



class TestLoader:
    testMethodPrefix = 'test'
    sortTestMethodsUsing = cmp
    suiteClass = TestSuite
    
    def loadTestsFromTestCase(self, testCaseClass):
        if issubclass(testCaseClass, TestSuite):
            raise TypeError('Test cases should not be derived from TestSuite. Maybe you meant to derive from TestCase?')
        
        testCaseNames = self.getTestCaseNames(testCaseClass)
        if not testCaseNames and hasattr(testCaseClass, 'runTest'):
            testCaseNames = [
                'runTest']
        
        return self.suiteClass(map(testCaseClass, testCaseNames))

    
    def loadTestsFromModule(self, module):
        tests = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, (type, types.ClassType)) and issubclass(obj, TestCase):
                tests.append(self.loadTestsFromTestCase(obj))
                continue
        
        return self.suiteClass(tests)

    
    def loadTestsFromName(self, name, module = None):
        parts = name.split('.')
        if module is None:
            parts_copy = parts[:]
            while parts_copy:
                
                try:
                    module = __import__('.'.join(parts_copy))
                continue
                except ImportError:
                    del parts_copy[-1]
                    if not parts_copy:
                        raise 
                    
                

            parts = parts[1:]
        
        obj = module
        for part in parts:
            parent = obj
            obj = getattr(obj, part)
        
        if type(obj) == types.ModuleType:
            return self.loadTestsFromModule(obj)
        elif isinstance(obj, (type, types.ClassType)) and issubclass(obj, TestCase):
            return self.loadTestsFromTestCase(obj)
        elif type(obj) == types.UnboundMethodType:
            return parent(obj.__name__)
        elif isinstance(obj, TestSuite):
            return obj
        elif callable(obj):
            test = obj()
            if not isinstance(test, (TestCase, TestSuite)):
                raise ValueError, 'calling %s returned %s, not a test' % (obj, test)
            
            return test
        else:
            raise ValueError, "don't know how to make test from: %s" % obj

    
    def loadTestsFromNames(self, names, module = None):
        continue
        suites = [ self.loadTestsFromName(name, module) for name in names ]
        return self.suiteClass(suites)

    
    def getTestCaseNames(self, testCaseClass):
        
        def isTestMethod(attrname, testCaseClass = testCaseClass, prefix = self.testMethodPrefix):
            if attrname.startswith(prefix):
                pass
            return callable(getattr(testCaseClass, attrname))

        testFnNames = filter(isTestMethod, dir(testCaseClass))
        for baseclass in testCaseClass.__bases__:
            for testFnName in self.getTestCaseNames(baseclass):
                if testFnName not in testFnNames:
                    testFnNames.append(testFnName)
                    continue
            
        
        if self.sortTestMethodsUsing:
            testFnNames.sort(self.sortTestMethodsUsing)
        
        return testFnNames


defaultTestLoader = TestLoader()

def _makeLoader(prefix, sortUsing, suiteClass = None):
    loader = TestLoader()
    loader.sortTestMethodsUsing = sortUsing
    loader.testMethodPrefix = prefix
    if suiteClass:
        loader.suiteClass = suiteClass
    
    return loader


def getTestCaseNames(testCaseClass, prefix, sortUsing = cmp):
    return _makeLoader(prefix, sortUsing).getTestCaseNames(testCaseClass)


def makeSuite(testCaseClass, prefix = 'test', sortUsing = cmp, suiteClass = TestSuite):
    return _makeLoader(prefix, sortUsing, suiteClass).loadTestsFromTestCase(testCaseClass)


def findTestCases(module, prefix = 'test', sortUsing = cmp, suiteClass = TestSuite):
    return _makeLoader(prefix, sortUsing, suiteClass).loadTestsFromModule(module)


class _WritelnDecorator:
    
    def __init__(self, stream):
        self.stream = stream

    
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

    
    def writeln(self, arg = None):
        if arg:
            self.write(arg)
        
        self.write('\n')



class _TextTestResult(TestResult):
    separator1 = '=' * 70
    separator2 = '-' * 70
    
    def __init__(self, stream, descriptions, verbosity):
        TestResult.__init__(self)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    
    def getDescription(self, test):
        if self.descriptions:
            if not test.shortDescription():
                pass
            return str(test)
        else:
            return str(test)

    
    def startTest(self, test):
        TestResult.startTest(self, test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(' ... ')
        

    
    def addSuccess(self, test):
        TestResult.addSuccess(self, test)
        if self.showAll:
            self.stream.writeln('ok')
        elif self.dots:
            self.stream.write('.')
        

    
    def addError(self, test, err):
        TestResult.addError(self, test, err)
        if self.showAll:
            self.stream.writeln('ERROR')
        elif self.dots:
            self.stream.write('E')
        

    
    def addFailure(self, test, err):
        TestResult.addFailure(self, test, err)
        if self.showAll:
            self.stream.writeln('FAIL')
        elif self.dots:
            self.stream.write('F')
        

    
    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    
    def printErrorList(self, flavour, errors):
        for (test, err) in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln('%s: %s' % (flavour, self.getDescription(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln('%s' % err)
        



class TextTestRunner:
    
    def __init__(self, stream = sys.stderr, descriptions = 1, verbosity = 1):
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity

    
    def _makeResult(self):
        return _TextTestResult(self.stream, self.descriptions, self.verbosity)

    
    def run(self, test):
        result = self._makeResult()
        startTime = time.time()
        test(result)
        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        self.stream.writeln(result.separator2)
        run = result.testsRun
        if not run != 1 or 's':
            pass
        self.stream.writeln('Ran %d test%s in %.3fs' % (run, '', timeTaken))
        self.stream.writeln()
        if not result.wasSuccessful():
            self.stream.write('FAILED (')
            (failed, errored) = map(len, (result.failures, result.errors))
            if failed:
                self.stream.write('failures=%d' % failed)
            
            if errored:
                if failed:
                    self.stream.write(', ')
                
                self.stream.write('errors=%d' % errored)
            
            self.stream.writeln(')')
        else:
            self.stream.writeln('OK')
        return result



class TestProgram:
    USAGE = "Usage: %(progName)s [options] [test] [...]\n\nOptions:\n  -h, --help       Show this message\n  -v, --verbose    Verbose output\n  -q, --quiet      Minimal output\n\nExamples:\n  %(progName)s                               - run default set of tests\n  %(progName)s MyTestSuite                   - run suite 'MyTestSuite'\n  %(progName)s MyTestCase.testSomething      - run MyTestCase.testSomething\n  %(progName)s MyTestCase                    - run all 'test*' test methods\n                                               in MyTestCase\n"
    
    def __init__(self, module = '__main__', defaultTest = None, argv = None, testRunner = None, testLoader = defaultTestLoader):
        if type(module) == type(''):
            self.module = __import__(module)
            for part in module.split('.')[1:]:
                self.module = getattr(self.module, part)
            
        else:
            self.module = module
        if argv is None:
            argv = sys.argv
        
        self.verbosity = 1
        self.defaultTest = defaultTest
        self.testRunner = testRunner
        self.testLoader = testLoader
        self.progName = os.path.basename(argv[0])
        self.parseArgs(argv)
        self.runTests()

    
    def usageExit(self, msg = None):
        if msg:
            print msg
        
        print self.USAGE % self.__dict__
        sys.exit(2)

    
    def parseArgs(self, argv):
        import getopt as getopt
        
        try:
            (options, args) = getopt.getopt(argv[1:], 'hHvq', [
                'help',
                'verbose',
                'quiet'])
            for (opt, value) in options:
                if opt in ('-h', '-H', '--help'):
                    self.usageExit()
                
                if opt in ('-q', '--quiet'):
                    self.verbosity = 0
                
                if opt in ('-v', '--verbose'):
                    self.verbosity = 2
                    continue
            
            if len(args) == 0 and self.defaultTest is None:
                self.test = self.testLoader.loadTestsFromModule(self.module)
                return None
            
            if len(args) > 0:
                self.testNames = args
            else:
                self.testNames = (self.defaultTest,)
            self.createTests()
        except getopt.error:
            msg = None
            self.usageExit(msg)


    
    def createTests(self):
        self.test = self.testLoader.loadTestsFromNames(self.testNames, self.module)

    
    def runTests(self):
        if self.testRunner is None:
            self.testRunner = TextTestRunner(verbosity = self.verbosity)
        
        result = self.testRunner.run(self.test)
        sys.exit(not result.wasSuccessful())


main = TestProgram
if __name__ == '__main__':
    main(module = None)

