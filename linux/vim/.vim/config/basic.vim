" ============================================================================================ "
"                                          VIM 基础配置
" ============================================================================================ "
" 设置编码方式
set encoding=utf-8
" 自动判断编码时，依次尝试编码
set fileencodings=utf-8,gbk
" 双宽显示
set ambiwidth=double
" 行末结束符
set binary
set noeol
" 设置文件格式unix
set ff=unix

" 开启文件类型检查，并载入该类型对应的缩进规则(如.py文件加载，$HOME/.vim/intent/python.vim)
filetype on
" 这里使用统一缩进
filetype indent on
" 允许插件
filetype plugin on
" 启动智能补全(ctrl-p)
filetype plugin indent on

" 中文帮助文档
set helplang=cn
" 不与vi兼容，使用vim自己的命令
set nocompatible
" 所有模式下支持鼠标
set mouse=a
" 命令下发后时延
set notimeout

" 语法高亮
syntax enable
syntax on

" 显示行号
set number
" 显示光标所在当前行号，其他行相对于该行的行号
set relativenumber
if has("nvim-0.5.0") || has("patch-8.1.1564")
  set signcolumn=number
else
  set signcolumn=yes
endif

" 突出显示当前行
set cursorline
" 突出显示当前列
set cursorcolumn
" 显示括号匹配
set showmatch
" 高亮显示搜索结果
set hlsearch
exec "nohlsearch"
" 总是显示状态栏
set laststatus=2
" 自动定位到上次编辑的位置
au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif

" 显示不可见字符，并定制行尾空格、tab键显示符号
set list
set listchars=tab:>-,trail:-,precedes:«,extends:»

" 设置行宽
set textwidth=132
" 设置自动换行（单行字符超过行宽）
set wrap
" 设置遇到指定字符换行
set linebreak
" 遇到指定字符不换行
set iskeyword+=_,$,@,%,#,-
" 指定折行处与编辑窗口右边缘之间空处的字符数
set wrapmargin=2
" 垂直滚动时光标距离顶/底部行数
set scrolloff=3
" 水平滚动时光标距离行首/尾字符数(不折行时使用)
set sidescrolloff=5
" 分割窗口间显示空白
set fillchars=vert:\ ,stl:\ ,stlnc:\ 

" 显示标签栏
set showtabline=2
" 同时打开的标签页
set tabpagemax=15

" 命令行高度
set cmdheight=3
" 状态栏显示正在输入的命令
set showcmd

" 状态栏显示光标行列位置
set ruler
" 底部显示当前模式
set showmode

set nospell
" 英中日韩单词拼写检查
set spelllang=en_us,cjk

" 回车自动同上行缩进
set autoindent
" Tab缩进空格数
set tabstop=4
" 文本上增加/取消一级或者取消全部缩进时，每级字符数
set shiftwidth=4
" Tab转空格
set expandtab
" Tab转空格数
set softtabstop=4
" 按退格键一次删除4个空格
set smarttab
" 设置退格键可退到上一行
set backspace=indent,eol,start

" 搜索模式时，每输入一个字符自动跳到第1个匹配结果
set incsearch
" 搜索时忽略大小写
set ignorecase
" 配合ignorecase，只对第1个字母大小写敏感。搜Test不匹配test，但搜test匹配Test
set smartcase

" 设置历史记录条数
set history=66
" 等待300ms后无输入将交换文件写入磁盘
set updatetime=300
" 取消备份
set nobackup
" 禁止临时文件生成
set noswapfile

" 自动切换到当前文件目录
set autochdir
" 出错时发出响声
set errorbells
" 出错时发出视觉提示
set visualbell
" 编辑时文件发生外部变更，给出提示
set autoread
" 命令模式下，底部操作指令按Tab补全，第1次按显示所有匹配指令清单，第2次按以次选择各指令
set wildmenu
set wildmode=longest:list,full

set nofoldenable
set foldlevel=99
set foldmethod=indent

" y,p操作与系统粘贴板共享。配合vimx使用(安装vim-gtk)
set clipboard+=unnamed
