**Selenium tests for Seamless Access**

Contains tests for: 
- Google Chrome release 91
- Firefox release 89    
- Microsoft Edge(dev) release 93              

Selenium setup: https://selenium-python.readthedocs.io/installation.html

Json files contain configuration data (search inputs, idp urls etc.) for test configuration
**Be sure to put the Webdrivers in your PATH and give access**: `cmhod -x geckodriver/chromedriver` etc.

check https://docs.google.com/document/d/1b--uuHo93_cp-oG5SFqup3XAMpXYYMJ_RQCSVuf_fCM/edit?ts=604884f7# for test descriptions

running tests in command line: 

    python3 filename [options] [--json JSON] [--browser BROWSER] [OPTIONAL --headless HEADLESS] [OPTIONAL --mobile MOBILE] [OPTIONAL --device DEVICE] ([REQUIRED binary BINARY]) -- -k Classname

For MSEdge tests under Linux we need to give beside the browser driver the browser binary location as well (usually installation location, '/opt/microsoft/msedge-dev/microsoft-edge-dev'), --binary location is only required if the browser is Edge.

browser options:
1. "firefox"
2. "chrome"
3. "edge" 

**msedge-selenium tools need to be installed under Linux for Edge tests** 

    pip install msedge-selenium-tools selenium==3.141


**e.g. (run all tests):** 

    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' --headless 'False' -- -k SeamlessTests

**running only 1 test in command line (look up the function name in seamless_tests.py) e.g.:** 

    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' -- -k SeamlessTests.test_selecting_institution

**The return code is 0 only if the test is OK. (You can use this fact to integrate with automated monitoring)**

    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' -- -k SeamlessTests.test_selecting_institution && <run some command or log to a file>

**e.g. for Edge and writing results to file:** 

    python3 seamless_tests.py --json 'spec_char_inputs.json' --browser 'edge' --headless 'False' --binary '/opt/microsoft/msedge-dev/microsoft-edge-dev' --mobile 'false' -- -k SeamlessTests.test_add_4th_selection &>> results.txt


**a simple, basic test suite for automated monitoring (1A, 1B, 1D, 3A)**

    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' --headless 'True' -- -k SeamlessTests.test_selecting_institution
    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' --headless 'True' -- -k SeamlessTests.too_many_results
    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' --headless 'True' -- -k SeamlessTests.test_show_all_matches
    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' --headless 'True' -- -k SeamlessTests.test_learn_more

**some more advanced tests (2A1, 2A2, 2B, 2D)**

    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' --headless 'True' -- -k SeamlessTests.test_remember_selection
    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' --headless 'True' -- -k SeamlessTests.test_remember_selection2
    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' --headless 'True' -- -k SeamlessTests.test_delete_selection
    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' --headless 'True' -- -k SeamlessTests.test_remember_selection

**very advanced tests (1C, 2C2, 2C2)**

    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' --headless 'True' -- -k SeamlessTests.test_typing_delays
    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' --headless 'True' -- -k SeamlessTests.test_add_more_selection
    python3 seamless_tests.py --json 'inputs.json' --browser 'firefox' --headless 'True' -- -k SeamlessTests.test_add_4th_selection

