import os.path
from datetime import datetime

import pytest

from cfnbot import parser


def test_absolute_link():
    a = parser.absolute_link('foo.html', base='http://example.com')
    assert a == 'http://example.com/foo.html'


def common_wrap(inner):
    return f"""
<html>
  <body>
    <div id="content-container">
      <div id="main-column">
        <div id="main">
          <div id="main-content">
            <div id="main-col-body">
              <table summary="Breadcrumbs"><tr><td>Not here...</td></tr></table>
              <h1 class="topictitle">Release History</h1>
              <p>Some header content</p>
              <div class="table">
                <div class="table-contents">
                  <table id="w423ab1c27b5">
                    <tr>
                      <th>Change</th>
                      <th>Description</th>
                      <th>Date</th>
                    </tr>
                    {inner}
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>"""


def test_release_atoms_1():
    html = common_wrap("""
<tr>
  <td><p>Generic update</p></td>
  <td>
    <p>This was a generic update.</p>
    <p>For more information see foo.</p>
  </td>
  <td>December 13, 2018</td>
</tr>
""")
    atoms = list(parser.get_release_atoms(html))
    assert atoms == [('Generic update', 'This was a generic update.',
                      parser.RELEASE_HISTORY, 'December 13, 2018')]


def test_release_atoms_2():
    html = common_wrap("""
<tr>
  <td><p>New resources</p></td>
  <td>
    <p>The following resources were added: AWS::foo, AWS::bar, AWS::baz.</p>
    <dl>
      <dt><a href="example.html">AWS::foo</a></dt>
      <dd>
        <p>Use the AWS::foo resource for testing.</p>
      </dd>
      <dt><a href="https://example.com">AWS::bar</a></dt>
      <dd>
        <ul>
          <li>In the foo property type, you can use the property.</li>
          <li>In the bar property type, also have some fun.</li>
        </ul>
      </dd>
      <dt>AWS::baz</dt>
      <dd>
        <p>Use the foo property for specifying the namespace.</p>
        <p>In the bar property type, use the RoutingPolicy.</p>
      </dd>
    </dl>
  </td>
  <td>December 13, 2018</td>
</tr>
""")
    atoms = list(parser.get_release_atoms(html))
    assert atoms == [
        ('New AWS::foo', 'Use the AWS::foo resource for testing.',
         parser.absolute_link('example.html'), 'December 13, 2018'),
        ('New AWS::bar', 'In the foo property type, you can use the property.',
         'https://example.com', 'December 13, 2018'),
        ('New AWS::bar', 'In the bar property type, also have some fun.',
         'https://example.com', 'December 13, 2018'),
        ('New AWS::baz', 'Use the foo property for specifying the namespace.',
         parser.RELEASE_HISTORY, 'December 13, 2018'),
        ('New AWS::baz', 'In the bar property type, use the RoutingPolicy.',
         parser.RELEASE_HISTORY, 'December 13, 2018'),
    ]
    

# If there is a paragraph where the last character is a colon, followed by
# a ul, then iterate over all entries in that list and prefix it by the
# preceding paragraph

def test_release_atoms_3():
    html = common_wrap("""
<tr>
  <td><p>Updated resource</p></td>
  <td>
    <p>The following resource was updated: AWS::foo.</p>
    <div class="variablelist">
      <dl>
        <dt> <span class="term">AWS::foo</span></dt>
        <dd>
          <p>The following attributes are now available: </p>
          <div class="itemizedlist">
            <ul class="itemizedlist">
              <li class="listitem">bar</li>
              <li class="listitem">baz</li>
            </ul>
          </div>
        </dd>
      </dl>
    </div>
  </td>
  <td>December 13, 2018</td>
</tr>
""")
    atoms = list(parser.get_release_atoms(html))
    assert atoms == [
        ('Updated AWS::foo',
         'The following attributes are now available: bar, baz',
         parser.RELEASE_HISTORY, 'December 13, 2018'),
    ]


def test_all_current_atoms():
    # This loads the currently live page, and merely verifies that no
    # exception is raised.
    html = parser.get_release_history()
    for atom in parser.get_release_atoms(html):
        assert len(atom) == 4
        # The date should parse consistently
        assert datetime.strptime(atom[-1], '%B %d, %Y') < datetime.now()
