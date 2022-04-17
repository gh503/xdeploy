" ============================================================================================ "
"                                          VIM 基础配置
" ============================================================================================ "
set encoding=utf-8                  " 设置编码方式
set fileencodings=utf-8,gbk         " 自动判断编码时，依次尝试编码
set ambiwidth=double                " 双 宽显示

filetype on                         " 开启文件类型检查，并载入该类型对应的缩进规则(如.py文件加载，$HOME/.vim/intent/python.vim)
filetype indent on                  " 这里使用统一缩进
filetype plugin on                  " 允许插件
filetype plugin indent on           " 启动智能补全(ctrl-p)

set helplang=cn                     " 中文帮助文档
set ff=unix                         " 设置文件格式unix
set nocompatible                    " 不与vi兼容，使用vim自己的命令
set mouse=a                         " 所有模式下支持鼠标
set notimeout                       " 命令下发后时延

syntax enable                       " 语法高亮
syntax on

set number                          " 显示行号
set relativenumber                  " 显示光标所在当前行号，其他行相对于该行的行号
if has("nvim-0.5.0") || has("patch-8.1.1564")
  set signcolumn=number
else
  set signcolumn=yes
endif

set cursorline                      " 突出显示当前行
set cursorcolumn                    " 突出显示当前列
set showmatch                       " 显示括号匹配
set hlsearch                        " 高亮显示搜索结果
exec "nohlsearch"
let &t_SI = "\<Esc>]50;CursorShape=1\x7"
let &t_SR = "\<Esc>]50;CursorShape=2\x7"
let &t_EI = "\<Esc>]50;CursorShape=0\x7"
set laststatus=2                    " 总是显示状态栏
au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif  " 自动定位到上次编辑的位置

set list                            " 显示不可见字符，并定制行尾空格、tab键显示符号
set listchars=tab:>-,trail:-,precedes:«,extends:»

set textwidth=132                   " 设置行宽
set wrap                            " 设置自动换行（单行字符超过行宽）
set linebreak                       " 设置遇到指定字符换行
set iskeyword+=_,$,@,%,#,-          " 遇到指定字符不换行
set wrapmargin=2                    " 指定折行处与编辑窗口右边缘之间空处的字符数
set scrolloff=3                     " 垂直滚动时光标距离顶/底部行数
set sidescrolloff=5                 " 水平滚动时光标距离行首/尾字符数(不折行时使用)

set fillchars=vert:\ ,stl:\ ,stlnc:\ " 分割窗口间显示空白

set showtabline=2                   " 显示标签栏
set tabpagemax=15                   " 同时打开的标签页

set cmdheight=3                     " 命令行高度
set showcmd                         " 状态栏显示正在输入的命令

set ruler                           " 状态栏显示光标行列位置
set showmode                        " 底部显示当前模式

set nospell
set spelllang=en_us,cjk             " 英中日韩单词拼写检查

set autoindent                      " 回车自动同上行缩进
set tabstop=4                       " Tab缩进空格数
set shiftwidth=4                    " 文本上增加/取消一级或者取消全部缩进时，每级字符数
set expandtab                       " Tab转空格
set softtabstop=4                   " Tab转空格数
set smarttab                        " 按退格键一次删除4个空格
set backspace=indent,eol,start      " 设置退格键可退到上一行

set incsearch                       " 搜索模式时，每输入一个字符自动跳到第1个匹配结果
set ignorecase                      " 搜索时忽略大小写
set smartcase                       " 配合ignorecase，只对第1个字母大小写敏感。搜Test不匹配test，但搜test匹配Test

set history=66                      " 设置历史记录条数
set updatetime=300                  " 等待300ms后无输入将交换文件写入磁盘
set nobackup                        " 取消备份
set noswapfile                      " 禁止临时文件生成

set autochdir                       " 自动切换到当前文件目录
set errorbells                      " 出错时发出响声
set visualbell                      " 出错时发出视觉提示
set autoread                        " 编辑时文件发生外部变更，给出提示
set wildmenu                        " 命令模式下，底部操作指令按Tab补全，第1次按显示所有匹配指令清单，第2次按以次选择各指令
set wildmode=longest:list,full

set nofoldenable
set foldlevel=99
set foldmethod=indent

set clipboard+=unnamed              " y,p操作与系统粘贴板共享。配合vimx使用(安装vim-gtk)
