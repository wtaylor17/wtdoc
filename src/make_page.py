HTML_FORMAT_TEMPLATE = '<!doctype html>\n\
<html>\n\
<head>\n\
<script src=\'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML\' async></script>\n\
</head>\n\
<body style="background-color:rgba(100, 50, 100, 0.2)">\n\
%s\
</body>\n\
</html>'


def fetch_comments(pyfile_lines, start_index):
    commentlines = []
    i = start_index + 2
    while not pyfile_lines[i].strip() == "'''":
        commentlines.append(pyfile_lines[i].strip())
        i += 1
    return commentlines


def handle_method(pyfile_lines, pyline, htmlbody_lines, i):
    clines = fetch_comments(pyfile_lines, i)
    try:
        param_ind = min([j for j in range(len(clines)) if clines[j] == 'parameters:'])
    except:
        print(clines)
    # start function list item
    htmlbody_lines.append('<li>')
    htmlbody_lines.append('<h3>%s</h3>' % pyline[4:])
    htmlbody_lines.append('<p>')
    for c in clines[:param_ind]:
        htmlbody_lines.append(c + '</br>')
    htmlbody_lines.append('</p>')
    htmlbody_lines.append('<h4>Parameters</h4>')
    htmlbody_lines.append('<ul>')
    for c in clines[param_ind + 1:]:
        htmlbody_lines.append('<li>%s</li>' % c)
    htmlbody_lines.append('</ul>')
    htmlbody_lines.append('</li>')


def handle_class(pyfile_lines, pyline, htmlbody_lines, i):
    clines = fetch_comments(pyfile_lines, i)
    htmlbody_lines.append('<h3>%s</h3>' % pyline)
    htmlbody_lines.append('<p>')
    for c in clines:
        htmlbody_lines.append(c + '</br>')
    htmlbody_lines.append('</p>')

    while pyfile_lines[i] != '#endclass':
        pyline = pyfile_lines[i].strip()
        if pyline.startswith('def '):
            handle_method(pyfile_lines, pyline, htmlbody_lines, i)
        i += 1


if __name__ == '__main__':
    import sys

    pypath, htmlpath, pagetitle = None, None, None
    for i, a in enumerate(sys.argv):
        if a == '-i':
            pypath = sys.argv[i + 1]
        elif a == '-o':
            htmlpath = sys.argv[i + 1]
        elif a == '-t':
            pagetitle = sys.argv[i + 1]

    if htmlpath is None or pypath is None or pagetitle is None:
        exit('Usage: python make_page.py -i <python_file> -o <output_file> -t <page_title>')

    htmlbody_lines = ['<center><h1>%s</h1></center>' % pagetitle]
    with open(pypath, 'r') as pyfile:
        pyfile_lines = pyfile.read().split('\n')
        k = 1
        htmlbody_lines.append('<center><p>')
        while pyfile_lines[k] != "'''":
            htmlbody_lines.append(pyfile_lines[k] + '</br>')
            k += 1
        htmlbody_lines.append('</center></p>')
        htmlbody_lines.extend(['<h2>Functions and Classes</h2>', '<ul>'])
        for i, pyline in enumerate(pyfile_lines):
            if pyline.startswith('def '):
                handle_method(pyfile_lines, pyline, htmlbody_lines, i)
            elif pyline.startswith('class '):
                handle_class(pyfile_lines, pyline, htmlbody_lines, i)
        htmlbody_lines.append('</ul>')

    with open(htmlpath, 'w') as htmlfile:
        htmlfile.write(HTML_FORMAT_TEMPLATE % (''.join([line + '\n' for line in htmlbody_lines])))