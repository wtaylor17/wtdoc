if __name__ == '__main__':
    import os
    for module in ['signal', 'data', 'vis']:
        os.system('python make_page.py -i ../util/%s.py -o util/%s.html -t phase_analysis.util.%s' % (module,module,module))
    print('FINISHED UTIL SUBMODULE...')
    for module in ['signal']:
        os.system('python make_page.py -i ../legacy/%s.py -o legacy/%s.html -t phase_analysis.legacy.%s' % (module,module,module))
    print('FINISHED LEGACY SUBMODULE...')
    for module in ['backend', 'embedded', 'config', 'neural']:
        os.system('python make_page.py -i ../%s.py -o %s.html -t phase_analysis.%s' % (module,module,module))
    print('FINISHED MAIN DIRECTORY MODULES...')