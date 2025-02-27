# conf.py 파일

# -- 프로젝트 정보 -----------------------------------------------------
project = 'Telelian Wiki'
copyright = '2025, dghwang'
author = 'dghwang'
release = '1.0.0'

# -- 일반 설정 ---------------------------------------------------------
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

# -- 국제화 설정 -------------------------------------------------------
language = 'ko'

# -- HTML 출력 설정 ----------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- MyST-Parser 설정 --------------------------------------------------
# MyST-Parser의 확장 기능을 활성화하려면 다음과 같이 설정할 수 있습니다.
# 자세한 내용은 MyST-Parser 공식 문서를 참고하세요.
# https://myst-parser.readthedocs.io/en/latest/configuration.html
myst_enable_extensions = [
    'dollarmath',  # $ 수학 표기법 지원
    'colon_fence',  # ::: 블록 지원
    # 필요한 다른 확장자를 여기에 추가하세요
]

# -- 기타 설정 ---------------------------------------------------------
# 자동으로 모듈 이름을 문서에 추가하지 않으려면 다음과 같이 설정할 수 있습니다.
add_module_names = False
myst_heading_anchors = 3
# 필요에 따라 추가 설정을 여기에 작성하세요.
