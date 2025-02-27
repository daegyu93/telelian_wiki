project = 'Telelian Wiki'
copyright = '2025, dghwang'
author = 'dghwang'
release = '1.1.0'

extensions = [
    'myst_parser',  # Markdown 지원
    'sphinx.ext.autodoc',  # 자동 문서화
    'sphinx.ext.napoleon',  # Google 스타일 docstring 지원
    'sphinx_copybutton',  # 복사 버튼 추가
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# MyST-Parser setup
myst_enable_extensions = [
    'dollarmath',  # $ 수학 표기법 지원
    'colon_fence',  # ::: 블록 지원
]

add_module_names = False
myst_heading_anchors = 3
